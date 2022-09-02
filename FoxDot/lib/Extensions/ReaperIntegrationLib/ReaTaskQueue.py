

class ReaTask(object):
    def __init__(self, type, reaper_object, param_name, param_value):
        self.id = id(self)
        self.type = type
        self.reaper_object = reaper_object
        self.param_name = param_name
        self.param_value = param_value
        self.result = None


class TaskQueue(object):
    """
    Time recursive task queue to ensure access of any value in reaper is executed with reapy inside_reaper context
    and avoid "inside_reaper" based race condition (provoque crash in the use of reapy socket)
    """
    def __init__(self, clock, reapylib):
        self.queue = []
        self.size = 200
        self.clock = clock
        self.is_active = False
        self.reapylib = reapylib
        self.task_execution_freq = 0.1
        self.currently_processing_tasks = False

    def __repr__(self):
        return f"<TaskQueue active: {self.is_active} tasks number: {len(self.queue)}>"

    def set_inactive(self):
        self.is_active = False
        self.queue = []

    def set_active(self):
        self.is_active = True


    def add_task(self, task: ReaTask):
        if len(self.queue) < self.size:
            if self.is_active:
                self.queue.append(task)
                if not self.currently_processing_tasks:
                    self.clock.future(self.task_execution_freq, self.execute_tasks, args=[])
            else:
                print("Queue is inactive")
        else:
            print("Maximum reapy tasks in queue reached")

    def execute_tasks(self):
        if not self.currently_processing_tasks and self.is_active:
            self.currently_processing_tasks = True
            with self.reapylib.inside_reaper():
                while self.queue:
                    task: ReaTask = self.queue.pop(0)
                    if task.type == "set":
                        task.reaper_object.set_param_direct(task.param_name, task.param_value)
                        task.reaper_object.set_param(task.param_name, task.param_value)
            self.currently_processing_tasks = False
            #if self.is_active:
            self.clock.future(self.task_execution_freq, self.execute_tasks, args=[])

    def timevar_update_loop(self, rea_object, name, value, state, update_freq):
        if rea_object.reaparams[name].state == state and self.is_active:
            self.add_task(ReaTask("set", rea_object, name, value))
            self.clock.future(update_freq, self.timevar_update_loop, args=[rea_object, name, value, state, update_freq])
