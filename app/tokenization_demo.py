import tiktoken

text = "I am learning Agentic AI engineering."

encoding = tiktoken.get_encoding("cl100k_base")

tokens = encoding.encode(text)

print("Text:")
print(text)

print("\nToken IDs:")
print(tokens)

print("\nNumber of tokens:")
print(len(tokens))

print("\nDecoded tokens:")
for token in tokens:
    print(token, "->", encoding.decode([token]))