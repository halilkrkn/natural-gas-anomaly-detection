# FAZ C — Kısa Mimari Kontrol Kaydı

**Durum:** Mimari karar önerisi tamamlandı; uygulama kodu ve Antigravity/skill paketi üretilmedi veya güncellenmedi. Faz 3 ve Antigravity nihai geçiş kapısı kapalıdır.

## 1. Mimari ilkeler

- Basit Python modülleri ve fonksiyonları; ihtiyaç yoksa ek framework, genel pipeline sınıfları veya derin kalıtım yok.
- Yeniden kullanılabilir bilimsel mantık `src/natural_gas_anomaly_detection/` altında.
- Notebook'lar EDA, deney akışı ve görselleştirme için orkestrasyon katmanıdır; yeniden kullanılabilir algoritmalar notebook'larda çoğaltılmaz.
- Bilimsel parametrelerin gerekçesi/durumu `docs/decision_register.md` içinde tutulur. `configs/` çalıştırılabilir değerleri taşır; config'te sayı bulunması kararı kapatmaz.
- Test/Colab kanıtı olmadan kurulum, simülasyon veya model başarısı iddiası yapılmaz.

## 2. Modül sınırları

| Modül | Sorumluluk | İçermemesi gerekenler |
|---|---|---|
| `data/` | SKAB yükleme, ortak veri şeması, run/file manifesti, veri kalite kontrolleri ve split ataması | Model eğitimi, eşik seçimi |
| `preprocessing/` | Eksik veri işlemleri, scaler fit/transform, nedensel pencere üretimi | Anomali skorları, fiziksel sızıntı denklemleri |
| `simulation/` | Talep profili ve `fluids.compressible.Weymouth` adapter'ı ile quasi-steady fiziksel koşu üretimi | Weymouth denklemini elde yeniden kodlama, ML karar eşiği |
| `anomaly/` | Senaryo manifestine uygun sensör bias/drift dönüşümleri ve zaman etiketleri | `Q_leak` gibi gerçek senaryo bilgisini model girdisine sızdırma |
| `features/` | Klasik modeller için sensör/pencere başına mean, std, min, max, slope | Deep modelin ham dizi girdisini istatistik özelliklere dönüştürme |
| `models/classical/` | IF, OCSVM, LOF wrapper'ları | Veri bölme, eşik optimizasyonu, rapor üretimi |
| `models/deep_learning/` | LSTM-AE, GRU-AE, ortak ve sade eğitim/rekonstrüksiyon fonksiyonları | Teste göre erken durdurma veya mimari seçimi |
| `evaluation/` | Ortak skor yönü, validation-only eşik kalibrasyonu, metrikler, run-level lead-time özeti | Model fit etme veya ayar değiştirme |
| `visualization/` | Önceden hesaplanan sonuçların grafikleri | Metrik hesaplarını gizlice yeniden uygulama |

**Küçük sınır düzeltmesi:** Mevcut mimari notunda pencere oluşturma `features/` ile aynı sorumlulukta anılıyor. Daha açık sınır için pencere oluşturma `preprocessing/windowing.py`, beş istatistiğin çıkarılması `features/window_statistics.py` altında olmalı. Yeni bir üst-seviye `windowing` paketi açmaya gerek yok.

## 3. Konfigürasyonların tek sorumluluğu

- `configs/data.yaml`: veri kaynağı, örnekleme aralığı, W=16, stride=1, sensör seçimi ve eksik veri ayarları.
- `configs/simulation.yaml`: boru ve gaz parametreleri, talep profili, fiziksel senaryo, ölçüm gürültüsü ve birimler.
- `configs/models.yaml`: model hiperparametre adayları ve teknik eğitim ayarları.
- `configs/experiments.yaml`: split protokolü, seed/repeat, threshold yöntemi, metrikler ve deney kimliği.
- Gizli bilgiler ve kullanıcıya özgü Drive yolları config dosyalarına gömülmez; ortam değişkeni veya yerel ve Git dışında kalan ayar kullanılır.
- Kaynak, kaynak bağlamı, kanıt sınıfı, gerekçe, durum ve kapanış kanıtı karar defterinin sorumluluğudur; bilimsel gerekçe birden fazla dosyada kopyalanıp birbirinden bağımsız değiştirilmeyecek.

## 4. Veri akışı için mimari kural

1. SKAB'da önce tüm deney/dosya birimi tek bir split'e atanır; sonra o split içinde pencereleme yapılır.
2. Sentetik veride bağımsız run ID, split ve senaryo dağılımı veriye bakılmadan manifestte önceden belirlenir.
3. Fiziksel sızıntı senaryosu, temiz basınç eğrisine keyfî offset eklemek değildir: senaryo atanmış run, iki segmentli `fluids` Weymouth çözümüyle fiziksel olarak yeniden üretilir. Sensör bias/drift ise fiziksel sistem normal kalırken ölçüm katmanına uygulanır.
4. Aynı run iki split arasında bölünmez. Pencereler split/run sınırını aşmaz. W=16, 96 noktalı bir koşuda tam seri üzerinde 81 pencere üretir.
5. Klasik yol: split → nedensel pencereler → mean/std/min/max/slope → scaler yalnızca normal train feature matrisi üzerinde fit → model.
6. Derin yol: split → scaler yalnızca normal train ham sensör değerlerine fit → transform → nedensel W=16 pencereler → model.
7. Model wrapper'larının ortak dış sözleşmesi: `fit(X_train_normal)` ve `score_anomaly(X) -> 1D array`; dış skorun yüksek olması daha anormal davranış demektir. Eşik kalibrasyonu ayrı `evaluation/` sorumluluğudur.

## 5. Test sınırı

### Unit test
- Pencere uzunluğu/stride/şekil, window-end index ve split/run sınırının aşılmaması.
- Eğitim pencerelerinin tüm noktalarının normal olması.
- Mean/std/min/max/slope için elle hesaplanabilir küçük örnekler.
- Scaler fit'ine yalnızca normal train örneklerinin girdiğinin doğrulanması.
- IF/OCSVM/LOF skor işaret dönüşümü, skor boyutu ve NaN/Inf kontrolü.
- Binary ve üç sınıflı eşik kısıtları (`T1 < T2`) ve eşitlik bozma sırası.
- Senaryo zaman çizelgesi, bias/drift büyüklüğü ve normal zaman aralığının etiketi.

### Integration test
- Gerçek `fluids.compressible.Weymouth` çağrısıyla nominal Q/P2 geri çözümü ve SI/referans koşulu kontrolleri.
- İki segmentli sızıntı senaryosunda akış kütle dengesi; fiziksel basınçların geçerliliği.
- Manifestten tam bir sentetik koşu oluşturma ve beklenen şema/etiketleri üretme.
- Her modelin küçük örnek üzerinde fit/score arayüzünü ve çıktı boyutunu doğrulama.

### Smoke test
- Çok küçük sentetik örnek ve sınırlı epoch ile beş modelin uçtan uca kablolamasını kontrol etme.
- Tam 170 koşuluk benchmark'ı, tüm seed tekrarlarını veya geniş tarama setini çalıştırmaz.

### Deney/araştırma denetimi
- Run-level bağımsızlık; sabit split manifesti; config snapshot; seed; paket sürümleri; train/validation/test ayrımı; threshold'un yalnızca validation'da seçildiği; test sonrasında ayar değiştirilmediği kaydedilir.
- Pencere seviyesinde örtüşen örnekler bağımsız istatistiksel deney gibi sayılmaz; sonuçlar run-level özetlerle desteklenir.

## 6. Mevcut taslak pakette saptanan tutarsızlıklar

Bu dosya bir platform paketi değildir. Aşağıdakiler mevcut ZIP taslağında saptandı; sessizce değiştirilmediler:

1. `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `configs/data.yaml`, `docs/thesis_method_contract.md` ve `docs/decision_register.md` hâlâ OPEN-DECISION-020/W=32 kontrolünü aktif gösteriyor. Kullanıcının kabul ettiği güncel çerçevede W=16 kilitli baseline; W=32 aktif deney değil. Eski öneri `SUPERSEDED` olarak işaretlenmeli ve etkin kurallardan kaldırılmalı.
2. Taslaktaki `configs/models.yaml` eski parametre değerleri taşıyor: `hidden_size=40`, `batch_size=32`, `max_epochs=200`. Kabul edilen Faz 1.5.9 v1.1 belgesi `hidden_size=32`, `batch_size=128`, `max_epochs=100` adaylarını kaydediyor. Bunlar nihai bilimsel değer sayılmamalı; ancak tek çalıştırılabilir config, kabul edilmiş protokolle açıkça eşleştirilip güncellendiğinde kullanılmalı.
3. Taslak içindeki `docs/phase1_5_9_hyperparameter_architecture.md` da v1.1 değil, eski protokol sürümünü temsil ediyor. Bu nedenle ZIP mevcut hâliyle “kabul edilmiş metodolojinin tutarlı uygulaması” sayılamaz.
4. Şu anki altı pytest testi, ZIP içindeki iskelet/ajan varlık kontrolleri. Bunlar model, pencereleme, scaler leakage veya Weymouth fiziksel doğrulama testleri değildir.

## 7. Faz C sonucu

**Kabul edilen mimari sınırları:** Yukarıdaki modül, config, notebook ve test ayrımları.

**Açık / yapılmamış:** Bilimsel modüllerin implementasyonu; gerçek bağımlılık kurulum testi; GitHub repo/MCP bağlantısı; Colab çalıştırması; Weymouth sayısal geri çözümü; parametre kararlarının kanıtla kapanması.

**Geçiş kapısı:** KAPALI. Bu belge Antigravity/skill paketi oluşturmaz ve mevcut taslak ZIP'i nihai ilan etmez.

## Kaynaklar
- Python Packaging Authority, “src layout vs flat layout”: https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/
- pytest, “Good Integration Practices”: https://pytest.org/en/stable/explanation/goodpractices.html
