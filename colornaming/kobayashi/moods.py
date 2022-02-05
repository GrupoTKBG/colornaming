import os

kobayashi_moods = {}

def palette_signature(palette):
    return ":".join(sorted(palette))

def ensure_mood_data():
    if kobayashi_moods != {}:
        return
        
    with open(os.path.join(os.path.dirname(__file__), "data/datos colores kobayashi - Combinations.csv")) as f:
        next(f) # Skip header
        for l in f:
            row = l.split(",")
            palette = row[1:4]
            mood = row[4]
            kobayashi_moods[palette_signature(palette)] = mood

class KobayashiMoods:
    def __init__(self, mood_model):
        self.mood_model = mood_model
        self.moods = None

    def ensure_moods(self):
        if self.moods is not None:
            return
        ensure_mood_data()
        if self.mood_model is not None:
            self.create_mood_model(self.mood_model)
        else:
            self.moods = kobayashi_moods

    def create_mood_model(self, mood_model):
        custom_moods = {}
        mood_model_index = {}
        for label, moods in mood_model.items():
            for mood in moods:
                mood_model_index[mood] = label
        for palette, mood in kobayashi_moods.items():
            if mood in mood_model_index:
                custom_moods[palette] = mood_model_index[mood]
        self.moods = custom_moods

    def get_mood(self, colors):
        self.ensure_moods()
        if len(colors) != 3:
            raise ValueError("Expected a 3 color palette")
        return self.moods.get(palette_signature(colors))
