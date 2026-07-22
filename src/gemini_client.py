from __future__ import annotations

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

##Bu satır proje klasöründeki .env dosyasını okur.
# Proje kökündeki .env dosyasını yükler.
load_dotenv()

# .env içindeki GEMINI_API_KEY değerini okur.
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY bulunamadı. "
        ".env dosyasını ve değişken adını kontrol edin."
    )


# Gemini API istemcisini oluşturur. Gemini ile iletişim
client = genai.Client(api_key=API_KEY)

####Burada:

#model: Hangi Gemini modelinin kullanılacağını,
#contents: Kullanıcı promptunu,
#config: Üretim ayarlarını belirler.
def generate_text(
    prompt: str,
    *,
    model: str = "gemini-3.1-flash-lite",
    system_instruction: str | None = None,
    temperature: float = 0.2,
    top_p: float = 0.9,
    seed: int = 42,
    max_output_tokens: int = 300,
) -> str:
    """
    Gemini API'ye prompt gönderir ve üretilen metni döndürür.

    Args:
        prompt:
            Kullanıcı tarafından gönderilecek metin.

        model:
            Kullanılacak Gemini modelinin adı.

        system_instruction:
            Modelin genel davranışını belirleyen sistem talimatı.

        temperature:
            Token seçimindeki çeşitlilik düzeyi.

        top_p:
            Token seçiminde kullanılacak olasılık havuzu.

        seed:
            Deneylerin daha tekrarlanabilir olmasına yardımcı olan değer.

        max_output_tokens:
            Üretilebilecek maksimum çıktı tokenı.

    Returns:
        Modelin ürettiği metin.
    """

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
            top_p=top_p,
            seed=seed,
            max_output_tokens=max_output_tokens,
        ),
    )

    if not response.text:
        raise RuntimeError(
            "Gemini boş bir cevap döndürdü."
        )

    return response.text.strip()


def main() -> None:
    prompt = "LLM nedir? İki cümleyle Türkçe açıkla."

    answer = generate_text(
        prompt=prompt,
        system_instruction=(
            "Teknik kavramları doğru, sade ve Türkçe olarak açıklayan "
            "bir yapay zekâ eğitmenisin."
        ),
        temperature=0.2,
        top_p=0.9,
        seed=42,
        max_output_tokens=200,
    )

    print("Gönderilen prompt:")
    print(prompt)

    print("\nGemini cevabı:")
    print(answer)


if __name__ == "__main__":
    main()