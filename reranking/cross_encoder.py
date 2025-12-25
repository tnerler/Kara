from sentence_transformers import CrossEncoder

def get_cross_encoder():
    return CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2", device="cuda")