# Gemini Prompt Karşılaştırması

## 1. Deney Amacı

Bu deneyin amacı, aynı görev farklı ayrıntı ve yapı seviyelerine
sahip promptlarla verildiğinde model çıktısının nasıl değiştiğini
incelemektir.

Deneyde kullanılan model:

- `gemini-3.1-flash-lite`

Karşılaştırılan prompt türleri:

1. Basit prompt
2. Bağlamlı prompt
3. Yapılandırılmış prompt

## 2. Araştırma Sorusu

Aynı görev basit, bağlamlı ve yapılandırılmış promptlarla
verildiğinde modelin teknik doğruluk, hedef kitleye uygunluk,
cevap organizasyonu, talimata uyum ve çıktı uzunluğu bakımından
ürettiği cevaplar nasıl değişmektedir?

## 3. Deney Tasarımı

Deney boyunca aşağıdaki değişkenler sabit tutulmuştur:

- Model: `gemini-3.1-flash-lite`
- Temperature: `1.0`
- Top-P: `0.9`
- Seed: `42`
- Maksimum çıktı tokenı: `1200`
- System instruction: Her üç prompt için aynı

Deneyde yalnızca kullanıcı promptunun ayrıntı ve yapı seviyesi
değiştirilmiştir.

Ortak system instruction kullanıldığı için basit prompt da tamamen
bağlamsız değildir. Model her üç çalıştırmada teknik, anlaşılır ve
Türkçe cevap üretmesi gerektiğini önceden bilmektedir.

## 4. Kullanılan Promptlar

### Basit Prompt

> LLM'leri anlat.

Bu promptta hedef kitle, cevap uzunluğu, konu kapsamı ve çıktı
formatı belirtilmemiştir.

### Bağlamlı Prompt

> LLM'lerin çalışma mantığını, temel makine öğrenmesi bilgisi olan
> bir bilgisayar mühendisliği öğrencisine açıkla.

Bu promptta görev ve hedef kitle tanımlanmış ancak cevap formatı
serbest bırakılmıştır.

### Yapılandırılmış Prompt

Yapılandırılmış promptta rol, hedef kitle, anlatılması gereken
başlıklar, maksimum uzunluk ve cevap üretiminde dikkat edilmesi
gereken kurallar belirtilmiştir.

## 5. Sayısal Sonuçlar

| Prompt | Karakter sayısı | Yaklaşık kelime sayısı | Yanıt süresi |
|---|---:|---:|---:|
| Basit | 3206 | 396 | 4.368 sn |
| Bağlamlı | 3393 | 406 | 4.392 sn |
| Yapılandırılmış | 2988 | 357 | 3.825 sn |

Yapılandırılmış prompt, en fazla talimat içermesine rağmen en kısa
cevabı ve en düşük yanıt süresini üretmiştir. Bu sonuç, ayrıntılı
bir promptun mutlaka daha uzun cevap anlamına gelmediğini
göstermektedir. Açık kapsam ve format talimatları gereksiz
bölümlerin azaltılmasına yardımcı olmuştur.

Yanıt süreleri internet bağlantısı ve API yoğunluğundan
etkilenebileceği için kesin model performansı olarak
yorumlanmamalıdır.

## 6. Basit Prompt Değerlendirmesi

Basit prompt sonucunda model, LLM tanımı, çalışma mantığı,
Transformer mimarisi, eğitim süreci, kullanım alanları ve
sınırlamalar içeren geniş kapsamlı bir cevap üretmiştir.

### Güçlü Yönler

- Yeni başlayan biri için anlaşılır bir dil kullanılmıştır.
- Cevap başlıklarla düzenlenmiştir.
- Next-token prediction ve Transformer kavramlarına değinilmiştir.
- Hallucination gibi önemli bir sınırlama açıklanmıştır.

### Zayıf Yönler

- Hedef kitle belirtilmediği için teknik seviye model tarafından
  belirlenmiştir.
- Kullanıcının özellikle istemediği ek konulara girilmiştir.
- Fine-tuning ile RLHF süreçleri birbirine fazla yakın
  anlatılmıştır.
- “Tüm internet” ve “en mantıklı yanıt” gibi fazla genelleyici
  ifadeler kullanılmıştır.

Basit prompt okunabilir bir cevap oluşturmuş ancak çıktı kapsamı
üzerindeki kontrol sınırlı kalmıştır.

## 7. Bağlamlı Prompt Değerlendirmesi

Hedef kitlenin bilgisayar mühendisliği öğrencisi olarak
belirtilmesi, cevabın teknik seviyesini artırmıştır.

### Güçlü Yönler

- Otoregresif üretim ve next-token prediction açıklanmıştır.
- Self-attention formülü gösterilmiştir.
- Query, Key, Value ve positional encoding kavramlarına
  değinilmiştir.
- Pre-training, SFT ve RLHF aşamaları açıklanmıştır.
- Cevap hedef kitlenin teknik bilgisine uygun hazırlanmıştır.

### Zayıf Yönler

- Kelimelerin gizlenerek tahmin edilmesi bütün üretken LLM'lerin
  temel eğitim yöntemi gibi anlatılmıştır. Otoregresif modellerde
  temel görev önceki tokenlardan sonraki tokenı tahmin etmektir.
- Bütün LLM'lerin PPO tabanlı RLHF sürecinden geçtiği izlenimi
  oluşturulmuştur.
- Beliren özelliklerin yalnızca parametre sayısındaki belirli bir
  eşikle oluştuğu fazla kesin şekilde ifade edilmiştir.
- Cevap bazı bölümlerde gerekli olandan daha ayrıntılıdır.

Bağlamlı prompt, hedef kitleye en uygun teknik cevabı üretmiştir;
ancak bazı teknik genellemeler içermektedir.

## 8. Yapılandırılmış Prompt Değerlendirmesi

Yapılandırılmış promptta modelden belirli başlıklar, bir örnek,
üç çıkarım ve maksimum 500 kelimelik bir cevap istenmiştir.

### Güçlü Yönler

- İstenen altı bölümün tamamı oluşturulmuştur.
- Maksimum 500 kelime sınırına uyulmuştur.
- Teknik terimler büyük ölçüde ilk kullanıldıkları yerde
  açıklanmıştır.
- Tokenization, embedding, next-token prediction ve Transformer
  ilişkisi sistematik biçimde anlatılmıştır.
- Cevap diğerlerinden daha kısa ve odaklıdır.
- Tam olarak üç temel çıkarım sunulmuştur.

### Zayıf Yönler

- Tokenization örneği gerçek tokenizer çıktısı gibi
  yorumlanmamalıdır; ayrım kullanılan modele göre değişebilir.
- Modelin her zaman en yüksek olasılıklı tokenı seçtiği izlenimi
  verilmiştir. Sampling parametreleri kullanıldığında farklı
  tokenlar da seçilebilir.
- Örnekte verilen yüzde değerleri varsayımsaldır ancak bu durum
  açıkça belirtilmemiştir.
- “Kusursuz şekilde modellemek” ifadesi fazla kesin bir ifadedir.

Yapılandırılmış prompt, format kontrolü ve konu kapsamı bakımından
en başarılı cevap olmuştur.

## 9. Değerlendirme Tablosu

Puanlama:

- 1: Çok yetersiz
- 2: Yetersiz
- 3: Orta
- 4: İyi
- 5: Çok iyi

| Ölçüt | Basit | Bağlamlı | Yapılandırılmış |
|---|---:|---:|---:|
| Teknik doğruluk | 3.7 | 3.6 | 4.1 |
| Hedef kitleye uygunluk | 3.3 | 4.8 | 4.8 |
| Cevap organizasyonu | 4.0 | 4.5 | 5.0 |
| Konu kapsamının kontrolü | 3.2 | 4.2 | 5.0 |
| Talimata uyum | 3.5 | 4.5 | 5.0 |
| Okunabilirlik | 4.4 | 4.2 | 4.6 |
| Genel değerlendirme | 3.7 | 4.3 | 4.8 |

## 10. Genel Sonuç

Basit prompt, modelin geniş kapsamlı ve okunabilir bir cevap
üretebildiğini göstermiştir. Ancak hedef kitle, uzunluk ve kapsam
belirtilmediğinden model hangi konulara değineceğine kendisi karar
vermiş ve bazı gereksiz bölümler eklemiştir.

Bağlamlı promptta hedef kitlenin belirtilmesi, kullanılan teknik
terimlerin ve matematiksel ayrıntıların artmasını sağlamıştır.
Cevap bilgisayar mühendisliği öğrencisine daha uygun hâle gelmiş,
ancak format ve kapsam hâlâ büyük ölçüde model tarafından
belirlenmiştir.

Yapılandırılmış prompt, istenen başlıkların tamamını içeren,
maksimum uzunluk sınırına uyan ve diğer cevaplardan daha kısa bir
çıktı üretmiştir. Bu deneyde rol, hedef kitle, konu başlıkları,
uzunluk sınırı ve çıktı formatının açıkça belirtilmesi model
çıktısının kontrol edilebilirliğini artırmıştır.

Deneyin temel çıkarımı şudur:

> İyi bir prompt yalnızca daha fazla kelime içeren prompt değildir.
> Görevi, hedef kitleyi, gerekli kapsamı, sınırları ve çıktı
> formatını açık biçimde tanımlayan prompttur.

Bununla birlikte yapılandırılmış bir prompt teknik doğruluğu
otomatik olarak garanti etmez. Model, ayrıntılı talimatlara uysa
bile hatalı, fazla kesin veya varsayımsal bilgiler üretebilir.
Bu nedenle çıktıların ayrıca değerlendirilmesi ve doğrulanması
gerekir.