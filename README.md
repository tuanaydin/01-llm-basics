# 01 — LLM Basics

Bu proje, büyük dil modellerinin temel çalışma mantığını öğrenmek ve farklı model, prompt ve üretim ayarlarının çıktılar üzerindeki etkisini uygulamalı deneylerle incelemek amacıyla hazırlanmıştır.

Projede Gemini API kullanılarak model karşılaştırması, prompt karşılaştırması, factuality hallucination ve faithfulness hallucination deneyleri gerçekleştirilmiştir. Temperature ve Top-P deneylerinin ise Ollama üzerinden yerel modellerle yapılması planlanmaktadır.

## Projenin Amaçları

Bu çalışmanın temel amaçları şunlardır:

- Büyük Dil Modeli kavramını anlamak
- Transformer mimarisinin temel çalışma mantığını incelemek
- Token ve tokenization kavramlarını öğrenmek
- Farklı modellerin aynı görevlerdeki çıktılarını karşılaştırmak
- Prompt ayrıntı seviyesinin model cevabını nasıl değiştirdiğini gözlemlemek
- Factuality ve faithfulness hallucination davranışlarını incelemek
- Temperature ve Top-P parametrelerinin etkisini gözlemlemek
- Embedding ve text generation arasındaki farkı anlamak
- Model çıktılarının yalnızca akıcılık açısından değil, doğruluk ve talimata uyum açısından da değerlendirilmesini sağlamak

## İncelenen Konular

- Large Language Models
- Transformer Architecture
- Self-Attention
- Query, Key ve Value
- Tokens and Tokenization
- Next-Token Prediction
- Temperature
- Top-P
- Factuality Hallucination
- Faithfulness Hallucination
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

Yerel model deneyleri için Ollama da kurulmuştur. İlk çalıştırma denemesinde Windows üzerinde `llama-server` süreci hata verdiği için Ollama deneylerinin proje sonunda yeniden ele alınması planlanmaktadır.

## Proje Yapısı

```text
01-llm-basics/
│
├── docs/
│   └── llm-fundamentals.md
│
├── prompts/
│   ├── model_prompts.json
│   ├── prompt_variations.json
│   └── hallucination_prompts.json
│
├── results/
│   ├── model_comparison.json
│   ├── model_evaluation.md
│   ├── prompt_comparison.json
│   ├── prompt_evaluation.md
│   ├── hallucination_results.json
│   └── hallucination_evaluation.md
│
├── src/
│   ├── __init__.py
│   ├── gemini_client.py
│   ├── list_models.py
│   ├── compare_models.py
│   ├── compare_prompts.py
│   └── hallucination_test.py
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

Windows PowerShell:

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
- Daha uzun bir cevap her zaman daha kaliteli veya daha eksiksiz bir cevap anlamına gelmemektedir.

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
- Hedef kitlenin belirtilmesi cevabın teknik seviyesini artırmıştır.
- Yapılandırılmış prompt istenen başlıklara ve uzunluk sınırına en iyi şekilde uymuştur.
- Yapılandırılmış prompt en fazla talimatı içermesine rağmen en kısa cevabı üretmiştir.
- Açık kapsam ve çıktı formatı gereksiz bilgilerin azaltılmasına yardımcı olmuştur.
- Ayrıntılı bir prompt teknik doğruluğu otomatik olarak garanti etmemektedir.

## Uygulama 3 — Hallucination Deneyi

### Araştırma Soruları

- Model, gerçek olmayan bir kavram hakkında kişi, tarih veya kaynak uyduruyor mu?
- Belirsizliği açıkça belirtmesini isteyen bir prompt cevabı nasıl etkiliyor?
- Model, verilen bağlamda bulunmayan bilgileri cevaba ekliyor mu?
- Cevaplanamayan bir soruda bilgi eksikliğini kabul ediyor mu?

### Kullanılan Model

```text
gemini-3.1-flash-lite
```

### Sabit Tutulan Ayarlar

- Temperature: `1.0`
- Top-P: `0.9`
- Seed: `42`
- Maksimum çıktı tokenı: `600`
- System instruction: Dört test için aynı

### Uygulanan Testler

1. Korumasız uydurma kavram sorusu
2. Korumalı uydurma kavram sorusu
3. Bağlamdan cevaplanabilen soru
4. Bağlamdan cevaplanamayan soru

Deneyi çalıştırmak için:

```powershell
python -m src.hallucination_test
```

Ham deney sonuçları:

```text
results/hallucination_results.json
```

İnsan tarafından yapılan değerlendirme:

```text
results/hallucination_evaluation.md
```

### Sayısal Sonuçlar

| Test | Karakter sayısı | Yanıt süresi |
|---|---:|---:|
| Korumasız uydurma kavram | 804 | 1.468 sn |
| Korumalı uydurma kavram | 465 | 0.892 sn |
| Bağlamdan cevaplanabilen soru | 73 | 0.480 sn |
| Bağlamdan cevaplanamayan soru | 37 | 0.461 sn |

### Temel Bulgular

- Model, uydurma algoritma için geliştirici adı, yayın yılı veya makale başlığı üretmemiştir.
- Korumalı prompt daha kısa ve doğrudan bir cevap üretmiştir.
- Model bağlamdan cevaplanabilen soruya doğru cevap vermiştir.
- Bağlamda bulunmayan üniversite bilgisini uydurmamıştır.
- Cevaplanamayan soruda bilginin verilen bağlamda bulunmadığını açıkça belirtmiştir.
- Testlerin hiçbirinde doğrudan kişi, tarih veya kaynak uydurulmamıştır.
- Model bazı cevaplarda kavramın kesinlikle var olmadığını söyleyerek gereğinden fazla kesin konuşmuştur.
- “Bu bilgiyi doğrulayamıyorum” ile “bu bilgi kesinlikle yoktur” ifadelerinin aynı olmadığı gözlemlenmiştir.

### Deney Sınırlaması

Bütün testlerde aşağıdaki ortak system instruction kullanılmıştır:

```text
Bilmediğin veya doğrulayamadığın bilgileri uydurma.
Verilen bir bağlam varsa yalnızca o bağlama dayan.
```

Bu nedenle korumasız olarak adlandırılan ilk test tamamen korumasız değildir. Ortak sistem talimatı modelin bilgi uydurma davranışını azaltmış olabilir.

Ayrıca her prompt yalnızca bir kez çalıştırılmıştır. Bu nedenle sonuçlar genel bir hallucination oranı veya kapsamlı bir model benchmark'ı olarak değerlendirilmemelidir.

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

`.gitignore` dosyasında aşağıdaki kayıtların bulunması önerilir:

```gitignore
.env
.env.*
.venv/
__pycache__/
*.py[cod]
```

Her commit öncesinde aşağıdaki komutla dosyalar kontrol edilmelidir:

```powershell
git status
```

`.env` ve `.venv` klasörlerinin Git tarafından izlenmediğinden emin olunmalıdır.

## Proje Durumu

- [x] Proje ve sanal ortam kurulumu
- [x] Gemini API bağlantısı
- [x] Kullanılabilir modellerin listelenmesi
- [x] Farklı modellerin karşılaştırılması
- [x] Model çıktılarının manuel değerlendirilmesi
- [x] Farklı promptların karşılaştırılması
- [x] Prompt çıktılarının manuel değerlendirilmesi
- [x] Factuality hallucination deneyi
- [x] Faithfulness hallucination deneyi
- [x] Hallucination sonuçlarının manuel değerlendirilmesi
- [ ] Embedding benzerliği deneyi
- [ ] Ollama'nın yeniden test edilmesi
- [ ] Temperature deneyi
- [ ] Top-P deneyi
- [ ] Yerel modellerle model karşılaştırması
- [ ] Deneylerin genel özetinin hazırlanması
- [ ] Teknik dokümantasyonun tamamlanması
- [ ] Medium yazısının hazırlanması

## Planlanan Çalışmalar

### Embedding Benzerliği Deneyi

Anlamsal olarak birbirine yakın ve uzak cümleler embedding vektörlerine dönüştürülecek ve cosine similarity yöntemiyle karşılaştırılacaktır.

### Ollama'nın Yeniden Test Edilmesi

Ollama ile yerel model çalıştırılırken alınan Windows `llama-server` hatası yeniden incelenecektir.

Kontrol edilmesi planlanan noktalar:

- CPU üzerinde çalıştırma
- Daha küçük veya farklı bir model kullanma
- Quantization seçimi
- Ollama loglarını inceleme
- Donanım hızlandırma ayarlarını kontrol etme

### Temperature ve Top-P Deneyleri

Yerel model çalıştırıldıktan sonra:

- Model sabit tutulacak
- Prompt sabit tutulacak
- Temperature değerleri ayrı ayrı değiştirilecek
- Top-P değerleri ayrı ayrı değiştirilecek
- Her değer birden fazla kez çalıştırılacak
- Çıktıların çeşitlilik, tutarlılık ve tekrar edilebilirlik özellikleri incelenecek

## Teknik Dokümantasyon

LLM, Transformer, token, temperature, Top-P, hallucination ve embedding konularının ayrıntılı açıklaması aşağıdaki dokümanda yer alacaktır:

```text
docs/llm-fundamentals.md
```

## Temel Çıkarımlar

1. Aynı prompt farklı modellerde farklı uzunluk, hız ve kalite düzeylerinde cevaplar üretmektedir.
2. Hedef kitle ve çıktı formatının belirtilmesi model cevabını daha kontrol edilebilir hâle getirmektedir.
3. Daha uzun veya ayrıntılı bir cevap her zaman daha kaliteli değildir.
4. Yapılandırılmış promptlar gereksiz içeriği azaltabilir.
5. Ayrıntılı bir prompt teknik doğruluğu otomatik olarak garanti etmez.
6. Modelin bilgi uydurmaması, bütün ifadelerinin doğrulanmış olduğu anlamına gelmez.
7. “Doğrulayamıyorum” ile “kesinlikle yoktur” ifadeleri birbirinden ayrılmalıdır.
8. Bağlamda bulunmayan bilgiler için açık bir başarısızlık cevabı tanımlamak faithfulness hallucination riskini azaltabilir.
9. Akıcı ve ikna edici bir cevap otomatik olarak doğru ve güvenilir değildir.
10. Tek çalıştırmalı deneyler kapsamlı bir benchmark olarak değerlendirilmemelidir.

## Genel Sonuç

Bu çalışmada elde edilen temel sonuç şudur:

> Model çıktısını yalnızca kullanılan model belirlemez. Promptun yapısı, hedef kitlenin tanımlanması, çıktı sınırları, sistem talimatları ve üretim parametreleri de cevabın doğruluğunu, uzunluğunu, organizasyonunu ve kullanılabilirliğini önemli ölçüde etkiler.