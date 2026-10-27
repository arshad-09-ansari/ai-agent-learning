from app.day32.chains import analyze_story


def main():
    title = "Add JWT authentication"

    description = """
    Users should log in using email and password.
    Access tokens should protect private APIs.
    """

    try:
        result = analyze_story(title, description)

        print("\n========== AI STORY ANALYSIS ==========\n")
        print(result)

    except Exception as exc:
        print(f"Story analysis failed: {exc}")


if __name__ == "__main__":
    main()