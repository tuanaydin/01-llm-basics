from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter
from typing import Any

from src.gemini_client import generate_text


# Bu dosya src klasörünün içindedir.
# parents[1], bir üst dizine çıkarak proje kökünü bulur.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROMPTS_FILE = (
    PROJECT_ROOT
    / "prompts"
    / "model_prompts.json"
)

RESULTS_FILE = (
    PROJECT_ROOT
    / "results"
    / "model_comparison.json"
)


# Karşılaştırılacak iki model.
MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
]


# Her iki modele de aynı sistem talimatı gönderilecek.
SYSTEM_INSTRUCTION = (
    "Teknik konuları doğru ve anlaşılır biçimde açıklayan "
    "bir yapay zekâ eğitmenisin. "
    "Cevaplarını Türkçe ver. "
    "Kullanıcının uzunluk, format ve içerik talimatlarına uy."
)


# Deney boyunca sabit tutulacak üretim ayarları.
#Uygulamada kullanıladak sabit değerler 
#Bu sayede iki farklı gemini modelinin aynı parametelere göre verdiği tepkileri karşılaşırmış oluyoruz.
TEMPERATURE = 1.0
TOP_P = 0.9
SEED = 42
MAX_OUTPUT_TOKENS = 800

##Promptları JSON dosyasından yükleyen fonksiyon 
def load_prompts() -> list[dict[str, str]]:
    """
    Model karşılaştırmasında kullanılacak promptları
    JSON dosyasından okur.
    """
    ##Okutulacak dosya yoksa hata fırlatır
    if not PROMPTS_FILE.exists():
        raise FileNotFoundError(
            f"Prompt dosyası bulunamadı: {PROMPTS_FILE}"
        )
    #dosyayı açar ve JSON formatında okur
    with PROMPTS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        prompts = json.load(file)
    ##Dosya list formatında değilse veya boşsa hata fırlatır
    if not isinstance(prompts, list):
        raise ValueError(
            "Prompt dosyasının ana yapısı bir JSON listesi olmalıdır."
        )
    #Boş prompt listesi varsa hata fırlatır
    if not prompts:
        raise ValueError(
            "Prompt dosyası boş. En az bir prompt eklenmelidir."
        )
    #İstenen alanlar
    required_fields = {
        "id",
        "category",
        "title",
        "prompt",
    }
    ##Her promptun gerekli alanlara sahip olup olmadığını kontrol eder
    for index, prompt_data in enumerate(prompts):
        missing_fields = (
            required_fields
            - prompt_data.keys()
        )
        #Eğer eksik alanlar varsa hata fırlatır
        if missing_fields:
            raise ValueError(
                f"{index}. promptta eksik alanlar var: "
                f"{sorted(missing_fields)}"
            )

    return prompts

#
def run_experiment(
    prompts: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """
    Her promptu bütün modellere gönderir.

    Model dışında bütün temel üretim ayarları sabit tutulur.
    """

    results: list[dict[str, Any]] = []

    total_requests = len(prompts) * len(MODELS)
    completed_requests = 0

    #Dış döngü promptları, iç döngü ise modelleri iterasyon yapar
    for prompt_data in prompts:
        print("\n" + "=" * 70)
        print(f"GÖREV: {prompt_data['title']}")
        print(f"KATEGORİ: {prompt_data['category']}")
        print("=" * 70)

        for model in MODELS:
            completed_requests += 1

            print(
                f"\n[{completed_requests}/{total_requests}] "
                f"Model çalıştırılıyor: {model}"
            )
            ##API çağrısı süresini ölçmek için zamanlayıcı başlatır
            start_time = perf_counter()

            try:
                answer = generate_text(
                    prompt=prompt_data["prompt"],
                    model=model,
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
                    "experiment": "model_comparison",
                    "model": model,
                    "prompt_id": prompt_data["id"],
                    "prompt_title": prompt_data["title"],
                    "category": prompt_data["category"],
                    "prompt": prompt_data["prompt"],
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
                    "experiment": "model_comparison",
                    "model": model,
                    "prompt_id": prompt_data["id"],
                    "prompt_title": prompt_data["title"],
                    "category": prompt_data["category"],
                    "prompt": prompt_data["prompt"],
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



#Sonuçları JSON dosyasına kaydeden fonksiyon
def save_results(
    results: list[dict[str, Any]],
) -> None:
    """
    Deney sonuçlarını JSON dosyasına kaydeder.
    """

    RESULTS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output = {
        "experiment_name": "Gemini Model Comparison",
        "research_question": (
            "Aynı prompt ve üretim ayarlarında farklı "
            "Gemini modellerinin cevapları nasıl değişir?"
        ),
        "models": MODELS,
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
    print("DENEY TAMAMLANDI")
    print(f"Sonuç dosyası: {RESULTS_FILE}")
    print("=" * 70)


def main() -> None:
    prompts = load_prompts()

    results = run_experiment(prompts)

    save_results(results)


if __name__ == "__main__":
    main()