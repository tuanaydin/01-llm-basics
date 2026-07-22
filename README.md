# 01 — LLM Basics

Bu proje, büyük dil modellerinin temel çalışma mantığını öğrenmek ve farklı model, prompt ve üretim parametrelerinin çıktılar üzerindeki etkisini uygulamalı deneylerle incelemek amacıyla hazırlanmıştır.

Proje kapsamında Gemini API kullanılarak farklı modeller ve farklı prompt yazım biçimleri karşılaştırılmaktadır. İlerleyen aşamada aynı deneylerin Ollama üzerinden yerel modellerle de gerçekleştirilmesi planlanmaktadır.

## Projenin Amaçları

Bu çalışmanın temel amaçları şunlardır:

- Büyük Dil Modeli kavramını anlamak
- Transformer mimarisinin temel çalışma mantığını incelemek
- Token ve tokenization kavramlarını öğrenmek
- Temperature ve Top-P parametrelerinin etkisini gözlemlemek
- Hallucination davranışını incelemek
- Embedding ve text generation arasındaki farkı anlamak
- Farklı modellerin aynı görevlerdeki çıktılarını karşılaştırmak
- Prompt ayrıntı seviyesinin model cevabını nasıl değiştirdiğini gözlemlemek

## İncelenen Konular

- Large Language Models
- Transformer Architecture
- Self-Attention
- Tokens and Tokenization
- Next-Token Prediction
- Temperature
- Top-P
- Hallucination
- Embedding vs Generation
- Prompt Design
- Model Comparison

## Kullanılan Teknolojiler

- Python 3.14
- Gemini API
- Google GenAI Python SDK
- NumPy
- python-dotenv
- Git ve GitHub
- Visual Studio Code

Yerel model deneyleri için ayrıca Ollama kullanılması planlanmaktadır.

## Proje Yapısı

```text
01-llm-basics/
│
├── docs/
│   └── llm-fundamentals.md
│
├── prompts/
│   ├── model_prompts.json
│   └── prompt_variations.json
│
├── results/
│   ├── model_comparison.json
│   ├── model_evaluation.md
│   ├── prompt_comparison.json
│   └── prompt_evaluation.md
│
├── src/
│   ├── __init__.py
│   ├── gemini_client.py
│   ├── list_models.py
│   ├── compare_models.py
│   └── compare_prompts.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

> `.env` dosyası API anahtarı içerdiği için GitHub'a gönderilmez.

## Kurulum

### 1. Repository'yi klonlama

```bash
git clone https://github.com/tuanaydin/01-llm-basics.git
cd 01-llm-basics
```

### 2. Sanal ortam oluşturma

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

PowerShell çalıştırma politikası hatası alınırsa:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

### 3. Bağımlılıkları yükleme

```powershell
python -m pip install -r requirements.txt
```

### 4. Gemini API anahtarını ekleme

Projenin ana dizininde `.env` dosyası oluşturun:

```env
GEMINI_API_KEY=API_ANAHTARINIZ
```

API anahtarını doğrudan Python dosyalarının içine yazmayın.

Anahtarın okunup okunmadığını kontrol etmek için:

```powershell
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(bool(os.getenv('GEMINI_API_KEY')))"
```

Beklenen çıktı:

```text
True
```

## Gemini API Bağlantısını Test Etme

Gemini istemcisini çalıştırmak için:

```powershell
python -m src.gemini_client
```

Bu komut Gemini API'ye örnek bir prompt gönderir ve model cevabını terminalde gösterir.

## Kullanılabilir Modelleri Listeleme

Gemini API anahtarının erişebildiği modelleri görmek için:

```powershell
python -m src.list_models
```

Bu işlem, `generateContent` özelliğini destekleyen Gemini modellerini listeler.

# Deneyler

## Uygulama 1 — Model Karşılaştırması

### Araştırma Sorusu

Aynı prompt ve üretim ayarlarında farklı Gemini modellerinin çıktıları nasıl değişmektedir?

### Karşılaştırılan Modeller

- `gemini-3.5-flash-lite`
- `gemini-3.1-flash-lite`

### Sabit Tutulan Ayarlar

- Temperature: `1.0`
- Top-P: `0.9`
- Seed: `42`
- Maksimum çıktı tokenı: `800`
- System instruction: Her iki model için aynı
- Promptlar: Her iki model için aynı

### Kullanılan Görevler

1. Transformer mimarisini açıklama
2. Python kodu üretme
3. Üç cümlelik bilim kurgu hikâyesi yazma

Deneyi çalıştırmak için:

```powershell
python -m src.compare_models
```

Ham deney sonuçları:

```text
results/model_comparison.json
```

İnsan tarafından yapılan değerlendirme:

```text
results/model_evaluation.md
```

### Temel Bulgular

- Gemini 3.1 Flash Lite, üç görevde de daha düşük yanıt süresi göstermiştir.
- Gemini 3.1 Flash Lite, kod üretimi görevini daha kısa ve tamamlanmış bir cevapla sonuçlandırmıştır.
- Gemini 3.5 Flash Lite, daha ayrıntılı açıklamalar ve daha özgün yaratıcı fikirler üretmiştir.
- Gemini 3.5 Flash Lite'ın kod cevabı maksimum çıktı sınırına ulaştığı için yarıda kesilmiştir.
- Daha uzun bir cevap, her zaman daha kaliteli veya daha eksiksiz bir cevap anlamına gelmemektedir.

## Uygulama 2 — Prompt Karşılaştırması

### Araştırma Sorusu

Aynı görev farklı prompt ayrıntı seviyeleriyle verildiğinde model çıktısı nasıl değişmektedir?

### Kullanılan Model

```text
gemini-3.1-flash-lite
```

### Karşılaştırılan Prompt Türleri

1. Basit prompt
2. Bağlamlı prompt
3. Yapılandırılmış prompt

### Sabit Tutulan Ayarlar

- Model: `gemini-3.1-flash-lite`
- Temperature: `1.0`
- Top-P: `0.9`
- Seed: `42`
- Maksimum çıktı tokenı: `1200`
- System instruction: Her üç prompt için aynı

Deneyi çalıştırmak için:

```powershell
python -m src.compare_prompts
```

Ham deney sonuçları:

```text
results/prompt_comparison.json
```

İnsan tarafından yapılan değerlendirme:

```text
results/prompt_evaluation.md
```

### Temel Bulgular

- Basit prompt geniş kapsamlı ancak daha az kontrollü bir cevap üretmiştir.
- Hedef kitlenin belirtilmesi, cevabın teknik seviyesini artırmıştır.
- Yapılandırılmış prompt, istenen başlıklara ve uzunluk sınırına en iyi şekilde uymuştur.
- Yapılandırılmış prompt en fazla talimatı içermesine rağmen en kısa cevabı üretmiştir.
- Açık kapsam ve çıktı formatı, gereksiz bilgilerin azaltılmasına yardımcı olmuştur.
- Ayrıntılı bir prompt teknik doğruluğu otomatik olarak garanti etmemektedir.

## Deney Sonuçlarının Yorumlanması

Bu projedeki süre ölçümleri aşağıdaki unsurları birlikte içermektedir:

- Modelin cevap üretme süresi
- İnternet bağlantısı
- API sunucusunun yoğunluğu
- Yanıtın istemciye aktarılması

Bu nedenle ölçülen süreler modelin saf hesaplama performansı olarak değerlendirilmemelidir.

Ayrıca deneylerin her biri sınırlı sayıda çalıştırılmıştır. Sonuçlar kapsamlı bir benchmark değil, öğrenme amaçlı kontrollü gözlemlerdir.

## Güvenlik

API anahtarları ve gizli bilgiler GitHub'a gönderilmemelidir.

`.gitignore` dosyasında aşağıdaki kayıtlar bulunmaktadır:

```gitignore
.env
.env.*
.venv/
```

Her commit öncesinde aşağıdaki komutla dosyalar kontrol edilmelidir:

```powershell
git status
```

## Planlanan Çalışmalar

- [x] Gemini API bağlantısı
- [x] Kullanılabilir modellerin listelenmesi
- [x] Farklı modellerin karşılaştırılması
- [x] Farklı promptların karşılaştırılması
- [ ] Temperature deneyi
- [ ] Top-P deneyi
- [ ] Hallucination deneyi
- [ ] Embedding benzerliği deneyi
- [ ] Ollama'nın yeniden test edilmesi
- [ ] Yerel modellerle model karşılaştırması
- [ ] Teknik dokümantasyonun tamamlanması
- [ ] Medium yazısının hazırlanması

## Teknik Dokümantasyon

LLM, Transformer, token, temperature, Top-P, hallucination ve embedding konularının ayrıntılı açıklaması aşağıdaki dokümanda yer alacaktır:

```text
docs/llm-fundamentals.md
```

## Temel Çıkarım

Bu çalışmada elde edilen en önemli sonuç şudur:

> Model çıktısını yalnızca kullanılan model belirlemez. Promptun yapısı, hedef kitlenin tanımlanması, çıktı sınırları ve üretim parametreleri de cevabın doğruluğunu, uzunluğunu, organizasyonunu ve kullanılabilirliğini önemli ölçüde etkiler.