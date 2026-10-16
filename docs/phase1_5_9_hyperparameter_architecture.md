# FAZ 1.5.9 — Hiperparametre ve Mimari Telafi Protokolü

**Sürüm:** 1.1 — kaynak uygunluğu denetimi eklenmiş protokol  
**Durum:** Protokol yazıldı; nihai model ayarları pilot kanıtına kadar açık/provisional. Parametre literatürü için doğal gaz boru hattına doğrudan uygunluk şartı ayrıca denetlendi.  
**Kapsam:** Isolation Forest, One-Class SVM, LOF, LSTM-AE, GRU-AE.  
**Amaç:** Gerekçeli, yalın bir baseline tanımlamak; geniş hiperparametre taramasından kaçınmak.

## 1. Değiştirilemez metodoloji sınırları

- Tez amacı doğal gaz iletim zaman serilerinde anomali tespiti ve erken uyarıdır; RUL kapsam dışıdır.
- Modeller: Isolation Forest, One-Class SVM, Local Outlier Factor, LSTM-AE ve GRU-AE.
- Pencere: W=16, 15 dakikalık örneklemede yaklaşık 4 saat; nedensel, step=1, look-ahead yok. Bu değer bu tez için **kilitli tasarım baseline'ıdır**, literatürde optimum olduğu iddia edilmez.
- Klasik modellerin girdisi, sensör başına mean/std/min/max/slope özellikleridir.
- Deep modeller ham, ölçeklenmiş zaman pencerelerini alır.
- StandardScaler yalnızca normal eğitim verisine fit edilir. Dataset başına ayrı scaler kullanılır.
- Eğitim yalnızca tamamen normal pencerelerle yapılır. Bölme koşu/dosya/deney birimini korur; aynı koşu iki split'e dağılmaz.
- Dış skor sözleşmesi: yüksek skor = daha anormal. Skorların işaret dönüşümü birim testleriyle doğrulanır.
- Eşikler yalnızca validation üzerinde seçilir. Test seti eşik veya hiperparametre seçmekte kullanılmaz.
- Birincil hedef yeni bir en iyi model aramak değil, beş yöntemin adil ve savunulabilir karşılaştırmasıdır.

## 2. Kanıt sınıfları

Her değer şu sınıflardan biriyle belgelenir:

- **Literatürden aktarılmış aday:** Bir yayında kullanılmıştır; başka veri alanından geliyorsa doğrudan optimum olarak kabul edilmez.
- **Kütüphane varsayılanı:** Uygulanabilir bir baseline'dır; bilimsel olarak optimal olduğu anlamına gelmez.
- **Tasarım tercihi:** Tez kapsamı, sadelik, karşılaştırılabilirlik ve nedensellik gerekçesiyle önceden belirlenmiştir.
- **Veriden türetilen:** Yalnızca eğitim verisi veya önceden tanımlı veri kalitesi incelemesinden hesaplanır.

Bir konfigürasyonda sayı bulunması bir kararı kapatmaz. Kapanış için kanıt, decision register kaydı ve yansıtıldığı dosya birlikte belirtilir.

## 3. Klasik modeller — baseline

### 3.1 Isolation Forest

| Parametre | Baseline | Kanıt sınıfı ve kaynağı | Neden / sınır |
|---|---|---|---|
| `n_estimators` | 100 | Kütüphane varsayılanı; scikit-learn API | Sade ve yaygın başlangıç; tarama yok. |
| `max_samples` | `auto` | Kütüphane varsayılanı; `min(256, n_samples)` | Modelin örnekleme davranışını ek taramayla karmaşıklaştırmaz. |
| `max_features` | 1.0 | Kütüphane varsayılanı | Seçilmiş özelliklerin tamamını kullanır. |
| `bootstrap` | `False` | Kütüphane varsayılanı | Varsayılan davranış korunur. |
| `contamination` | `auto` | Kütüphane varsayılanı | Yalnızca kütüphane iç eşiği için; tez kararları `predict` eşiğiyle değil validation skor kalibrasyonuyla verilir. |
| `random_state` | Pilot için 42 | Geliştirme tercihi | Nihai seed/tekrar sayısı OPEN-DECISION-009 olarak açık kalır. |

**Pilot kuralı:** Hiperparametre taraması yapılmaz. `score_samples` çıktısı `-score_samples(X)` ile dış anomali skoruna çevrilir. `contamination` iç kararı, validation ile seçilen tez eşiğiyle karıştırılmaz.

Kaynak: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html

### 3.2 One-Class SVM

| Parametre | Baseline adayı | Kanıt sınıfı ve kaynağı | Neden / sınır |
|---|---|---|---|
| `kernel` | `rbf` | Kütüphane varsayılanı; ayrıca Zahoor ve ark. (2025) TON_IoT çalışmasında kullanılmış | Doğrusal olmayan sınırı destekler; başka domain olduğu için optimum iddiası yok. |
| `gamma` | `scale` | Kütüphane varsayılanı; 2025 TON_IoT çalışmasında da kullanılmış | Özellik sayısı ve varyansını hesaba katan belgelenmiş baseline. |
| `nu` | 0.1 (provisional pilot adayı; nihai değil) | Alanla doğrudan örtüşmeyen TON_IoT makalesinde kullanılmış bir aday; **doğal gaz literatürü kanıtı değildir** | Bu nedenle `nu=0.1` karar kilidi değildir. Önce doğal gaz/SCADA odaklı kaynak taraması; doğrudan değer bulunamazsa açıkça `explicit-assumption` olarak kayıt ve en fazla bir validation-only duyarlılık karşılaştırması. |
| `tol` | 0.001 | Kütüphane varsayılanı | Optimizasyon toleransı için ek arama açılmaz. |

**Kaynak uygunluğu düzeltmesi:** `nu=0.1` ve `nu=0.5` değerlerini doğal gaz boru hattı için kanıtlanmış parametreler olarak göstermiyoruz. Önceki dayanak TON_IoT ağ trafiği çalışmasıdır; bu, tez konusuna doğrudan alan kanıtı değildir. Bu nedenle `nu=0.1` yalnızca **provisional pilot adayıdır**; decision register bu kaynakla kapatılmaz. Önceden belirlenmiş çok küçük bir duyarlılık karşılaştırması ancak doğal gaz/SCADA odaklı literatür incelemesi sonrasında ve validation-only protokolüyle yapılabilir. Test sonuçlarına bakarak seçim yapılmaz. `nu`, eğitim hatalarının üst sınırı ve destek vektör oranının alt sınırıyla ilgilidir; gerçek veri anomali oranı olarak yorumlanmaz.

Skor yönü: `-score_samples(X)`; yüksek skor daha anormal. `decision_function`/`predict` eşiği nihai tez eşiği olarak kullanılmaz.

Kaynaklar:  
- https://scikit-learn.org/stable/modules/generated/sklearn.svm.OneClassSVM.html  
- https://www.nature.com/articles/s41598-025-20445-4

### 3.3 Local Outlier Factor

| Parametre | Baseline | Kanıt sınıfı ve kaynağı | Neden / sınır |
|---|---|---|---|
| `n_neighbors` | 20 | Kütüphane varsayılanı | Yerel yoğunluk ölçeği için sade başlangıç; geniş tarama yapılmaz. |
| `metric` | `minkowski` | Kütüphane varsayılanı | Belgelenmiş varsayılan uzaklık metriği. |
| `p` | 2 | Kütüphane varsayılanı | Minkowski için Öklid uzaklığı. |
| `novelty` | `True` | Resmî scikit-learn novelty detection dokümanı | Validation/test'teki görülmemiş örnekleri puanlamak için zorunlu. |

**Pilot kuralı:** `novelty=True` ile fit yapılır. `score_samples` yalnızca eğitim sırasında görülmemiş validation/test pencerelerinde çalıştırılır; LOF'ta bu skorun düşük olması daha anormaldir, bu nedenle dış skor `-score_samples(X)` olur. Model `predict` eşiği kullanılmaz.

Kaynaklar:  
- https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html  
- https://scikit-learn.org/stable/modules/outlier_detection.html

## 4. LSTM-AE ve GRU-AE — ortak mimari baseline adayı

### 4.1 Mimari

- Girdi şekli: `(batch, W=16, F)`; `batch_first=True`.
- Encoder: tek recurrent katman; `hidden_size=32`.
- Latent bağlam: encoder'ın son gizil durumu `h_n`.
- Decoder: tek recurrent katman; bağlam W zaman adımına tekrarlanarak verilir.
- Çıktı projeksiyonu: doğrusal katmanla F değişkenine dönülür; çıktı şekli girdiyle aynı olur.
- LSTM-AE ile GRU-AE arasında hücre tipi dışındaki yapı, girdi, kayıp, eğitim protokolü ve değerlendirme aynı tutulur.
- Kayıp: tüm zaman adımları ve değişkenler üzerinde ortalama MSE.
- Eğitim pencereleri tamamen normal olmalıdır.
- Özellik bazlı hata, her sensör için pencerenin zaman boyutu üzerinde ayrıca saklanır.

`hidden_size=32`, endüstriyel kontrol sistemi zaman serileri için boyutları 32/64 ara temsil ve 16/32 latent boyut seçenekleriyle inceleyen bir LSTM-VAE çalışmasından esinlenen **provisional adaydır**. Çalışma VAE mimarisindedir; bizim sade LSTM-AE/GRU-AE'mizle aynı model değildir ve doğal gaz verisi üzerinde yapılmamıştır. Dolayısıyla değer doğal gaz literatürünün doğruladığı optimum değildir; yalnızca sadelik amacıyla sınanabilecek bir `explicit-assumption` / aktarılmış başlangıç adayı olarak tutulur.

Kaynak: https://pmc.ncbi.nlm.nih.gov/articles/PMC9030796/

### 4.2 Eğitim ayarları

| Parametre | Başlangıç adayı | Kanıt sınıfı ve kaynak | Neden / sınır |
|---|---|---|---|
| Optimizer | Adam | Endüstriyel zaman serisi AE literatüründe kullanılan yöntem; PyTorch belgelenmiş optimizer | Sade ve standart başlangıç. |
| `learning_rate` | 0.001 | PyTorch Adam varsayılanı; endüstriyel LSTM-AE örneklerinde de kullanılmış | Evrensel optimum değildir; pilot sırasında yalnızca öğrenmenin sayısal olarak kararlı olup olmadığı kontrol edilir. |
| `batch_size` | 128 | Endüstriyel LSTM/VAE zaman serisi çalışmasında kullanılan değer | Veri miktarı için uygulanabilirlik kontrol edilir; küçük veri grubunda son batch daha küçük olabilir, `drop_last=True` kullanılmaz. |
| `max_epochs` | 100 | Endüstriyel compressor-PLC LSTM-AE çalışmasında kullanılan üst sınır | Hedef epoch sayısı değildir; erken durdurma devrededir. |
| `early_stopping_patience` | 10 epoch | Aynı endüstriyel çalışma | Eğitim süresini sınırlayan başlangıç ayarı; pilotta normal validation kaybının takibiyle kontrol edilir. |
| `weight_decay` | 0 | Kütüphane başlangıç davranışı | İlk baseline'a ek düzenlileştirme parametresi sokulmaz. |
| `dropout` | Kullanılmayacak | Tasarım tercihi | Her recurrent blok tek katmanlı olduğundan PyTorch recurrent dropout parametresi katmanlar arası uygulanmaz; etkisiz bir hiperparametre eklenmez. |
| `seed` | Pilot için 42 | Geliştirme tercihi | Final tekrar sayısı OPEN-DECISION-009 olarak kalır. |

Kaynaklar:  
- https://docs.pytorch.org/docs/stable/generated/torch.optim.Adam.html  
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9030796/  
- https://doi.org/10.1016/j.array.2026.100940

### 4.3 Eğitim ve model seçimi

- `StandardScaler` normal eğitim verisine fit edilir; validation/test sadece dönüştürülür.
- Derin model yalnızca normal eğitim pencereleriyle optimize edilir.
- Early stopping, **normal etiketli validation pencerelerinin MSE'si** üzerinden çalışır. Anomali etiketleri model ağırlıklarını veya durdurma epoch'unu seçmek için kullanılmaz.
- En iyi normal-validation kaybındaki checkpoint saklanır.
- Eşik kalibrasyonu bundan sonra, mevcut tez protokolündeki validation prosedürüyle yapılır.
- Ana karşılaştırma için `hidden_size=32` kullanılır. Eğitim ve normal-validation kayıplarının ikisi de yüksek seviyede plato yapar ve overfit işareti yoksa tek duyarlılık adayı `hidden_size=64` çalıştırılabilir; gerekçe ve sonucu decision register'a yazılır. Bu koşul oluşmazsa ikinci mimari koşul çalıştırılmaz.
- LSTM-AE ve GRU-AE için bu kural aynıdır. Test skorları mimari seçimine katılmaz.

Literatür gerekçesi: LSTM encoder–decoder yaklaşımı normal zaman serisi davranışını yeniden yapılandırmayı öğrenir ve rekonstrüksiyon hatasını anomali skoruna dönüştürür; dizi uzunluğu ve mimari değerleri veri alanına bağlıdır. Bu nedenle yayınlardaki belirli boyutlar evrensel optimum sayılmaz. https://arxiv.org/abs/1607.00148

## 5. Pilot protokolü — küçük ve önceden tanımlı

1. Önce tek geliştirme seed'i `42` ile bir uçtan uca smoke/pilot çalıştırması yapılır; bu nihai sonuç değildir.
2. Bütün veri bölmeleri ve split manifesti sabit kalır; hiçbir koşu veya dosya train/validation/test arasında bölünmez.
3. Kontroller: girdi/çıktı şekilleri, NaN/Inf olmaması, model skor yönü, scaler'ın yalnızca eğitim verisine fit edilmesi, eğitim verisinin tamamen normal olması, LOF novelty davranışı, eşiklerin yalnızca validation'da seçilmesi.
4. Isolation Forest ve LOF için geniş parametre araması yapılmaz.
5. OCSVM için önce doğal gaz/SCADA odaklı kaynak taraması tamamlanır. Doğrudan aktarılabilir bir sayısal `nu` bulunmazsa `nu=0.1` yalnızca provisional/explicit-assumption pilot adayı olarak tutulur; en fazla `nu=0.5` tek duyarlılık adayı olarak validation-only karşılaştırmasına alınabilir. Bu karşılaştırma kaynak uygunluğu ve gerekçesi decision register'a yazılmadan nihai deney planına girmez.
6. LSTM-AE/GRU-AE aynı mimari ve eğitim ayarlarıyla çalıştırılır; normal-validation kaybı üzerinden erken durdurma yapılır. `hidden_size=64` yalnızca 4.3'teki underfit koşulu varsa denenir.
7. Her deneme için konfigürasyon, veri/split sürümü, seed, paket sürümleri, eğitim süresi, epoch, train/normal-validation kayıpları, validation skorları ve seçilmiş eşikler kaydedilir.
8. Test verisiyle hiçbir ayar seçilmez. Bir test metriği görüldükten sonra parametre değişirse mevcut test sonucu artık nihai test sonucu olarak kullanılamaz; değişiklik yeni deney sürümü olarak kaydedilir.
9. Nihai tekrar sayısı pilot değişkenliği görülene kadar açık kalır; en iyi seed seçilmez.

## 6. Karar defteri durumu

- **FAZ 1.5.9 protokolü:** Yazıldı; kapsamı sade baseline ve pilot kuralıyla tamamlandı.
- **OPEN-DECISION-007 — Hiperparametrelerin nihai durumu:** AÇIK. Yukarıdaki adaylar pilot kanıtı ve decision register güncellemesiyle kapanabilir.
- **OPEN-DECISION-008 — LSTM/GRU mimarisi:** AÇIK/PROVISIONAL. Ortak 1-katmanlı encoder-decoder baseline adaydır; pilot shape/loss/underfit kontrolleri gerekir.
- **OPEN-DECISION-009 — Nihai seed/tekrar sayısı:** AÇIK. Pilot varyansı görülmeden kapatılmaz.
- **W=16:** Kullanıcının güncel nihai çerçevesinde kilitli tasarım baseline'ıdır; bu protokol W=32 taraması eklemez. Önceki yanıtta önerilmiş `OPEN-DECISION-020` bu çerçeveyle çeliştiği için **SUPERSEDED** sayılmalı ve açık kararlar arasında tutulmamalıdır.

## 7. Referans özeti

1. scikit-learn. IsolationForest API. https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html
2. scikit-learn. OneClassSVM API. https://scikit-learn.org/stable/modules/generated/sklearn.svm.OneClassSVM.html
3. scikit-learn. LocalOutlierFactor API and novelty detection. https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html
4. Zahoor, A. et al. (2025). *Robust IoT security using isolation forest and one class SVM algorithms*. Scientific Reports. https://www.nature.com/articles/s41598-025-20445-4
5. Malhotra, P. et al. (2016). *LSTM-based Encoder-Decoder for Multi-sensor Anomaly Detection*. https://arxiv.org/abs/1607.00148
6. *Lightweight Long Short-Term Memory Variational Auto-Encoder for Multivariate Time Series Anomaly Detection in Industrial Control Systems* (2022). https://pmc.ncbi.nlm.nih.gov/articles/PMC9030796/
7. *A 5G-enabled edge–cloud collaborative framework for anomaly detection in industrial compressor PLC data* (2026). https://doi.org/10.1016/j.array.2026.100940. Bu kaynak genel endüstriyel PLC bağlamındadır; doğal gaz boru hattı için bire bir parametre kanıtı değildir.
8. PyTorch. Adam optimizer API. https://docs.pytorch.org/docs/stable/generated/torch.optim.Adam.html


## 8. Alan-uygunluğu denetimi (v1.1 ek notu)

Doğrudan doğal gaz boru hattı yayınları önce incelenecektir. Örnekler: Miao et al. (2023), doğal gaz hattında unsupervised leak detection (https://doi.org/10.1016/j.psep.2022.12.001); Wu et al. (2023), ana doğal gaz iletim hattında pressure-drop sinyalleri (https://doi.org/10.1016/j.psep.2023.09.048); Kim et al. (2021), doğal gaz boru hattında ML ile sızıntı tespiti (https://doi.org/10.1016/j.jngse.2021.104134); Zhao et al. (2024), gaz boru hatlarında pressure-wave tabanlı leak-detection yöntemleri (https://doi.org/10.1016/j.measurement.2024.115062). Bu yayınlar fiziksel değişkenler, olay tipleri ve alan bağlamı için önceliklidir.

Bu yayınlardan doğrudan beş modelin tüm parametrelerini veren bir kanıt yoksa parametre uydurulmayacak. Kütüphane default'u `library-default`; model boyutu, batch size veya noise sigma gibi bağlamla örtüşmeyen bir değerin aktarımı ise `explicit-assumption`/`provisional` olarak yazılacaktır. Özellikle doğal gaz olmayan IoT ağ trafiği, tıbbi veya görsel veri alanlarındaki parametreler doğal gaz için optimum kanıtı sayılmayacaktır.
