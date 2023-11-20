import os
import warnings
from typing import Dict, Optional

kobayashi_moods = {}
mood_palettes = {}

def palette_signature(palette):
    return ":".join(sorted(palette))

def ensure_mood_data():
    if kobayashi_moods != {}:
        return
        
    with open(os.path.join(os.path.dirname(__file__), "data/datos colores kobayashi - Combinations.csv")) as f:
        global mood_palettes
        next(f) # Skip header
        for l in f:
            row = l.split(",")
            palette = row[1:4]
            mood = row[4]
            # Keep mood and original palette
            kobayashi_moods[palette_signature(palette)] = mood
            if mood in mood_palettes:
                mood_palettes[mood].append(palette)
            else:
                mood_palettes[mood] = [palette]

class KobayashiMoods:
    def __init__(self, mood_model):
        self.mood_model = mood_model
        self.moods: Optional[Dict] = None

    def ensure_moods(self):
        if self.moods is not None:
            return
        ensure_mood_data()
        if self.mood_model is not None:
            self.create_mood_model(self.mood_model)
        else:
            self.moods = kobayashi_moods
            self.mood_palettes = mood_palettes

    def create_mood_model(self, mood_model):
        custom_moods = {}
        mood_model_index = {}
        mood_palettes_index = {}
        for label, moods in mood_model.items():
            for mood in moods:
                if mood not in mood_palettes:
                    warnings.warn(f"Warning: unknown mood {mood}")
                mood_model_index[mood] = label
                if label in mood_palettes_index:
                    mood_palettes_index[label].extend(mood_palettes.get(mood, []))
                else:
                    mood_palettes_index[label] = mood_palettes.get(mood, [])
        self.mood_palettes = mood_palettes_index
        for palette, mood in kobayashi_moods.items():
            if mood in mood_model_index:
                custom_moods[palette] = mood_model_index[mood]
        self.moods = custom_moods

    def get_mood(self, colors):
        self.ensure_moods()
        if len(colors) != 3:
            raise ValueError("Expected a 3 color palette")
        return self.moods.get(palette_signature(colors)) # type: ignore
    
    def get_palettes(self, mood):
        self.ensure_moods()
        return self.mood_palettes[mood]


