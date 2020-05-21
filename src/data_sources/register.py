import inspect

class Register(list):
    def add_func(self, index):
        def decorator(func):
            step_dict = {
                "func": func,
                "async" : inspect.iscoroutinefunction(func)
            }
            self.insert(index, step_dict)
            return func
        return decorator