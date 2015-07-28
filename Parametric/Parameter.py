__author__ = 'def'

class Parameter:
    def __init__(self, name, object_name, object_property, value=None, min=None, max=None, ):
        self.name = name
        self.object_name = object_name
        self.object_property = object_property
        self.value = None
        self.min = None
        self.max = None

        self.update_object()

    def update_object(self):
        pass