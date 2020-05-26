import inspect
from .base import Status

class SourceRegister:
    actions = []

    @classmethod
    def register_action(cls, method, owner):
        if "triggers" in inspect.getfullargspec(method)[0]:
            triggers_present = True
        else:
            triggers_present = False

        method_dict =  {
            'index': register_source_action.get_method_count_for(owner),
            'class': owner,
            'func': method,
            'triggers': triggers_present,
            'async': inspect.iscoroutinefunction(method)
        }
        cls.actions.append(method_dict)
    
    @classmethod
    def get_method_count_for(cls, data_source_class):
        count = 0
        for method_dict in cls.actions:
            if method_dict['class'] == data_source_class:
                count += 1
        return count

    @classmethod
    def get_long_pole_count(cls):
        max_index = 0
        for method_dict in cls.actions:
            index = method_dict['index']
            if index > max_index:
                max_index = index
        return max_index + 1

    @classmethod
    def get_source_action_at_index(cls, source_class, index):
        for method_dict in cls.actions:
            if method_dict['class'] == source_class and \
                method_dict['index'] == index:
                return method_dict['func']
        else:
            return None
    
    @classmethod
    def get_actions_by_async_at_index(cls, index):
        async_funcs = []
        serial_funcs = []
        for method_dict in cls.actions:
            if method_dict['index'] == index and \
                method_dict['async'] is True:
                async_funcs.append(method_dict)
            elif method_dict['index'] == index and \
                method_dict['async'] is False:
                serial_funcs.append(method_dict)
        return async_funcs, serial_funcs

 
class register_source_action(SourceRegister):
    def __init__(self, fn):
        self.fn = fn

    def __set_name__(self, owner, name):
        register_source_action.register_action(
            self.fn, owner
        )
        setattr(owner, name, self.fn)
