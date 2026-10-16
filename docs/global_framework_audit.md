# Küresel Çerçeve Uyum Denetimi

Tarih: 2026-10-10

## Genel sonuç

Proje çerçevesinin ana hattı tez önerisiyle uyumludur: SKAB + Weymouth tabanlı sentetik zaman serisi; SWaT'ın isteğe bağlı tutulması; IF, OCSVM, LOF, LSTM-AE ve GRU-AE; normal-only eğitim; doğrulama-only eşik kalibrasyonu; normal/erken uyarı/kritik alarm; test setinin nihai değerlendirmeye ayrılması; lead time ve SKAB detection delay; RUL kapsam dışı.

Ancak “çerçeve uyumlu” demek, bütün parametrelerin nihai olarak kapandığı anlamına gelmez. Hiperparametre/mimari telafisi eksikti, Weymouth hesapları gerçek `fluids` çağrısıyla henüz doğrulanmadı ve EDA/pilot gerektiren kararlar açık kalmalı. Faz 3'teki başlangıç ZIP'i hesap tarafında GitHub veya Colab kurulmuş olduğunu göstermez.

## Aşamaların gözden geçirilmesi

| Süreç | Uyum durumu | Denetim sonucu |
|---|---|---|
| Faz 0 — tez tasarımı | Uyumlu | Kapsam, araştırma soruları ve RUL dışı sınırı tez önerisiyle tutarlı. |
| Faz 1 — deney protokolü | Büyük ölçüde uyumlu | Eğitim/validasyon/test ayrımı, normal-only eğitim, run/file bazlı bölme, iki eşik ve metrikler ana tasarımla tutarlı. Bazı parametreler literatür sabiti değil tasarım kararı olarak etiketlenmeli. |
| Faz 1.5.9 — hiperparametre/mimari | Önceden tamamlanmamıştı; şimdi aday protokol hazır | `docs/phase1_5_9_hyperparameter_architecture.md`. Nihai kilit Colab pilotundan sonra. |
| Faz 1.5.10–1.5.13 — Weymouth/anomali/alarm | Yöntemsel olarak uyumlu; sayısal doğrulama açık | `fluids` round-trip, basınç/akış fiziksel sınırları ve Zavg varsayımı doğrulanmalı. Anomali etiketleri ve model girdileri ayrılmalı. |
| Faz 2 — yazılım mimarisi | Tam kapanmış değil | Başlangıç paket iskeleti var; bu, `src/` sınırları, test sözleşmesi ve karar kayıtlarının uygulama mimarisinin nihai onayı değildir. Platforma özgü CLAUDE.md/AGENTS.md/skills daha sonra yazılacak. |
| Faz 3 — GitHub + Colab | Henüz çalışma ortamında tamamlanmadı | ZIP hazır; GitHub deposu oluşturma, Colab kurulum, sürüm kaydı, Weymouth sayısal testleri çalıştırılmalı. Faz 1.5.9'un ardından geçilmesi uygundur. |
| Faz 4+ — kodlama/veri/model/deney/tez | Henüz başlanmamalı | Hiperparametre/mimari ve sayısal doğrulama açıkları çözülmeden nihai deneylere geçilmemeli. |

## Önceki denetimdeki dört kritik nokta

1. **Eğitim penceresi normal olmalı.** Tüm W zaman adımları normal etikete sahip olmayan herhangi bir pencere eğitimden çıkarılır. Pencere sonu etiketleme doğrulama/test için kullanılır. Test: pencere oluşturma ve etiketleme birim testleri.
2. **Model skor yönü birleştirilmeli.** IF, OCSVM ve LOF ham skor API'lerinin yönü birbirinden farklı olabilir; tek adaptör `higher = more anomalous` sözleşmesi verir. AE skoru MSE'dir. Test: sentetik sıralı skor ve API yön testleri.
3. **Weymouth sayısal doğrulaması yapılmalı.** Sabit `Zavg=0.8065` v1 politikası seçildi; `OPEN-DECISION-012` Colab çağrısı, nominal geri çözüm, birimler, akış monotonluğu ve iki segmentin kütle dengesi doğrulanana kadar açık kalır.
4. **İkili eşik yöntemi sabit.** Doğrulama F1 maksimize edilir; eşitlikte Recall, sonra normal doğrulama FPR kullanılır. Test skor/etiketleri eşik seçimine katılmaz. Üç sınıf için ayrı, önceden belirtilen Macro-F1 protokolü sürer.

## Tasarım kararı ile literatür değerini ayırma

- Weymouth boru boyu/çap/basınç ve gaz özellikleri literatür destekli baseline olarak tanımlanmıştır; bunlar gerçek bir BOTAŞ hattı ölçümü değildir.
- 30/10/10 bağımsız normal simülasyon koşusu bölmesi ve anomali koşulu başına 10 doğrulama + 10 test koşusu, pratik tasarım seçimleridir; evrensel optimum veya literatürün zorunlu kıldığı oranlar değildir.
- 15 dakikalık örnekleme, 24 saatlik koşu, ±%5 normal talep dalgalanması ve kademeli anomalilerin 6 saatlik rampası tasarım varsayımlarıdır; saha verisi iddiası değildir.
- Penceredeki beş klasik özellik (ortalama, standart sapma, minimum, maksimum, doğrusal eğim) yorumlanabilir başlangıç tasarımıdır; değişkenler EDA'dan sonra seçilir.
- Ölçüm gürültüsü, model girdisindeki akış temsili ve sensör seçimi için kararlar kanıt gelene kadar açık kalır.

## Yeni açık karar

### OPEN-DECISION-020: W=16 pencere uzunluğunun uygunluğu — 🔴 SUPERSEDED (historical entry)
- Neden açık: 15 dakikalık örneklemede W=16 yaklaşık 4 saatlik bağlam verir. Weymouth normal talep varyasyonu 24 saatlik profile bağlıdır. Malhotra ve ark. (2016) LSTM encoder-decoder çalışmalarında 30–500 adım örneklemiştir; bu farklı veri ve örnekleme bağlamları nedeniyle doğrudan eşik değildir, fakat W=16 için doğrudan literatür gerekçesinin zayıf olduğunu gösterir.
- Ne zaman kapanacak: Colab'da Weymouth üretimi ve bir model pilotu çalıştıktan sonra, nihai hiperparametreler/deneyler başlamadan önce.
- Güncel sonuç: Kullanıcının onaylı nihai çerçevesi W=16'yı baseline olarak kilitledi; W=32 karşılaştırması iptal edildi. Bu tarihsel öneri aktif protokol değildir.

## Faz sırası önerisi

1. **Faz 1.5.9** — literatür tabanlı aday hiperparametre ve mimari protokolü (şimdi).
2. **Faz 2 — kısa mimari geçiş kontrolü** — mevcut scaffold'ın klasör/modül sınırlarını, konfigürasyon sahipliğini, test sözleşmelerini ve notebook-kaynak-kod ayrımını onayla. CLAUDE.md/AGENTS.md/platform skill dosyaları henüz yazılmayacak; bunlar proje planında daha sonraki ayrı iş paketidir.
3. **Faz 3 — GitHub/Colab** — depoyu hesapta oluştur, kurulum ve sürüm manifestini doğrula, `fluids` gerçek çağrılarıyla Weymouth smoke testini çalıştır.
4. **Pilot ve karar kapanışları** — OPEN-DECISION-007/008/009/012/020 gibi pilot veya çalışma ortamı kanıtı isteyen kayıtları yalnızca kapanış koşulları sağlandığında güncelle.
5. Ardından veri pipeline, simülasyon/anomali enjeksiyonu, modeller, değerlendirme ve deney fazlarına geç.

Bu sıra, kullanıcının istediği gibi hiperparametre/mimari kararları önce netleştirir; aynı zamanda resmi yol haritasındaki Faz 2 → Faz 3 sırasını korur. Mevcut ZIP yalnızca scaffold sağlar; mimari geçiş kontrolünün veya GitHub/Colab hesabı kurulumunun tamamlandığı anlamına gelmez. Tez yazımına geçmeden önce bütün kararların GLOBAL FINAL DECISION AUDIT'i yapılmalı ve Methodology Baseline v1.0 çıkarılmalıdır.
