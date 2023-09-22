from models import MODELS


def setup_llm(model):
    if model == "hello":
        model = MODELS[model]
        response_model = model()
    return response_model
