import os
import weaviate
import weaviate.classes as wvc
from sqlalchemy.orm import properties
from weaviate.classes.config import Configure, Property, DataType
from weaviate.util import generate_uuid5


COLLECTION_NAME = "ArticleIndex"

def connect_weaviate():
    return weaviate.connect_to_custom(
        http_host=os.getenv("WEAVIATE_HTTP_HOST", "weaviate"),
        http_port=int(os.getenv("WEAVIATE_HTTP_PORT", "8080")),
        http_secure=False,
        grpc_host=os.getenv("WEAVIATE_GRPC_HOST", "weaviate"),
        grpc_port=int(os.getenv("WEAVIATE_GRPC_PORT", "50051")),
        grpc_secure=False
    )


def ensure_collection(client):
    if client.collections.exists(COLLECTION_NAME):
        return

    client.collections.create(
        name=COLLECTION_NAME,
        vector_config=Configure.Vectors.self_provided(),
        properties=[
            Property(name="article_id", data_type=DataType.TEXT),
            Property(name="user_id", data_type=DataType.TEXT),
            Property(name="title", data_type=DataType.TEXT),
            Property(name="main_text", data_type=DataType.TEXT),
        ]
    )


def article_uuid(article_id):
    return generate_uuid5({"article_id": str(article_id)})


def upsert_article(
        client,
        article_id,
        user_id,
        title,
        main_text,
        vector: list[float],
):
    ensure_collection(client)
    collection = client.collections.use(COLLECTION_NAME)

    payload = {
        "article_id": str(article_id),
        "user_id": str(user_id),
        "title": title,
        "main_text": main_text,
    }

    uid = article_uuid(article_id)

    try:
        collection.data.delete_by_id(uid)
    except Exception as e:
        print(e)
        pass

    collection.data.insert(
        properties=payload,
        vector=vector,
        uuid=uid
    )