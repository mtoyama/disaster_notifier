import inspect

class Register(list):
    def add_func(self, index):
        def decorator(func):
            if "triggers" in inspect.getfullargspec(func)[0]:
                triggers_present = True
            else:
                triggers_present = False

            step_dict = {
                "func": func,
                "triggers": triggers_present,
                "async": inspect.iscoroutinefunction(func)
            }
            self.insert(index, step_dict)
            return func
        return decorator