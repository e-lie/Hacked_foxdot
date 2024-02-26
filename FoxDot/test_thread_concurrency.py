import threading
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys

class FileModificationHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"Le fichier {event.src_path} a été modifié.")

def monitor_file_changes(path_to_watch):
    event_handler = FileModificationHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def listen_to_stdin():
    try:
        while True:
            user_input = input()
            print(f"Entrée utilisateur reçue: {user_input}")
    except KeyboardInterrupt:
        print("Arrêt de l'écoute de stdin.")

if __name__ == "__main__":
    path_to_watch = "/tmp/foxdotcode.txt"  # Modifiez cela pour le chemin de votre fichier
    # Démarrage du thread de surveillance de fichier
    file_thread = threading.Thread(target=monitor_file_changes, args=(path_to_watch,))
    file_thread.daemon = True
    file_thread.start()

    # Démarrage du thread d'écoute de stdin
    stdin_thread = threading.Thread(target=listen_to_stdin)
    stdin_thread.daemon = True
    stdin_thread.start()

    stdin_thread.join()
    file_thread.join()
