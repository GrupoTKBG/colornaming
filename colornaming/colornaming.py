from abc import ABC, abstractmethod

class ColorNamingModel(ABC):
    @abstractmethod
    def from_rgb(self, r, g, b):
        pass

    def to_rgb(self, label):
        raise NotImplementedError()        

known_models = {}

def get_model(name):
    return known_models[name]

def register_model(name, instance): 
    known_models[name] = instance