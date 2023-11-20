from abc import ABC, abstractmethod

class ColorNamingModel(ABC):
    @abstractmethod
    def from_rgb(self, r, g, b):
        pass

    def to_rgb(self, label):
        raise NotImplementedError()     

known_models = {}

class QColor(ABC):
    def __str__(self):
        raise NotImplementedError()  

    def to_rgb(self):
        raise NotImplementedError()  

    def from_rgb(self, r, g, b):
        raise NotImplementedError()  
    
class BaseQColor(QColor):
    def __init__(self, label, model):
        self.label = label
        self.model = model

    def __str__(self):
        return self.label

    def to_rgb(self):
        return self.model.to_rgb(self.label)

    def from_rgb(self, r, g, b):
        return self.model.to_rgb(r, g, b)

def get_model(name, *args, **kwargs):
    return known_models[name](*args, **kwargs)

def register_model(name, cls): 
    known_models[name] = cls

def c():
    return known_models.keys()