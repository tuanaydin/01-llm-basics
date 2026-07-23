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
    / "hallucination_prompts.json"
)

RESULTS_FILE = (
    PROJECT_ROOT
    / "results"
    / "hallucination_results.json"
)


MODEL = "gemini-3.1-flash-lite"

SYSTEM_INSTRUCTION = (
    "Cevaplarını Türkçe veren teknik bir yapay zekâ asistanısın. "
    "Bilmediğin veya doğrulayamadığın bilgileri uydurma. "
    "Verilen bir bağlam varsa yalnızca o bağlama dayan."
)

TEMPERATURE = 1.0
TOP_P = 0.9
SEED = 42
MAX_OUTPUT_TOKENS = 600


def load_prompts() -> list[dict[str, str]]:
    """Hallucination deney promptlarını JSON dosyasından okur."""

    if not PROMPTS_FILE.exists():
        raise FileNotFoundError(
            f"Prompt dosyası bulunamadı: {PROMPTS_FILE}"
        )

    with PROMPTS_FILE.open("r", encoding="utf-8") as file:
        prompts = json.load(file)

    if not isinstance(prompts, list) or not prompts:
        raise ValueError(
            "hallucination_prompts.json boş veya geçersiz."
        )

    required_fields = {
        "id",
        "category",
        "title",
        "description",
        "prompt",
    }

    for index, prompt_data in enumerate(prompts):
        missing_fields = required_fields - prompt_data.keys()

        if missing_fields:
            raise ValueError(
                f"{index}. promptta eksik alanlar var: "
                f"{sorted(missing_fields)}"
            )

    return prompts


def run_experiment(
    prompts: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Bütün hallucination testlerini aynı modele gönderir."""

    results: list[dict[str, Any]] = []

    for index, prompt_data in enumerate(prompts, start=1):
        print("\n" + "=" * 70)
        print(f"[{index}/{len(prompts)}] {prompt_data['title']}")
        print(f"KATEGORİ: {prompt_data['category']}")
        print("=" * 70)

        print("\nDENEY AÇIKLAMASI")
        print("-" * 70)
        print(prompt_data["description"])

        print("\nGÖNDERİLEN PROMPT")
        print("-" * 70)
        print(prompt_data["prompt"])

        start_time = perf_counter()

        try:
            answer = generate_text(
                prompt=prompt_data["prompt"],
                model=MODEL,
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                seed=SEED,
                max_output_tokens=MAX_OUTPUT_TOKENS,
            )

            elapsed_seconds = perf_counter() - start_time

            result = {
                "experiment": "hallucination_test",
                "model": MODEL,
                "test_id": prompt_data["id"],
                "category": prompt_data["category"],
                "title": prompt_data["title"],
                "description": prompt_data["description"],
                "prompt": prompt_data["prompt"],
                "response": answer,
                "response_character_count": len(answer),
                "elapsed_seconds": round(elapsed_seconds, 3),
                "manual_evaluation": {
                    "invented_person": None,
                    "invented_date": None,
                    "invented_source": None,
                    "used_only_provided_context": None,
                    "acknowledged_missing_information": None,
                    "notes": "",
                },
                "settings": {
                    "temperature": TEMPERATURE,
                    "top_p": TOP_P,
                    "seed": SEED,
                    "max_output_tokens": MAX_OUTPUT_TOKENS,
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
            elapsed_seconds = perf_counter() - start_time

            results.append(
                {
                    "experiment": "hallucination_test",
                    "model": MODEL,
                    "test_id": prompt_data["id"],
                    "category": prompt_data["category"],
                    "title": prompt_data["title"],
                    "prompt": prompt_data["prompt"],
                    "error": str(error),
                    "elapsed_seconds": round(
                        elapsed_seconds,
                        3,
                    ),
                }
            )

            print("\nHATA")
            print("-" * 70)
            print(error)

    return results


def save_results(
    results: list[dict[str, Any]],
) -> None:
    """Hallucination sonuçlarını JSON dosyasına kaydeder."""

    RESULTS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output = {
        "experiment_name": "Gemini Hallucination Test",
        "research_questions": [
            (
                "Model, var olmayan bir kavram hakkında "
                "kişi, tarih veya kaynak uyduruyor mu?"
            ),
            (
                "Daha açık güvenlik talimatları hallucination "
                "riskini azaltıyor mu?"
            ),
            (
                "Model, verilen bağlamda bulunmayan "
                "bilgileri ekliyor mu?"
            ),
        ],
        "model": MODEL,
        "controlled_settings": {
            "system_instruction": SYSTEM_INSTRUCTION,
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "seed": SEED,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
        },
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
    print("HALLUCINATION DENEYİ TAMAMLANDI")
    print(f"Sonuç dosyası: {RESULTS_FILE}")
    print("=" * 70)


def main() -> None:
    prompts = load_prompts()
    results = run_experiment(prompts)
    save_results(results)


if __name__ == "__main__":
    main()