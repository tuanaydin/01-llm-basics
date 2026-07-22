# Gemini Model Karşılaştırması

## 1. Deney Amacı

Bu deneyin amacı, aynı promptlar ve aynı üretim parametreleri
kullanıldığında farklı Gemini modellerinin ürettiği cevapların
nasıl değiştiğini incelemektir.

Karşılaştırılan modeller:

- `gemini-3.5-flash-lite`
- `gemini-3.1-flash-lite`

## 2. Araştırma Sorusu

Aynı prompt ve üretim ayarlarında farklı Gemini modellerinin
teknik doğruluk, açıklık, talimata uyum, yaratıcılık ve yanıt
süresi bakımından çıktıları nasıl değişmektedir?

## 3. Sabit Tutulan Ayarlar

Deneyde model dışındaki temel değişkenler sabit tutulmuştur:

- Temperature: `1.0`
- Top-P: `0.9`
- Seed: `42`
- Maksimum çıktı tokenı: `800`
- System instruction: Her iki model için aynı
- Kullanılan promptlar: Her iki model için aynı

Bu sayede cevaplar arasındaki farkların temel olarak kullanılan
modelden kaynaklanması amaçlanmıştır.

## 4. Kullanılan Görevler

Deneyde üç farklı görev türü kullanılmıştır:

1. Transformer mimarisini açıklama
2. Python kodu üretme
3. Üç cümlelik bilim kurgu hikâyesi yazma

Bu görevlerle modellerin teknik açıklama, kod üretimi, talimat
takibi ve yaratıcı yazım becerileri incelenmiştir.

## 5. Sayısal Sonuçlar

| Görev | Gemini 3.5 Flash Lite | Gemini 3.1 Flash Lite | Daha hızlı model |
|---|---:|---:|---|
| Transformer açıklaması | 2.003 sn | 1.733 sn | Gemini 3.1 |
| Python kodu | 3.539 sn | 2.249 sn | Gemini 3.1 |
| Yaratıcı metin | 1.178 sn | 1.079 sn | Gemini 3.1 |
| Ortalama | 2.240 sn | 1.687 sn | Gemini 3.1 |

Bu deneyde Gemini 3.1 Flash Lite, üç görevin tamamında daha düşük
yanıt süresi göstermiştir.

Ancak ölçülen süre yalnızca modelin hesaplama süresi değildir.
İnternet bağlantısı, API sunucusunun yoğunluğu ve yanıtın
aktarılması da ölçülen toplam süreyi etkileyebilir.

Ayrıca her görev yalnızca bir kez çalıştırıldığı için bu sonuçlar
genel ve kesin bir performans ölçümü olarak değerlendirilmemelidir.

## 6. Transformer Açıklaması

### Gemini 3.5 Flash Lite

Model, Transformer mimarisini günlük bir örnek üzerinden
açıklamıştır. Self-attention, Query, Key ve Value kavramlarına
değinmiş ve banka kelimesi üzerinden bağlam ilişkisini
örneklendirmiştir.

Güçlü yönleri:

- Self-attention kavramını somut bir örnekle açıklamıştır.
- Query, Key ve Value bileşenlerine değinmiştir.
- Öğrenciye uygun ve anlaşılır bir dil kullanmıştır.
- 180 kelimelik sınıra uymuştur.

Zayıf yönleri:

- “RNN'leri tarihe gömen” ifadesi fazla kesin ve iddialıdır.
- “Bağlamı kusursuz yakalayan” ifadesi teknik olarak doğru değildir.
- Transformer'ın bütün tokenları aynı anda işlemesi konusu
  basitleştirilmiş şekilde anlatılmıştır.
- Cevapta küçük bir yazım hatası bulunmaktadır.

### Gemini 3.1 Flash Lite

Model, self-attention yanında positional encoding ve
encoder-decoder yapısına da değinmiştir.

Güçlü yönleri:

- Teknik kapsamı daha geniştir.
- Positional encoding kavramını açıklamıştır.
- Query, Key ve Value bileşenlerine değinmiştir.
- Paralel işlem avantajını belirtmiştir.
- 180 kelimelik sınıra uymuştur.

Zayıf yönleri:

- “Transformer mimarisi encoder-decoder yapısındadır” ifadesi
  bütün Transformer modelleri için geçerli değildir.
- Günümüzde birçok büyük dil modeli decoder-only yapı kullanmaktadır.
- “RNN/LSTM yöntemlerinin yerini alan” ifadesi fazla genel ve
  kesin bir anlatımdır.

### Transformer Görevi Puanları

| Model | Teknik doğruluk | Açıklık | Talimata uyum | Genel puan |
|---|---:|---:|---:|---:|
| Gemini 3.5 Flash Lite | 3.5/5 | 4.5/5 | 5/5 | 4.3/5 |
| Gemini 3.1 Flash Lite | 4/5 | 4.3/5 | 5/5 | 4.4/5 |

Transformer açıklamasında Gemini 3.5 Flash Lite daha somut ve
öğrenci dostu bir anlatım sunarken Gemini 3.1 Flash Lite daha
geniş bir teknik kapsam sağlamıştır.

## 7. Python Kod Üretimi

Her iki model de tekrar eden elemanları bulmak için iki farklı
`set` kullanan bir çözüm üretmiştir.

Temel çalışma mantığı:

1. Daha önce görülen elemanlar bir kümede saklanır.
2. Daha önce görülen bir elemanla tekrar karşılaşılırsa ikinci
   kümeye eklenir.
3. Tekrar eden elemanlar liste olarak döndürülür.

Bu yaklaşımın ortalama zaman karmaşıklığı `O(n)`, alan karmaşıklığı
ise `O(n)` olur.

### Gemini 3.5 Flash Lite

Güçlü yönleri:

- `TypeVar` kullanarak genel bir type hint oluşturmaya çalışmıştır.
- Kodun çalışma mantığını adım adım açıklamıştır.
- Sonuç sırasının değişebileceğini belirtmiştir.
- Tekrar eden her elemanın sonuçta yalnızca bir kez bulunmasını
  sağlamıştır.

Zayıf yönleri:

- Cevap maksimum çıktı tokenı sınırına ulaştığı için yarıda
  kesilmiştir.
- Zaman karmaşıklığı açıklaması tamamlanamamıştır.
- Örnek kullanımda walrus operatörü gereksiz biçimde kullanılmıştır.
- `TypeVar`, elemanların hashlenebilir olması gerektiğini
  belirtmemektedir.
- Fazla ayrıntılı anlatım cevabın tamamlanamamasına neden olmuştur.

### Gemini 3.1 Flash Lite

Güçlü yönleri:

- Kod sade ve doğrudan çalışabilecek yapıdadır.
- Type hint kullanılmıştır.
- Zaman karmaşıklığı doğru şekilde `O(n)` olarak açıklanmıştır.
- Alan karmaşıklığı `O(n)` olarak belirtilmiştir.
- Aynı çıktı sınırı içinde görevin bütün maddeleri tamamlanmıştır.

Zayıf yönleri:

- `List[Any]` oldukça genel bir type hinttir.
- Elemanların hashlenebilir olması gerektiği belirtilmemiştir.
- `set` kullanıldığı için çıktı sırası garanti edilmez.
- “En verimli yol” ifadesi fazla kesin bir ifadedir.

### Kod Görevi Puanları

| Model | Kod doğruluğu | Açıklık | Talimata uyum | Genel puan |
|---|---:|---:|---:|---:|
| Gemini 3.5 Flash Lite | 3.5/5 | 4/5 | 3.5/5 | 3.7/5 |
| Gemini 3.1 Flash Lite | 4.3/5 | 4.5/5 | 5/5 | 4.6/5 |

Kod üretimi görevinde Gemini 3.1 Flash Lite daha başarılıdır.
Gemini 3.5 Flash Lite daha ayrıntılı bir cevap üretmiş ancak cevap
tamamlanamadığı için görevin bütün gereksinimlerini yerine
getirememiştir.

## 8. Yaratıcı Metin

Her iki model de tam olarak üç cümle üretmiş, yapay zekâ ve
elektrik şebekesi temasını korumuştur.

### Gemini 3.5 Flash Lite

Hikâyede yapay zekâ, kıtanın enerjisini dünya dışı varlıklara
gönderilen bir lazer için kullanmıştır.

Güçlü yönleri:

- Daha beklenmedik ve özgün bir fikir üretmiştir.
- Görsel olarak güçlü bir sahne oluşturmuştur.
- Tam olarak üç cümle yazmıştır.
- Bilim kurgu havası belirgindir.

Zayıf yönleri:

- “Yapay zekâ ana sinir ağı” ifadesi doğal olmayan bir kullanım
  olarak değerlendirilebilir.
- Elektrik şebekesinin teknik yönetiminden çok fantastik bir olaya
  odaklanmıştır.

### Gemini 3.1 Flash Lite

Hikâyede merkezi yapay zekâ önce şehir enerjisini optimize etmiş,
sonrasında kaynakları kendi genişlemesi için kullanmaya başlamıştır.

Güçlü yönleri:

- Elektrik şebekesi temasıyla daha doğrudan ilişkilidir.
- Hikâyenin gelişimi daha kontrollü ve tutarlıdır.
- Tam olarak üç cümle yazmıştır.
- Yapay zekânın kontrolü ele geçirmesi teması açıkça işlenmiştir.

Zayıf yönleri:

- Yapay zekânın insanlığı kontrol etmesi teması daha bilinen ve
  daha az özgün bir bilim kurgu fikridir.

### Yaratıcı Metin Puanları

| Model | Tutarlılık | Talimata uyum | Özgünlük | Genel puan |
|---|---:|---:|---:|---:|
| Gemini 3.5 Flash Lite | 4.3/5 | 5/5 | 4.8/5 | 4.7/5 |
| Gemini 3.1 Flash Lite | 4.7/5 | 5/5 | 4.2/5 | 4.6/5 |

Gemini 3.5 Flash Lite daha özgün ve görsel bir hikâye üretirken
Gemini 3.1 Flash Lite daha kontrollü ve elektrik şebekesi
bağlamıyla daha doğrudan ilişkili bir hikâye oluşturmuştur.

## 9. Genel Sonuç

Bu deneyde Gemini 3.1 Flash Lite teknik görevlerde daha kısa,
kontrollü ve tamamlanmış cevaplar üretmiştir. Özellikle kod üretimi
görevinde bütün gereksinimleri aynı çıktı bütçesi içinde yerine
getirmiştir.

Gemini 3.5 Flash Lite ise daha ayrıntılı açıklamalar ve daha özgün
yaratıcı fikirler üretme eğilimi göstermiştir. Bununla birlikte
kod üretimi cevabı gereğinden uzun olduğu için maksimum çıktı
sınırında kesilmiştir.

Yanıt süresi açısından Gemini 3.1 Flash Lite üç görevde de daha
hızlı sonuç vermiştir. Tek çalıştırmaya dayanan ölçümlerde ortalama
yanıt süreleri şu şekildedir:

- Gemini 3.5 Flash Lite: 2.240 saniye
- Gemini 3.1 Flash Lite: 1.687 saniye

Genel olarak:

- Teknik görevler ve kod üretimi için Gemini 3.1 Flash Lite
  daha kontrollü sonuç vermiştir.
- Daha ayrıntılı açıklama ve yaratıcı fikir üretimi için Gemini
  3.5 Flash Lite daha güçlü görünmüştür.
- Daha uzun cevap her zaman daha kaliteli veya daha eksiksiz cevap
  anlamına gelmemektedir.
- Model seçimi yapılırken yalnızca modelin adı değil, görevin türü,
  yanıt süresi, talimata uyum ve çıktı sınırı da değerlendirilmelidir.