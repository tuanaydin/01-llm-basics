from __future__ import annotations

import os

from dotenv import load_dotenv
from google import genai


def main() -> None:
    """Gemini API anahtarının erişebildiği metin üretim modellerini listeler."""

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY bulunamadı. .env dosyasını kontrol edin."
        )

    client = genai.Client(api_key=api_key)

    print("Metin üretimini destekleyen Gemini modelleri:\n")

    model_count = 0

    for model in client.models.list():
        supported_actions = model.supported_actions or []

        if "generateContent" not in supported_actions:
            continue

        model_name = model.name or ""

        # Embedding ve görüntü modelleri yerine Gemini metin modellerini göster.
        if "gemini" not in model_name.lower():
            continue

        print(f"- {model_name}")
        model_count += 1

    print(f"\nToplam uygun model: {model_count}")


if __name__ == "__main__":
    main()