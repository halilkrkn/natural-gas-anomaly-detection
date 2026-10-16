# FAZ B — Küresel OPEN-DECISION Kapanış Planı

**Sürüm:** 1.0  
**Durum:** Kapanış planı; bu belge tek başına hiçbir açık kararı kapatmaz.  
**Tez çerçevesi:** Doğal gaz iletiminde zaman serisi anomali tespiti ve erken uyarı; RUL yok; v1 tek boru, `fluids.compressible.Weymouth` tabanlı quasi-steady-state model; SKAB ve erişim sağlanırsa SWaT yalnızca alan sınırlılıkları açıkça yazılarak; IF, OCSVM, LOF, LSTM-AE, GRU-AE; W=16; StandardScaler yalnızca normal eğitim verisine fit; validation kalibrasyonu; test yalnızca nihai değerlendirme.

## 1. Zorunlu kaynak ve kanıt kuralı

Her karar için şu alanlar tutulur: (a) karar konusu, (b) kanıt türü, (c) kaynak ve kaynağın neyi gerçekten desteklediği, (d) aktarım sınırlılığı, (e) uygulanacak kontrol, (f) kapanış koşulu, (g) hangi dosyalara yansıdığı.

### Kanıt türleri

- **literature:** Konuyla doğrudan ilgili, izlenebilir bir bilimsel kaynakla desteklenir. Kaynakta bildirilen değer/range ve deney bağlamı kaydedilir.
- **dataset-derived:** Değer, veri kümesinin gerçek yapısından veya yalnızca eğitim verisinden hesaplanır. Test performansı ile belirlenmez.
- **explicit-assumption:** Doğrudan aktarılabilir literatür değeri bulunmadığında açıkça tasarım varsayımı olarak ilan edilir; neden gerekli olduğu ve sınırlılığı yazılır.
- **design-choice:** Tez kapsamını sade ve adil tutmak için önceden seçilir; literatür sabiti veya optimum gibi sunulmaz.
- **library-default:** Yazılım kütüphanesinin belgelenmiş varsayılanıdır. Bu yalnızca uygulama baseline'ıdır; bilimsel optimum veya karar kapanışının tek başına kanıtı değildir.

**Kritik ayrım:** Doğal gaz hattına ait yayınlar fiziksel değişkenler, sızıntı davranışı ve alan bağlamı için birincil kaynaktır. SKAB/SWaT gibi endüstriyel benchmark yayınları veri kümesi ve genel endüstriyel anomali değerlendirmesi için kullanılabilir; bu veri kümelerinin doğal gaz verisi olduğu iddia edilmez. Genel makine öğrenmesi yayınları bir yöntemin teorisini açıklayabilir, fakat doğal gaz uygulamasına ait sayısal parametreyi doğrudan kanıtlamaz.

## 2. Kaynak uygunluğu matrisi

### Doğal gaz boru hattı ve anomali bağlamı — birincil alan kaynakları

1. Miao, X., Zhao, H. & Xiang, Z. (2023). **Leakage detection in natural gas pipeline based on unsupervised learning and stress perception.** *Process Safety and Environmental Protection*, 170, 76–88. DOI: [10.1016/j.psep.2022.12.001](https://doi.org/10.1016/j.psep.2022.12.001).  
   **Destekler:** Doğal gaz boru hattında etiketli arıza örneklerinin sınırlı olması ve denetimsiz sızıntı tespitinin bağlamı.  
   **Tek başına desteklemez:** IF/OCSVM/LOF veya LSTM-AE/GRU-AE için evrensel hiperparametre değerlerini.

2. Wu, X. et al. (2023). **A machine-learning method to accurately recognize the leakage pressure-drop signals in trunk natural gas pipelines.** *Process Safety and Environmental Protection*, 179, 847–863. DOI: [10.1016/j.psep.2023.09.048](https://doi.org/10.1016/j.psep.2023.09.048).  
   **Destekler:** Ana iletim hattındaki basınç düşüş sinyallerini sızıntı ile diğer işletim olaylarından ayırmanın önemi.  
   **Sınır:** Çalışmanın sinyal/olay tanımı bizim sentetik rampalarımızla bire bir aynı varsayılmaz.

3. Kim, J. et al. (2021). **The development of leak detection model in subsea gas pipeline using machine learning.** *Journal of Natural Gas Science and Engineering*, 94, 104134. DOI: [10.1016/j.jngse.2021.104134](https://doi.org/10.1016/j.jngse.2021.104134).  
   **Destekler:** Basınç, kütlesel debi ve sıcaklığın doğal gaz hattı izleme bağlamında anlamlı gözlemler olabileceği.  
   **Sınır:** Deniz altı uygulaması bizim tek kara hattı v1 senaryomuzla aynı değildir; değişken seçimi için kanıt, sayısal parametre aktarımı için doğrudan kanıt değildir.

4. Zhao, L., Cao, Z. & Deng, J. (2024). **A review of leak detection methods based on pressure waves in gas pipelines.** *Measurement*, 236, 115062. DOI: [10.1016/j.measurement.2024.115062](https://doi.org/10.1016/j.measurement.2024.115062).  
   **Destekler:** Gaz boru hatlarında basınç sinyali üzerinden sızıntı tespit yöntemlerinin ve makine öğrenmesi yaklaşımlarının alan içi konumu.  
   **Sınır:** Basınç dalgası/akustik lokalizasyon çalışmaları, bizim quasi-steady-state Weymouth simülatörünün geçici rejim fiziğini çözdüğünü kanıtlamaz.

5. Kim, J. et al. (2024). **Gas Pipeline Leak Detection by Integrating Dynamic Modeling and Machine Learning Under the Transient State.** *Energies*, 17(21), 5517. DOI: [10.3390/en17215517](https://doi.org/10.3390/en17215517).  
   **Destekler:** Gaz hattı fizik modeliyle makine öğrenmesini birleştiren sızıntı tespiti için güncel bir alan karşılaştırması.  
   **Sınır:** Bu çalışma transient state ele alır; bizim v1 yaklaşımımız quasi-steady-state olduğundan transient sonuçları veya parametreleri doğrudan taşınmaz.

6. ElMahdy, O. F. M., Hassan, M. E. Z. & Metwalli, S. M. (2025). **Machine learning anomaly detection of lost and unaccounted for gas in natural gas networks.** *Journal of Engineering and Applied Science*, 72, 123. DOI: [10.1186/s44147-025-00677-x](https://doi.org/10.1186/s44147-025-00677-x).  
   **Destekler:** Gerçek doğal gaz ağlarında giriş-çıkış dengesi, ölçüm belirsizliği ve basınç/sıcaklık/debi ölçümlerinin operasyonel önemi. Çalışmada 21 ağın beş yıllık kayıtları kullanılmıştır.  
   **Önemli sınır:** Makaledeki *unaccounted-for gas* veya giriş-çıkış dengesizliği her zaman fiziksel sızıntı demek değildir; ölçüm, zamanlama ve muhasebe hataları da fark üretebilir. Bu nedenle bizim sentetik `Q_leak` değişkenimizle doğrudan eş tutulmaz.

7. **Development of natural gas flow rate in pipeline networks based on unsteady state Weymouth equation.** DOI/ScienceDirect: [makale sayfası](https://www.sciencedirect.com/science/article/pii/S1875510016303602).  
   **Destekler:** Weymouth yaklaşımının doğal gaz hattı debi hesabındaki yeri ve steady/unsteady davranış ayrımı.  
   **Sınır:** Bizim `fluids` fonksiyonumuzun sayısal doğrulamasının yerine geçmez; bunu gerçek kütüphane çağrısı ile ayrıca test edeceğiz.

### Veri kümesi ve yöntem kaynakları — kapsamı sınırlı şekilde kullanılır

8. Katser, I. D. & Kozitsin, V. O. (2020). **Skoltech Anomaly Benchmark (SKAB).** DOI: [10.34740/KAGGLE/DSV/1693952](https://doi.org/10.34740/KAGGLE/DSV/1693952); [resmî depo](https://github.com/waico/skab).  
   **Destekler:** SKAB'ın testbed tabanlı çok değişkenli zaman serisi olması; deney/dosya organizasyonu; `anomaly` ve `changepoint` etiketleri; basınç, sıcaklık, akış vb. sütunların veri anlamları.  
   **Sınır:** Kaynak, SKAB'ın su sirkülasyon test düzeneği olduğunu gösterir; doğal gaz hattı fiziksel parametrelerini veya gaz borusu sensör doğruluğunu desteklemez.

9. Malhotra, P. et al. (2016). **LSTM-based Encoder-Decoder for Multi-sensor Anomaly Detection.** [arXiv:1607.00148](https://arxiv.org/abs/1607.00148).  
   **Destekler:** Normal çoklu sensör zaman serisini encoder-decoder ile yeniden yapılandırma ve reconstruction error üzerinden anomali tespiti fikri.  
   **Sınır:** Belirli bir gizil boyut, pencere uzunluğu veya epoch sayısının doğal gaz için optimum olduğunu göstermez.

10. Liu, F. T., Ting, K. M. & Zhou, Z.-H. (2008). **Isolation Forest.** DOI: [10.1109/ICDM.2008.17](https://doi.org/10.1109/ICDM.2008.17).  
11. Schölkopf, B. et al. (2001). **Estimating the support of a high-dimensional distribution.** *Neural Computation*, 13(7), 1443–1471. DOI: [10.1162/089976601750264965](https://doi.org/10.1162/089976601750264965).  
12. Breunig, M. M. et al. (2000). **LOF: Identifying Density-Based Local Outliers.** *Proceedings of ACM SIGMOD*. DOI: [10.1145/335191.335388](https://doi.org/10.1145/335191.335388).  
   **Destekler:** Algoritmaların yöntemsel temelleri. **Tek başına desteklemez:** Bizim doğal gaz verimizdeki en iyi parametre değerleri.

## 3. Açık karar kapanış planı

### OPEN-DECISION-002: SKAB sensör seçimi

- **Neden açık:** SKAB sensörleri doğal gaz hattının fiziksel sensörleri değildir. Veri kalitesi, varyans, korelasyon/redundans ve sensör anlamları gerçek dosyalar incelenmeden seçimi kapatmaya yetmez.
- **Kanıt türü:** `dataset-derived` + `design-choice`.
- **Literatürün rolü:** SKAB resmî deposu sütunların anlamını ve dosya/deney yapısını destekler. Doğal gaz boru hattı yayınları basınç/debi/sıcaklık değişkenlerinin alan bağlamını destekler; SKAB sensörlerini doğrudan gaz sensörüymüş gibi yorumlamak için kullanılamaz.
- **Ne zaman kapanacak:** SKAB EDA tamamlanıp seçim, model metrikleri görülmeden önce sabitlendiğinde.
- **Kapanmadan önce yapılacak:** Her dosyada sensör mevcutluğu, NaN oranı, ardışık eksiklik, örnekleme aralığı, varyans, fiziksel anlam ve yüksek korelasyon incelemesi. Dışarıda bırakılan değişkenler gerekçesiyle kayıt altına alınır.
- **Dosyaya yansıma:** `reports/data_quality/skab_sensor_audit.md`, `configs/data.yaml`, `docs/decision_register.md`, sensör seçimi testleri.

### OPEN-DECISION-003: Eksik veri politikası

- **Neden açık:** Eksik veri oranı, blok uzunluğu ve zaman damgası boşlukları gerçek SKAB dosyalarında ölçülmedi. Baştan sabit bir eşik seçmek veri kanıtı olmadan karar vermek olur.
- **Kanıt türü:** `dataset-derived`; gerekirse sade bir `design-choice`.
- **Ne zaman kapanacak:** EDA raporunda eksik verinin tipi ve uzunluğu çıkarılıp kuralın etkisi test edildiğinde.
- **Kapanmadan önce yapılacak:** Tekil eksik örnek, kısa blok, uzun blok, tüm sensör kaybı ve timestamp gap ayrı sınıflandırılır. Kısa interpolasyon ancak gerekçelendirilirse; uzun eksik bloklar körlemesine doldurulmaz. W=16 penceresinin herhangi bir zorunlu girdisi eksikse pencere politikası açıkça uygulanır.
- **Dosyaya yansıma:** `src/preprocessing/missing_data.py`, `configs/data.yaml`, `tests/test_missing_data.py`, EDA raporu ve karar defteri.

### OPEN-DECISION-006: Üç sınıflı ground truth — P2 post-faz politikası onaylı; uygulama kontrolü açık
- Kullanıcı onayı: 18. saatte leak enjeksiyonu sonlanır (`Q_leak=0`); drift enjeksiyonu kaldırılır ve offset sıfırlanır. Quasi-steady v1'de dönüş anlıktır; transient recovery fiziği eklenmez.
- Etiket politikası: recovery sınıfı yok. 16 ardışık post-reset örnek oluşana kadar geçiş pencereleri üç sınıflı validation kalibrasyonundan ve sınıf metriklerinden çıkarılır; ardından post-faz pencereleri normal etiketlenebilir.
- Ne zaman kapanacak: pencere-sonu etiket çizelgesi ve config/manifest uygulama uyumu doğrulandığında.
- Kapanmadan önce yapılacak: 17:45, 18:00, 18:15, 21:45 ve 22:00 örnek zamanları için pencere içeriği/etiketi doğrulamak; validation dışlama maskesini kontrol etmek; test setini eşik seçimi için kullanmamak.

### OPEN-DECISION-007: Hiperparametrelerin nihai durumu

- **Neden açık:** Kütüphane varsayılanları çalıştırılabilir baseline sunar, fakat alan-özel optimum kanıtı değildir. Doğrudan doğal gaz verisi ile seçilen beş modelin parametrelerini bire bir bağlayan literatür bulunmayabilir.
- **Kanıt türü:** Parametre başına `library-default`, `literature` veya `explicit-assumption`.
- **Literatür ilkesi:** Doğal gaz boru hattı yayınları fiziksel görev ve değişkenler için önceliklidir. Genel anomaly/ICS çalışmaları model yapısı ve eğitim yaklaşımı için ikincil kanıt olabilir; farklı alandaki `nu`, `hidden_size`, batch size gibi değerler doğal gaz için optimum diye aktarılmaz.
- **Mevcut düzeltme:** OCSVM için `nu=0.1` değerinin önceki dayanağı genel IoT ağ trafiği çalışmasıdır; bu kaynak doğrudan doğal gaz hattı kanıtı değildir. Bu değer en fazla `provisional` aday olabilir; decision register kapanış kaynağı olarak gösterilmez.
- **Ne zaman kapanacak:** Baseline değerleri ve varsa tek/az sayıda önceden tanımlanmış duyarlılık adayının validation değerlendirmesi tamamlanıp kaynak uygunluğu kaydedildiğinde; nihai test açılmadan önce.
- **Kapanmadan önce yapılacak:** IF/LOF için geniş arama yapılmaz. OCSVM için bir ana `nu` adayı ve gerekçelendirilmiş en fazla bir duyarlılık adayı belirlenir. Her DL eğitim parametresinin kaynağı/varsayım türü belirtilir. Seçim test metriğiyle yapılmaz.
- **Dosyaya yansıma:** `configs/models.yaml` veya `configs/experiments.yaml`, `docs/hyperparameter_evidence.md`, her model config'i/testi, `docs/decision_register.md`.

### OPEN-DECISION-008: LSTM-AE / GRU-AE mimarisi

- **Neden açık:** Encoder-decoder rekonstrüksiyon yaklaşımı literatürle desteklenir; ancak bire bir aynı doğal gaz verisi, W=16 ve aynı iki hücre tipi için tek katman/hidden size kanıtlanmış optimum değildir.
- **Kanıt türü:** Mimari yaklaşım için `literature`; boyutlar için `explicit-assumption` veya bağlamı uygun çalışmadan aktarılmış aday.
- **Ne zaman kapanacak:** Aynı train/validation split'te şekil, kayıp kararlılığı, erken durdurma ve LSTM/GRU karşılaştırılabilirliği pilot kontrollerini geçtiğinde; test değerlendirmesinden önce.
- **Kapanmadan önce yapılacak:** Tek katmanlı encoder-decoder v1 adayı; LSTM ve GRU için eşit gizil boyut, loss, optimizer, eğitim verisi ve early-stopping kuralı. Model yalnızca tamamen normal eğitim pencereleriyle optimize edilir. Early stopping normal validation reconstruction loss kullanır; anomaly etiketleri model ağırlığı/epoch seçtirmez. Ek kapasite yalnızca gözlemlenebilir underfit kanıtı varsa düşünülür.
- **Dosyaya yansıma:** `src/models/deep_learning/lstm_autoencoder.py`, `gru_autoencoder.py`, `configs/models.yaml`, `tests/test_autoencoders.py`, pilot raporu ve karar defteri.

### OPEN-DECISION-009: Nihai seed ve tekrar sayısı

- **Neden açık:** Seed etkisi ve model eğitim varyansı henüz ölçülmedi. Tek seed nihai sonuç için yeterli değişkenlik bilgisini vermez; üç seed de otomatik olarak evrensel kural değildir.
- **Kanıt türü:** `design-choice`, pilotta `dataset/experiment-derived` değişkenlik özeti.
- **Ne zaman kapanacak:** Nihai test değerlendirmesinden önce, sabit split ve aynı hiperparametrelerle pilot tekrarlamaları bitip seed sayısı kilitlendiğinde.
- **Kapanmadan önce yapılacak:** Geliştirme için seed 42. Pilot/final adayları 42, 43, 44; aynı data split ve simülasyon koşuları korunur. Validation metrikleri ve eğitim kararlılığı mean±std olarak değerlendirilir. Yalnızca en iyi seed seçilmez. Pilot değişkenliği ve hesaplama bütçesi temelinde 3 tekrarın yeterli olup olmadığı test skorları görülmeden kararlaştırılır.
- **Dosyaya yansıma:** `configs/experiments.yaml`, `experiments/configs/`, run manifesti, `reports/metrics/`, karar defteri.

### OPEN-DECISION-011: SWaT'ın rolü

- **Neden açık:** Tez önerisinde SWaT erişim sağlanmasına bağlıdır; erişim veya kullanım koşulları henüz doğrulanmadı.
- **Kanıt türü:** Erişim/izin doğrulaması + `design-choice`.
- **Literatürün rolü:** SWaT, endüstriyel kontrol sistemi testbed'idir; doğal gaz hattı değildir. Eklenirse dış endüstriyel benchmark olarak sunulur, ana gaz hattı kanıtı gibi yorumlanmaz.
- **Ne zaman kapanacak:** Erişim ve kullanım koşulu netleştiğinde; veri erişilemiyorsa v1'de isteğe bağlı olmadığı açıkça kayıt altına alınıp kapatılabilir.
- **Kapanmadan önce yapılacak:** Erişim, atıf/lisans, veri biçimi, örnekleme ve etiket şeması kontrolü. SWaT ana veri pipeline'ından ayrı bir dataset adapter ile girer; eşik ve metrik prosedürü aynı kalır, domain limitation raporlanır.
- **Dosyaya yansıma:** `configs/data.yaml`, `docs/limitations.md`, adapter/EDA raporu ve karar defteri.

### OPEN-DECISION-012: Weymouth sayısal doğrulaması (Zavg policy selected: fixed 0.8065)

- **Neden açık:** Daha önceki nominal debi hesabı gerçek `fluids` çağrısında tekrar üretilmedi; segment başına basınç ve sıkıştırılabilirlik yaklaşımı sayısal olarak kontrol edilmeli.
- **Kanıt türü:** `literature` + kütüphane dokümantasyonu + çalıştırılmış sayısal test.
- **Alan kaynağı:** Weymouth'un doğal gaz akışını modelleme bağlamı için gaz boru hattı literatürü; bir `Q` değerinin makul olduğunu iddia etmek için yalnız literatür yetmez.
- **Ne zaman kapanacak:** Colab'da gerçek `fluids.compressible.Weymouth` fonksiyonuyla geri çözüm ve fiziksel tutarlılık testleri geçtikten sonra.
- **Politika kararı:** v1 için sabit `Zavg=0.8065` seçildi; segment-bazlı Z hesabı artık bu baseline için gerekli değildir. **Sayısal kapanıştan önce:** (1) Fonksiyon imzasını/sürümünü doğrula ve tüm argümanları isimle ver. (2) Verilen P1/P2'den Q hesapla; Q ile P2'yi geri çöz ve toleransla karşılaştır. (3) Akış birimini/reference conditions değerlerini kaydet. (4) Her segment için basınç, D, L, sabit Zavg, E, T ve Q denetle. (5) `Qin=Qout+Qleak` ilişkisini test et. (6) Pozitif/makul basınç ve fiziksel yön kontrollerini uygula. Geçmezse sentetik koşu üretimine geçme.
- **Dosyaya yansıma:** `src/simulation/weymouth_simulator.py`, `configs/simulation.yaml`, `tests/test_weymouth_simulator.py`, `reports/weymouth_validation.md`, karar defteri.

### OPEN-DECISION-014: Normal ölçüm gürültüsü büyüklüğü

- **Neden açık:** Doğal gaz ölçüm belirsizliğinin önemli olduğuna dair alan kanıtı vardır; ancak gerçek sensör/metre modeli seçilmediği için bu kanıt doğrudan `sigma` vermez. Ölçüm cihazının maksimum izin verilen hatası, rastgele gürültünün standart sapması ile aynı değildir.
- **Kanıt türü:** Mümkün olduğunca gaz ölçüm/cihaz literatürü (`literature`); cihaz spesifikasyonu yoksa açıkça `explicit-assumption`.
- **Kaynak uygunluğu notu:** ElMahdy et al. (2025) doğal gaz ağlarında ölçüm cihazı doğruluğu, yaşlanma ve ölçüm/hesaplama belirsizliğinin etkisini tartışır. Ancak meterde sınıfa bağlı 1–3% hata aralığı basınç/flow/temperature için doğrudan Gaussian `sigma` olarak alınamaz.
- **Kullanıcı onayı alındı:** Basınç σ=5 kPa, debi σ=Q0'ın %0.5'i, sıcaklık σ=0.1 K; tüm sigmaları 2× yapma tek duyarlılık kontrolü. Bunlar geçici `explicit-assumption` değerleridir.
- **Ne zaman kapanacak:** ana ve 2× gürültü koşulları çalıştırılıp karşılaştırmalı metrik/run-level özetleri kaydedildiğinde, nihai test değerlendirmesinden önce.
- **Kapanmadan önce yapılacak:** (1) Bias/drift şiddetlerini normal noise sigma ile karıştırma. (2) Her değişken için sensor/metrology kaynaklarını tara. (3) `sigma` karşılığı kaynaktan doğrudan gelmiyorsa `explicit-assumption` diye işaretle. (4) Tek baseline ve sınırlı düşük/yüksek duyarlılık koşulu önceden tanımla; sonuçlara göre gürültü seçme. (5) Ölçümde görülebilirlik ve fiziksel makullük kontrolü yap.
- **Dosyaya yansıma:** `configs/simulation.yaml`, `src/simulation/`, `reports/noise_assumption.md`, deney manifesti, karar defteri.

### OPEN-DECISION-016: Model girdilerinde akış temsili — Qin/Qout approved pilot candidate; validation pending

- **Kullanıcı onayı alındı:** `Qin` ve `Qout` ayrı gözlenen kanallar olarak ilk pilot adayıdır; türetilmiş `Qin-Qout` farkı ana girdiye otomatik eklenmeyecektir.
- **Neden açık:** Fiziksel simülasyonun iç değişkenleriyle modelin gözlem olarak alabileceği sensör değerleri aynı değildir. `Q_leak` senaryo parametresi doğrudan modele verilirse görevi yapay biçimde kolaylaştırma riski olur. `Qin` ve `Qout` ikisini vermek ise iki uçta ölçüm varlığını varsayar ve sızıntıyı aşırı kolaylaştırabilir.
- **Kanıt türü:** Doğal gaz hattı literatürü + `explicit-assumption` / `design-choice` + fiziksel değişken erişilebilirliği kontrolü.
- **Alan kaynakları:** Kim et al. (2021) basınç, kütlesel debi ve sıcaklığın boru hattı sızıntı izleme bağlamını destekler. ElMahdy et al. (2025), ağ debi dengesizliğinin ölçüm ve zamanlama hataları yüzünden de doğabileceğini; bu dengesizliğin tek başına fiziksel leak ile eşit olmadığını vurgular.
- **Ne zaman kapanacak:** Weymouth simülasyon çıktıları hazır olduğunda ve model girdileri gerçek bir gözlem senaryosu olarak gerekçelendirildiğinde, model eğitimi/test performansı seçimi etkilemeden önce.
- **Kapanmadan önce yapılacak:** (1) Latent fizik değişkenleri, ölçülen değerler ve label/metadata sütunlarını ayır. (2) `Q_leak`, anomali seviyesi, senaryo adı ve etiket gibi bilgileri model girdisinden çıkar. (3) `Qin_meas`, `Qout_meas`, tek bir debi kanalı veya debi dengesizliği türevinin her birinin ne tür sensörlere ihtiyaç duyduğunu yaz. (4) Birincil gözlem setini önceden seç; alternatif ancak gerekçeli duyarlılık analizi ise sınırlı tut. (5) Hiçbir girdi test başarısına bakılarak seçilmez.
- **Dosyaya yansıma:** `docs/data_dictionary.md`, `configs/data.yaml`, `configs/simulation.yaml`, `src/simulation/`, model input schema, testler ve karar defteri.

## 4. Önceden tanımlı ama kapanmış kararlar

Aşağıdakiler kanıt/kurallar yazıldığı için metodolojik olarak kapalıdır; gerektiğinde yeni bilimsel kanıt varsa yeniden açılabilir:

- **OPEN-DECISION-001 — Fiziksel debi ve sızıntı dengesi:** `Qin = Qout + Qleak`; sızıntı konumu v1'de boru ortası ve iki segmentli model. Model girdisi kararı OPEN-016'dan ayrı.
- **OPEN-DECISION-004 — Normal koşuların bölünmesi:** Weymouth normal koşuları 30 train / 10 validation / 10 test; 60/20/20'nin literatürde optimum olduğu iddia edilmez.
- **OPEN-DECISION-005 — Anomali koşusu sayısı:** Her koşul için 10 validation + 10 test koşusu; tasarım kararı ve test kompozisyonu önceden sabitlenir.
- **OPEN-DECISION-010 — SKAB'da üç sınıflı alarm:** SKAB'ın severity etiketi yoktur; üç seviyeli fiziksel alarm iddiası kurulmaz.
- **OPEN-DECISION-015 — Anomali zaman çizgisi:** Kademeli senaryo: 0–6 h normal, 6–12 h rampa, 12–18 h kritik şiddetin korunması, 18–24 h post. Sabit senaryo: 0–6 h normal, 6–18 h anomali, 18–24 h post.
- **OPEN-DECISION-017 — Alarm olayı:** Birincil analizde ilk T1 crossing tespit zamanı; ardışık crossing şartı yok. Run-level normal alarm oranı ayrıca raporlanır. Bu bir operasyonel tasarım tanımıdır.
- **OPEN-DECISION-018 — Autoencoder skoru:** Pencere ve değişkenler üzerindeki ortalama MSE; özellik bazlı rekonstrüksiyon hataları ayrıca raporlanır.
- **OPEN-DECISION-019 — İkili eşik seçimi:** Validation F1 maksimize; eşitlikte Recall, ardından normal validation noktalarında daha düşük FPR; test kullanılmaz.

## 5. Süperseed edilen kayıt

- **OPEN-DECISION-020 — W=16'nın W=32 ile duyarlılık karşılaştırması:** **SUPERSEDED / açık karar listesinde tutulmayacak.** Kullanıcının güncel nihai çerçevesi W=16'yı v1 pencere baseline'ı olarak kilitler ve W=32 denemesini istememektedir. Bu nedenle bu eski öneri aktif bir deney veya geçiş kapısı değildir.

## 6. Kapanış sırası ve geçiş kapıları

1. **Şimdi:** Bu planı küresel referans olarak kabul et; kararlar kanıtı gelmeden kapatılmaz.
2. **SKAB EDA:** OPEN-002 ve OPEN-003'ü gerçek dataset profiliyle tamamla.
3. **Colab / Weymouth doğrulaması:** OPEN-012'yi gerçek kütüphane çağrısı ve test çıktıları ile ele al.
4. **Fiziksel noise/input kararları:** OPEN-014 ve OPEN-016'yı kaynak + açık varsayım + test/senaryo gerekçesiyle, test sonuçlarına bakmadan tamamla.
5. **Model pilotları:** OPEN-007, OPEN-008 ve OPEN-009'u aynı sabit split'lerde, kayıtlı parametrelerle ve validation-only kurallarıyla değerlendir.
6. **SWaT:** Erişim durumu netleşince OPEN-011'i kapat.
7. **Kapanış biçimi:** Decision register'da statü, kapanış gerekçesi/kanıtı ve etkilenen dosyalar yazılı değilse karar `OPEN` veya `PROVISIONAL` olarak kalır.

## 7. Nihai Antigravity geçiş kapısı ile ilişki

Bu planın hazırlanması, Google Antigravity'ye nihai kod/agent/skill çalışması için geçiş izni vermez. Kullanıcının belirlediği kapılar geçerlidir: Faz 1.5.9 protokolü; küresel karar kapanış planı; GitHub deposu; Colab bağımlılık kurulumu ve `pip install -e .` ile temel testler; Weymouth sayısal geri çözüm/fiziksel kontrolleri ya geçmiş olmalı ya da bilinçli OPEN olarak kayıtlı olmalıdır. Nihai platform paketi bu kapılar öncesinde üretilmez veya nihai ilan edilmez.


### A4 seçim durumu — OPEN-DECISION-021
- Onaylanan yöntem: independent noise seed + 0–24 h demand phase jitter; demand amplitude ±5% sabit. Bu bir `design-choice`tir. Her run için `run_id`, `noise_seed`, `demand_phase_offset_hours`, `split` manifestte saklanmalı.
