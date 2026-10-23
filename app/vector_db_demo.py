import chromadb

client = chromadb.Client()

collection = client.create_collection(
    name="java_docs"
)

collection.add(
    ids=["1", "2", "3", "4"],

    documents=[
        "Java is an object-oriented programming language.",
        "Spring Boot is used to build Java backend applications.",
        "Redis is an in-memory data store.",
        "Kafka is used for event streaming and messaging."
    ],

    metadatas=[
        {"topic": "java"},
        {"topic": "spring"},
        {"topic": "redis"},
        {"topic": "kafka"}
    ]
)

print("Documents stored successfully.")