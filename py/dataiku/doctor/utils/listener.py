from . import unix_time_millis
import logging


class ExitState:

    def __init__(self, listener):
        self.listener = listener

    def __exit__(self, type, value, traceback):
        self.listener.pop_state()

    def __enter__(self):
        pass


class ProgressListener(object):
    def __init__(self, verbose=True):
        self.stack = []
        self.top_level_todo = []
        self.top_level_done = []
        self.verbose = verbose

    def to_jsonifiable(self):
        return {
            "stack": self.stack,
            "top_level_todo": self.top_level_todo,
            "top_level_done": self.top_level_done
        }

    def reset(self):
        self.top_level_todo = []
        self.top_level_done = []
        self.stack = []

    def add_future_step(self, name):
        self.top_level_todo.append(name)

    def add_future_steps(self, names):
        self.top_level_todo.extend(names)

    def push_state(self, name, target=None):
        if self.verbose:
            logging.info("START -  " + name)
        if len(self.stack) == 0:
            self.top_level_step_start = unix_time_millis()
            try:
                self.top_level_todo.remove(name)
            except:
                pass
        self.stack.append({"name": name, "target": target})
        return ExitState(self)

    def pop_state(self):
        step = self.stack.pop()
        if self.verbose:
            logging.info("END -  " + step["name"])
        if len(self.stack) == 0:
            step_len = unix_time_millis() - self.top_level_step_start
            self.top_level_done.append({"name": step["name"], "time": step_len})

    def set_current_progress(self, progress):
        self.stack[-1]["current"] = progress
