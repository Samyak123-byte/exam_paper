MODEL = None


def load_model():

    global MODEL

    # Later you can load:
    #
    # SentenceTransformer
    # BERT
    # RoBERTa
    # Custom trained model

    return MODEL


def model_status():

    return {

        "loaded":
            MODEL is not None
    }