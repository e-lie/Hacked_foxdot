from __future__ import absolute_import, division, print_function

import re
import os.path
import time
import threading
from traceback import format_exc as error_stack
from types import CodeType, FunctionType
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

try:

    from types import TypeType

except ImportError:

    TypeType = type
    
from ..Utils import modi
from ..Settings import *

"""
Live Object
===========

Base for any self-scheduling objects
"""

# Player RegEx
re_player = re.compile(r"(\s*?)(\w+)\s*?>>\s*?\w+")

class LiveObject(object):

    foxdot_object = True
    isAlive = True
    
    metro = None
    step  = None
    n     = 0
    
    def kill(self):
        self.isAlive = False
        return self

    def __call__(self):
        self.metro.schedule(self, self.metro.now() + float(modi(self.step, self.n)))
        self.n += 1
        return self

"""
    FoxCode
    =======
    Handles the execution of FoxDot code
    
"""

class CodeString:
    def __init__(self, raw):
        self.raw = raw
        self.iter = -1
        self.lines = [s + "\n" for s in self.raw.split("\n")] + ['']
    def readline(self):
        self.iter += 1
        return self.lines[self.iter]
    def __str__(self):
        return self.raw

if sys.version_info[0] > 2:

    def clean(string):
        string = string.replace("\u03BB", "lambda")
        return string

else:

    def clean(string):
        """ Removes non-ascii characters from a string """
        string = string.replace(u"\u03BB", "lambda")
        return string.encode("ascii", "replace")

class _StartupFile:
    def __init__(self, path):
        self.set_path(path)
    def set_path(self, path):
        self.path = path if path  is None else os.path.realpath(path)

    def load(self):
        if self.path is not None:
            try:
                file = open(self.path)
                code = file.read()
                file.close()
                return code
            except (IOError, OSError):
                WarningMsg("'{}' startup file not found.".format(self.path))
        return ""

FOXDOT_STARTUP = _StartupFile(FOXDOT_STARTUP_PATH)
        
class FoxDotCode:
    namespace={}
    player_line_numbers={}

    @staticmethod
    def _compile(string):
        ''' Returns the bytecode for  '''
        return compile(str(CodeString(string)), "FoxDot", "exec")

    @classmethod
    def use_sample_directory(cls, directory):
        ''' Forces FoxDot to look in `directory` instead of the default 
            directory when using audio samples. '''
        return cls.namespace['symbolToDir'].set_root( directory )

    @classmethod
    def use_startup_file(cls, path):
        return cls.namespace['FOXDOT_STARTUP'].set_path(path)

    @classmethod
    def no_startup(cls):
        return cls.namespace["FOXDOT_STARTUP"].set_path(None)

    def load_startup_file(self): 
        """ Must be initialised first """
        code = self.namespace["FOXDOT_STARTUP"].load()
        return self.__call__(code, verbose=False)
                 
    def __call__(self, code, verbose=True, verbose_error=None):
        """ Takes a string of FoxDot code and executes as Python """

        if verbose_error is None:

            verbose_error = verbose

        if not code:

            return

        try:

            if type(code) != CodeType:

                code = clean(code)

                response = stdout(code)

                if verbose is True:

                    print(response)

            exec(self._compile(code), self.namespace)

        except Exception as e:

            response = error_stack()

            if verbose_error is True:

                print(response)

        return response

    def update_line_numbers(self, text_widget, start="1.0", end="end", remove=0):

        lines = text_widget.get(start, end).split("\n")[remove:]
        update = []
        offset = int(start.split(".")[0])

        for i, line in enumerate(lines):

            # Check line for a player and assign it a line number
            match = re_player.match(line)
            line_changed = False

            if match is not None:                

                whitespace = len(match.group(1))
                player     = match.group(2)
                line       = i + offset

                if player in self.player_line_numbers:

                    if (line, whitespace) != self.player_line_numbers[player]:

                        line_changed = True

                if line_changed or player not in self.player_line_numbers:

                    self.player_line_numbers[player] = (line, whitespace)
                    update.append("{}.id = '{}'".format(player, player))
                    update.append("{}.line_number = {}".format(player, line))
                    update.append("{}.whitespace  = {}".format(player, whitespace))

        # Execute updates if necessary
    
        if len(update) > 0:

            self.__call__("\n".join(update), verbose = False)
                
        return

execute = FoxDotCode() # this is not well named

def get_now(obj):
    """ Returns the value of objects if they are time-varying """
    return getattr(obj, 'now', lambda: obj).__call__()

def get_input():
    """ Similar to `input` but can handle multi-line input. Terminates on a final "\n" """
    line = " "; text = []
    while len(line) > 0:
        line = input("")
        text.append(line)
    return "\n".join(text)

class FileModificationHandler(FileSystemEventHandler):
    def on_modified(self, event):
        file_path ='/tmp/foxdotcode.txt'
        with open(file_path, 'r+') as input_file:
            if os.path.getsize(file_path) > 0:
                foxdot_code_string = input_file.read()
                input_file.seek(0)
                input_file.write('')
                input_file.truncate()
                execute(foxdot_code_string, verbose=False, verbose_error=True)
                #print(f"Code récupéré : {foxdot_code_string}")

def monitor_file_changes(path_to_watch):
    event_handler = FileModificationHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(0.3)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def listen_to_stdin():
    try:
        while True:
            user_input = get_input()
            execute(user_input, verbose=False, verbose_error=True)
            #print(f"Entrée utilisateur reçue: {user_input}")
    except KeyboardInterrupt:
        print("Quit listening stdin.")


async def handle_stdin():
    """ When FoxDot is run with the --pipe added, this function
        is called and continuosly   """

    load_startup_file()

    # thread to continuously watch for modification of a code file
    # and execute new foxdot code each time it changes
    path_to_watch = "/tmp/foxdotcode.txt"
    file_thread = None
    if os.path.exists(path_to_watch):
        file_thread = threading.Thread(target=monitor_file_changes, args=(path_to_watch,))
        file_thread.daemon = True
        file_thread.start()

    # thread to listen to stdin (classic foxdot --pipe mode but non blocking)
    stdin_thread = threading.Thread(target=listen_to_stdin)
    stdin_thread.daemon = True
    stdin_thread.start()

    stdin_thread.join()
    if file_thread:
        file_thread.join()
    sys.exit("Quitting")

    return

def stdout(code):
    """ Shell-based output """
    console_text = code.strip().split("\n")
    return ">>> {}".format("\n... ".join(console_text))

def debug_stdout(*args):
    """ Forces prints to server-side """
    sys.__stdout__.write(" ".join([str(s) for s in args]) + "\n")

def load_startup_file():
    return execute.load_startup_file()

def WarningMsg(*text):
    print("Warning: {}".format( " ".join(str(s) for s in text) ))

def write_to_file(fn, text):
    try:
        with open(fn, "w") as f:
            f.write(clean(text))
    except IOError:
        print("Unable to write to {}".format(fn))
    return

# These functions return information about an imported module

# Should use insepct module

def classes(module):
    """ Returns a list of class names defined in module """
    return [name for name, data in vars(module).items() if type(data) == TypeType]

def instances(module, cls):
    """ Returns a list of instances of cls from module """
    return [name for name, data in vars(module).items() if isinstance(data, cls)]

def functions(module):
    """ Returns a list of function names defined in module """
    return [name for name, data in vars(module).items() if type(data) == FunctionType]
