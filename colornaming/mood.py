from abc import ABC, abstractmethod

class MoodModel(ABC):
    @abstractmethod
    def get_mood(self, colors):
        pass

    @abstractmethod
    def get_mood_palette_size(self):
        pass

