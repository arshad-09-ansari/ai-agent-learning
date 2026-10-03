from app.services.chat_service import chat


def main():
    print("=" * 50)
    print("   AI agents platform")
    print("=" * 50)

    while True:
        question = input("\nYou: ").strip()

        if not question:
            continue

        if question.lower() == "exit":
            print("goodbye")
            break

        try:
            answer = chat(question)
        except Exception as exc:  # pragma: no cover - CLI UX path
            print(f"\nError: {exc}")
            continue

        print("\nGemini:")
        print(answer)


if __name__ == "__main__":
    main()