from .colornaming import get_model

class GenericConverter:
    def __call__(self, color):
        pass

class IdentityConverter(GenericConverter):
    def __call__(self, color):
        return color

class AnyToRGBConverter(GenericConverter):
    def __init__(self, from_model):
        self.from_model = get_model(from_model)

    def __call__(self, *args):
        return self.from_model.to_rgb(*args)

class AnyFromRGBConverter(GenericConverter):
    def __init__(self, to_model):
        self.to_model = get_model(to_model)

    def __call__(self, r, g, b):
        return self.to_model.from_rgb(r, g, b)

class AnyViaRGBConverter(GenericConverter):
    def __init__(self, from_model, to_model):
        self.from_model = get_model(from_model)
        self.to_model = get_model(to_model)

    def __call__(self, *args):
        r, g, b = self.from_model.to_rgb(*args)
        return self.to_model.from_rgb(r, g, b)

converter_table = {}

def get_converter(model1, model2):
    if model1 == model2:
        return IdentityConverter()
    elif model2 == "RGB":
        return AnyToRGBConverter(model1)
    elif (model1, model2) in converter_table:
        return converter_table[(model1, model2)]
    else:
        return AnyViaRGBConverter(model1, model2)
