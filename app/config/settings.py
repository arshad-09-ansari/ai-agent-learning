import os
from pathlib import Path

from dotenv import dotenv_values, load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]


def load_environment(env_path: str | os.PathLike[str] | None = None) -> dict[str, str]:
    """Load environment variables from a project .env file or the sample env file."""
    candidate_paths: list[Path] = []

    if env_path is not None:
        candidate_paths.append(Path(env_path))

    candidate_paths.extend([
        BASE_DIR / ".env",
        BASE_DIR / ".env.example",
    ])

    seen: set[Path] = set()
    loaded: dict[str, str] = {}

    for path in candidate_paths:
        resolved = path if path.is_absolute() else BASE_DIR / path
        if resolved in seen:
            continue
        seen.add(resolved)

        if not resolved.exists():
            continue

        for key, value in dotenv_values(resolved).items():
            if key and value is not None:
                loaded[key] = value
                os.environ.setdefault(key, value)

    if not loaded:
        load_dotenv(BASE_DIR / ".env", override=False)
        load_dotenv(BASE_DIR / ".env.example", override=False)

    return {
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", ""),
        "MODEL_NAME": os.getenv("MODEL_NAME", "gemini-3.6-flash"),
    }


load_environment()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-3.6-flash")