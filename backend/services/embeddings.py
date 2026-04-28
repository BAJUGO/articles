from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def build_article_text(title: str, main_text: str) -> str:
    return f"Title: {title}\n\nText: {main_text}"


def get_embedding(text: str) -> list[float]:
    text = text.replace("\n", " ")
    return model.encode(text).tolist()