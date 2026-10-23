text = """
Redis is an in-memory data store.

Redis is commonly used for caching.

TTL defines how long a key should remain available.

When TTL expires, Redis removes the key.

Redis can also be used for session management.
"""

chunk_size = 100

chunks = []

for i in range(0, len(text), chunk_size):
    chunk = text[i:i + chunk_size]
    chunks.append(chunk)

for index, chunk in enumerate(chunks):
    print(f"\n--- Chunk {index + 1} ---")
    print(chunk)