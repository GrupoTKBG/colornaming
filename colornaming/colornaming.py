from abc import ABC, abstractmethod

class ColorNamingModel(ABC):
    @abstractmethod
    def from_rgb(self, r, g, b):
        pass

    def to_rgb(self, label):
        raise NotImplementedError()     

known_models = {}

def get_model(name, *args, **kwargs):
    return known_models[name](*args, **kwargs)

def register_model(name, cls): 
    known_models[name] = cls