from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter
from typing import Any

from src.gemini_client import generate_text


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROMPTS_FILE = (
    PROJECT_ROOT
    / "prompts"
    / "prompt_variations.json"
)

RESULTS_FILE = (
    PROJECT_ROOT
    / "results"
    / "prompt_comparison.json"
)


# Uygulama 2 boyunca model sabit tutulur.
MODEL = "gemini-3.1-flash-lite"

SYSTEM_INSTRUCTION = (
    "Teknik konuları doğru ve anlaşılır biçimde açıklayan "
    "bir yapay zekâ eğitmenisin. "
    "Cevaplarını Türkçe ver ve kullanıcı talimatlarına uy."
)


# Uygulama 2 boyunca bu ayarlar değişmeyecek.
TEMPERATURE = 1.0
TOP_P = 0.9
SEED = 42
MAX_OUTPUT_TOKENS = 1200


def load_prompt_variations() -> list[dict[str, str]]:
    """
    Prompt varyasyonlarını JSON dosyasından okur.
    """

    if not PROMPTS_FILE.exists():
        raise FileNotFoundError(
            f"Prompt dosyası bulunamadı: {PROMPTS_FILE}"
        )

    with PROMPTS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        prompt_variations = json.load(file)

    if not isinstance(prompt_variations, list):
        raise ValueError(
            "Prompt dosyasının ana yapısı bir liste olmalıdır."
        )

    if not prompt_variations:
        raise ValueError(
            "Prompt dosyası boş. En az bir prompt eklenmelidir."
        )

    required_fields = {
        "id",
        "level",
        "title",
        "prompt",
    }

    for index, variation in enumerate(prompt_variations):
        missing_fields = (
            required_fields
            - variation.keys()
        )

        if missing_fields:
            raise ValueError(
                f"{index}. promptta eksik alanlar var: "
                f"{sorted(missing_fields)}"
            )

    return prompt_variations


def run_experiment(
    prompt_variations: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """
    Aynı modele farklı prompt varyasyonlarını gönderir.
    """

    results: list[dict[str, Any]] = []

    for index, variation in enumerate(
        prompt_variations,
        start=1,
    ):
        print("\n" + "=" * 70)
        print(
            f"[{index}/{len(prompt_variations)}] "
            f"{variation['title']}"
        )
        print(f"SEVİYE: {variation['level']}")
        print("=" * 70)

        print("\nGÖNDERİLEN PROMPT")
        print("-" * 70)
        print(variation["prompt"])

        start_time = perf_counter()

        try:
            answer = generate_text(
                prompt=variation["prompt"],
                model=MODEL,
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                seed=SEED,
                max_output_tokens=MAX_OUTPUT_TOKENS,
            )

            elapsed_seconds = (
                perf_counter()
                - start_time
            )

            result = {
                "experiment": "prompt_comparison",
                "model": MODEL,
                "prompt_id": variation["id"],
                "prompt_level": variation["level"],
                "prompt_title": variation["title"],
                "prompt": variation["prompt"],
                "response": answer,
                "response_character_count": len(answer),
                "elapsed_seconds": round(
                    elapsed_seconds,
                    3,
                ),
                "settings": {
                    "temperature": TEMPERATURE,
                    "top_p": TOP_P,
                    "seed": SEED,
                    "max_output_tokens": (
                        MAX_OUTPUT_TOKENS
                    ),
                },
            }

            results.append(result)

            print("\nMODEL CEVABI")
            print("-" * 70)
            print(answer)

            print("\nTEMEL ÖLÇÜMLER")
            print("-" * 70)
            print(
                "Cevap karakter sayısı:",
                len(answer),
            )
            print(
                "Geçen süre:",
                f"{elapsed_seconds:.3f} saniye",
            )

        except Exception as error:
            elapsed_seconds = (
                perf_counter()
                - start_time
            )

            error_result = {
                "experiment": "prompt_comparison",
                "model": MODEL,
                "prompt_id": variation["id"],
                "prompt_level": variation["level"],
                "prompt_title": variation["title"],
                "prompt": variation["prompt"],
                "error": str(error),
                "elapsed_seconds": round(
                    elapsed_seconds,
                    3,
                ),
            }

            results.append(error_result)

            print("\nHATA")
            print("-" * 70)
            print(error)

    return results


def save_results(
    results: list[dict[str, Any]],
) -> None:
    """
    Prompt karşılaştırma sonuçlarını JSON dosyasına kaydeder.
    """

    RESULTS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output = {
        "experiment_name": "Gemini Prompt Comparison",
        "research_question": (
            "Aynı görev farklı prompt ayrıntı seviyeleriyle "
            "verildiğinde model çıktısı nasıl değişir?"
        ),
        "model": MODEL,
        "controlled_settings": {
            "system_instruction": SYSTEM_INSTRUCTION,
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "seed": SEED,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
        },
        "changed_variable": "prompt",
        "result_count": len(results),
        "results": results,
    }

    with RESULTS_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            output,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print("\n" + "=" * 70)
    print("PROMPT KARŞILAŞTIRMA DENEYİ TAMAMLANDI")
    print(f"Sonuç dosyası: {RESULTS_FILE}")
    print("=" * 70)


def main() -> None:
    prompt_variations = load_prompt_variations()

    results = run_experiment(prompt_variations)

    save_results(results)


if __name__ == "__main__":
    main()