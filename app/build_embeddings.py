import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-embedding-001"


documents = [
    {
        "id": "doc_1",
        "text": "Redis is an in-memory data store commonly used for caching. Redis TTL defines how long a key remains available before it expires.",
        "source": "redis.md",
        "category": "database"
    },
    {
        "id": "doc_2",
        "text": "JWT is a token-based authentication mechanism. JWT expiration defines how long the authentication token remains valid.",
        "source": "jwt.md",
        "category": "security"
    },
    {
        "id": "doc_3",
        "text": "SVC-57 is a Not_Found error returned when the requested resource does not exist. The API should return HTTP 404.",
        "source": "api-errors.md",
        "category": "api"
    },
    {
        "id": "doc_4",
        "text": "Spring Security provides authentication and authorization functionality for Spring Boot applications.",
        "source": "spring-security.md",
        "category": "security"
    },
    {
        "id": "doc_5",
        "text": "PostgreSQL indexes improve query performance by allowing the database to locate rows efficiently.",
        "source": "postgresql.md",
        "category": "database"
    },
    {
        "id": "doc_6",
        "text": "Redis distributed locking can coordinate access to shared resources across application instances.",
        "source": "redis-lock.md",
        "category": "database"
    },
    {
        "id": "doc_7",
        "text": "Payment services should validate webhook signatures before processing payment events.",
        "source": "payment-security.md",
        "category": "payment"
    },
    {
        "id": "doc_8",
        "text": "HTTP 401 indicates authentication is required. HTTP 403 indicates the user is authenticated but does not have permission.",
        "source": "http-status.md",
        "category": "api"
    },
    {
        "id": "doc_9",
        "text": "Kafka is a distributed event streaming platform commonly used for asynchronous communication between microservices.",
        "source": "kafka.md",
        "category": "messaging"
    },
    {
        "id": "doc_10",
        "text": "RabbitMQ is a message broker commonly used for asynchronous communication. Queues store messages until consumers process them.",
        "source": "rabbitmq.md",
        "category": "messaging"
    }
]


def create_embedding(text):

    response = client.models.embed_content(
        model=MODEL,
        contents=text
    )

    return response.embeddings[0].values


def main():

    output = []

    for index, document in enumerate(documents, start=1):

        print(
            f"Embedding document {index}/{len(documents)}..."
        )

        embedding = create_embedding(
            document["text"]
        )

        document_with_embedding = {
            **document,
            "embedding": embedding
        }

        output.append(
            document_with_embedding
        )

    os.makedirs("data", exist_ok=True)

    with open(
        "data/embeddings.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file
        )

    print("\nEmbeddings created successfully.")
    print("Saved to: data/embeddings.json")


if __name__ == "__main__":
    main()