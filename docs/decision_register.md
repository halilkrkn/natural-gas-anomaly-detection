# Global decision register

This is the authoritative global register across all phases. Status changes require evidence, not mere code/config creation.

**Statuses:** 🔒 LOCKED = current justified baseline; 🟡 OPEN = missing required evidence/choice; 🔵 PROVISIONAL = pilot/candidate only; 🔴 REJECTED/SUPERSEDED = no longer current.

**Source order:** current approved thesis proposal → `docs/thesis_method_contract.md` + this register → `configs/` → implementation. Surface conflicts; never resolve them silently.

## OPEN decisions

### OPEN-DECISION-002: SKAB sensor selection
- Neden açık: Sensör seçimi gerçek dosyaların veri kalitesi, fiziksel rolü, değişkenliği ve tekrar eden bilgi yapısının EDA incelemesini gerektiriyor.
- Ne zaman kapanacak: SKAB EDA ve kalite kontrolü tamamlandığında, split manifesti dondurulmadan önce.
- Kapanmadan önce yapılacak: Sensör rolü, eksiklik, varyans, zaman damgası, korelasyon/tekrar ve veri kalitesi kontrolleri; sensör seçimi test performansına göre yapılmayacak.

### OPEN-DECISION-003: Eksik veri politikası
- Neden açık: Tekil NaN, uzun eksik blok ve zaman damgası boşluğu farklı yöntem gerektirebilir.
- Ne zaman kapanacak: SKAB EDA ve eksiklik örüntüsü incelemesi tamamlandığında.
- Kapanmadan önce yapılacak: Eksik oranını, ardışık eksik uzunluğunu ve W=16 pencere etkisini ölçmek; kısa boşluk doldurma ve uzun blok dışlama kurallarını gerekçelendirmek.

### OPEN-DECISION-006: Gradual-scenario ground-truth timeline — 🟡 OPEN (post-phase policy approved; window-end implementation check pending)
- Kullanıcı onayı: mevcut zaman/faz temelli baseline korunur: 24 h run, 15-minute sampling; 0–6 h normal; 6–12 h ramp/early-warning phase; 12–18 h critical hold; 18–24 h post phase. Şiddet-temelli etiketlere bu aşamada geçilmiyor; drift için ayrıca kaynaklı/gerekçeli eşik bulunmadığından yeni şiddet eşiği uydurulmayacak.
- Fixed leak/bias cases remain binary evaluation scenarios; only gradual leak/drift scenarios participate in three-class calibration.
- **Kullanıcı onaylı post-faz fiziği (P2):** 18. saatte gradual leak enjeksiyonu sona erer (`Q_leak=0`) ve quasi-steady model, aynı talep profili altında normal kütle dengesi/işletim durumuna döner. 18. saatte sensor-drift enjeksiyonu kaldırılır; drift offset'i sıfırlanır (sensör yeniden kalibre edilmiş gibi). Geçici rejim veya kademeli fiziksel iyileşme modellenmez; bu, quasi-steady v1 kapsamındaki açık sadeleştirmedir.
- **Kullanıcı onaylı post-faz etiket politikası:** recovery sınıfı eklenmez. 18. saatten sonra, W=16 için 16 ardışık post-reset gözlem birikene kadar pencereler üç sınıflı kalibrasyondan ve üç sınıflı sınıf-metriklerinden dışlanır. 15 dakikalık örnekleme ile ilk uygun pencere sonunun beklenen zamanı yaklaşık 22:00'dır; kesin pencere-end sınırı örnek zaman çizelgesi kontrolünde doğrulanacaktır. Sonraki post-faz pencereleri `normal` olarak etiketlenebilir.
- **Lead time:** OPEN-DECISION-015 gereği `t_critical - t_detect` korunur; `t_critical` önceden belirlenen 12. saat kritik uç noktasıdır, post-fazın başlaması lead-time tanımını değiştirmez.
- **Alarm olayı:** OPEN-DECISION-017 gereği ilk `T1` aşımı tespit olayıdır; persistence filtresi eklenmez. Post-faz geçiş pencerelerinin dışlanması, bu birincil tespit kuralını değiştirmez.
- Ne zaman kapanacak: window-end label davranışı örnek zaman çizelgesiyle doğrulandığında ve config/manifest ile uygulama uyumu kontrol edildiğinde.
- Kapanmadan önce yapılacak: 17:45, 18:00, 18:15, 21:45, 22:00 örnek zaman damgaları için pencere içeriği ve etiketi gösteren küçük bir doğrulama tablosu üretmek; validation koşularında dışlama maskesinin T1/T2 kalibrasyonuna etkisini kontrol etmek; test setini eşik seçimi için kullanmamak.
- **Early sınıfı sınırlılığı:** 6–12 h aralığı zamana göre `early_warning` etiketlenir; ancak rampanın başındaki sızıntı sinyali ölçüm gürültüsü seviyesinin altında kalabilir. Bu nedenle Early sınıfı recall değerinin düşük çıkması beklenebilir. Sonuçlar sınıf bazında raporlanacak; bu durum zaman-temelli etiketlemenin sonucu olarak tartışılacak, tek başına yöntem hatası sayılmayacak. `t_critical - t_detect` lead-time hesabı bu sınıf etiketinden bağımsızdır.

### OPEN-DECISION-007: Model hiperparametreleri
- Neden açık: Beş modelin başlangıç adayları listelendi; henüz hedef ortamda pilotla doğrulanmadı.
- Ne zaman kapanacak: Colab pilotu ve hata/kararlılık kontrolleri tamamlanıp nihai model deneylerinden önce.
- Kapanmadan önce yapılacak: `docs/phase1_5_9_hyperparameter_architecture.md` tablosundaki kaynak/değer/bağlam/uygunluk kayıtlarını korumak; geniş ve gerekçesiz taramadan kaçınmak; gerçek run configs ve sonuçları eklemek.

### OPEN-DECISION-008: LSTM-AE/GRU-AE mimarisi
- Neden açık: Basit ortak encoder-decoder adayı tariflendi ama kodlanıp şekil/kayıp/öğrenme eğrisi testleri geçmedi.
- Ne zaman kapanacak: Her iki mimari Colab pilotunda aynı veri ve eğitim düzeninde çalıştırılıp kabul koşullarını geçtiğinde.
- Kapanmadan önce yapılacak: Girdi/çıktı şekli, MSE, early stopping, model parametre sayısı, hata analizi ve karşılaştırılabilirlik testleri.

### OPEN-DECISION-009: Nihai seed ve tekrar sayısı
- Neden açık: Seed 42 geliştirme başlangıcıdır; tekrarlanabilirlik raporlama sayısı pilot varyasyonu görülmeden belirlenmemiştir.
- Ne zaman kapanacak: Sabit split ve config ile pilot tekrarları bitip değişkenlik gözlemlendiğinde, final testten önce.
- Kapanmadan önce yapılacak: En iyi seed seçmemek; bağımsız run ve model-seed değişkenliğini ayırt etmek; ortalama ± SD raporlama kuralını sabitlemek.

### OPEN-DECISION-011: SWaT'ın kapsam içindeki rolü
- Neden açık: Erişim durumu ve doğal gaz dışı veri setinin ek dış doğrulama katkısı belirsiz; ana tez buna bağlı değil.
- Ne zaman kapanacak: Veri erişimi, lisans/erişim koşulları ve ek iş yükü gözden geçirildiğinde.
- Kapanmadan önce yapılacak: Dış endüstriyel genelleme katkısını kapsam kayması ve zaman maliyetiyle karşılaştırmak; kullanılamazsa SKAB+Weymouth ile devam etmek.

### OPEN-DECISION-012: Weymouth sayısal doğrulaması — 🟡 OPEN; Zavg policy subdecision closed
- **A1 policy decision: 🔒 CLOSED — fixed Zavg=0.8065 for both segments in the v1 controlled synthetic baseline.** Rationale: minimum-complexity v1; the value is a derived/provisional simplifying assumption, not a universal literature constant. Limitation: absolute pressure values may shift with compressibility assumptions; do not claim full physical validation.
- Rejected for v1 baseline (not deleted as a future alternative): Papay–Sutton segment-specific pressure-dependent Zavg, because it adds iterative segment-specific calculations outside the current simple baseline.
- Neden OPEN: User-provided review reports `fluids==1.3.1` API/round-trip tests passed in another environment, but this runtime/Colab evidence has not yet been independently captured. The policy choice is closed; the numerical-validation decision is not.
- Ne zaman kapanacak: Colab'da actual `fluids` outputs, nominal round-trip, demand monotonicity and two-segment sanity checks are saved; the report, code/config and decision record agree.
- Kapanmadan önce yapılacak: Run the validation notebook; record package version/signature, Q0/P2/P_mid/P_out, flow unit/reference conditions, and pass/fail outputs. No A/B Z comparison is required for this selected v1 policy; report the fixed-Z limitation.

### OPEN-DECISION-014: Normal ölçüm gürültüsü büyüklüğü — 🔵 APPROVED PROVISIONAL ASSUMPTIONS; evidence pending
- Kullanıcı onayı: pilotta geçici explicit-assumption adayları kabul edildi: pressure sigma 5 kPa (nominal 5 MPa'nın %0.1'i), flow sigma Q0'ın %0.5'i, temperature sigma 0.1 K. Bunlar gerçek operatör sensör spesifikasyonu veya literatür bulgusu değildir; final fiziksel parametre olarak kilitlenmedi.
- Kullanıcı onayı: tek düşük karmaşıklıklı duyarlılık kontrolü, diğer her şeyi sabit tutup üç sigma değerini birlikte 2 katına çıkarmaktır.
- Neden OPEN: varsayımların etkisi henüz Colab pilotunda ölçülmedi.
- Ne zaman kapanacak: ana ve 2× noise koşuları tamamlanıp metrikler/run-level değişkenlik karşılaştırması kaydedildiğinde ve sonuçlar bu varsayımın uygunluğunu desteklediğinde; aksi durumda revize edilip yeniden test edilir.
- Kapanmadan önce yapılacak: her kanal için birim/baz değeri doğrulamak; accuracy bound ile sigma'yı karıştırmamak; aynı noise üretim kuralını normal ve anomali koşularına uygulamak.

### OPEN-DECISION-016: Model girdisinde akış değişkenlerinin temsili — 🔵 APPROVED PILOT CANDIDATE; not closed
- Kullanıcı onayı: ilk pilot adayı, fiziksel olarak gözlenebilir basınç kanallarıyla birlikte `Qin` ve `Qout` ayrı kanallarıdır. Türetilmiş `Qin-Qout` dengesizliği ana girdiye otomatik eklenmeyecektir.
- Neden OPEN: pilotta gözlenebilirlik ve model görevinin yapay biçimde kolaylaşıp kolaylaşmadığı test edilmedi. Simülatörde Qin−Qout=Q_leak olduğundan bu fark, sızıntı büyüklüğünü neredeyse doğrudan göstererek görevi yapay biçimde kolaylaştırabilir.
- Alternatifler: (1) Qin+Qout: sızıntı kütle dengesini görünür kılar ancak simülatördeki fark çok doğrudan bir şiddet göstergesidir. (2) Qout+basınç: daha az doğrudan gösterge olabilir; küçük sızıntıların görünürlüğü azalabilir. (3) Qin−Qout: en doğrudan göstergedir ve pilotun birincil girdisine otomatik eklenmeyecektir.
- Kesin yasak: `Q_leak`, anomaly severity, scenario ID, ramp ayarı veya başka ground-truth-only alan model girdisine giremez.
- Ne zaman kapanacak: aynı önceden sabitlenmiş validation koşularında küçük karşılaştırma tamamlandığında, gözlenen model kanalları simülatör ground-truth alanlarından veri sözlüğünde ayrıldığında ve sonuçlar karar kaydına işlendiğinde.
- Kapanmadan önce yapılacak: gözlenebilirlik varsayımını yazmak; Qin/Qout farkının görevi yapay biçimde kolaylaştırma düzeyini pilotta ölçmek; test setine bakarak seçim yapmamak.


## Closed / locked decisions

### OPEN-DECISION-001: Physical leak representation — 🔒 LOCKED
- Normal: Qin=Qout. Leak: Qin=Qout+Qleak. Leak at x=0.5L using two L/2 segments. This is a simplified controlled mass-balance scenario, not an orifice/transient physical leak model.

### OPEN-DECISION-004: Weymouth normal-run split — 🔒 LOCKED baseline
- Current baseline: 30 train / 10 validation / 10 test normal runs. Practical design choice, not a literature optimum. No run can appear in more than one split.

### OPEN-DECISION-005: Number of runs per anomaly condition — 🔒 LOCKED baseline
- Current baseline: 10 validation and 10 test runs for each registered anomaly condition; no anomaly training runs. Revisit only with a justified reason and before final test results are evaluated.


### OPEN-DECISION-021: Run-to-run variability design — 🔒 CLOSED design choice
- Kullanıcı onayı: Aday B seçildi — her koşuda bağımsız noise seed ve 24 saatlik periyodik talep profilinde 0–24 saat arası başlangıç fazı kaydırması uygulanır. ±%5 talep genliği sabit kalır.
- Sınıflandırma: `design-choice`; literatürden alınmış fiziksel sabit veya gerçek operatör talep profili değildir.
- Uygulama sözleşmesi: her run için `run_id`, `noise_seed`, `demand_phase_offset_hours` ve `split` manifestte kaydedilecek; validation/test run'ları bağımsız seed/fazlarla üretilecek. Nihai test sonuçlarına bakılarak fazlar seçilmeyecek.
- Kapanış koşulu: karar politikası kapandı. Uygulama doğrulaması Phase 3'te config/manifest üretildiğinde yapılacak; başarısız uygulama OPEN kararını yeniden açmak yerine kod hatası olarak düzeltilecek.

### OPEN-DECISION-010: SKAB three-level alarms — 🔒 LOCKED
- Do not force synthetic three-class early-warning/critical ground truth onto SKAB. Report binary anomaly metrics and detection delay after labeled anomaly onset.

### OPEN-DECISION-015: Scenario timing and detection lead time — 🔒 LOCKED
- For gradual simulation anomalies, lead time = predefined scenario critical time minus detection time, not T2 crossing time. SKAB uses detection delay after labeled onset.

### OPEN-DECISION-017: Alarm persistence/event definition — 🔒 LOCKED primary analysis
- First score crossing T1 after scenario onset defines detection time. No consecutive-crossing persistence filter in primary results. Report point-level FPR and proportion of normal runs with at least one alarm.
- Known risk recorded: a single noisy threshold crossing may count as a detection and may inflate false alarms/lead-time estimates. Do not add a persistence filter to primary analysis without user-approved protocol revision. The two registered false-alarm summaries are mandatory.

### OPEN-DECISION-018: Autoencoder reconstruction score — 🔒 LOCKED
- Window score is MSE averaged over W time steps and F input channels. Save per-channel MSE separately for diagnostics. Higher score = more anomalous.

### OPEN-DECISION-019: Binary threshold objective — 🔒 LOCKED
- Validation-only candidate boundaries between distinct scores; maximize binary validation F1; ties by higher Recall and then lower FPR on normal validation windows. Test labels/scores never choose a threshold.

## Superseded decisions

### OPEN-DECISION-020: W=16 pencere uzunluğunun uygunluğu — 🔴 SUPERSEDED
- Gerekçe: Güncel kullanıcı onaylı nihai çerçeve W=16'yı kilitli v1 baseline olarak tanımlar ve W=32 duyarlılık deneyi istemez. Bu kayıt artık aktif açık karar değildir.
- Geçersiz olan eski öneri: W=16 ile W=32 karşılaştırması.
- Etki: W=16 aktif tasarım baseline'ı olarak kalır; W=32 için deney, konfigürasyon veya hiperparametre taraması yapılmaz.
- Yeniden açma koşulu: Yalnızca kullanıcı tarafından onaylanan yeni bilimsel kapsam değişikliği ve bunun önceden kayıt altına alınması.

## Locked baseline rules (must also pass implementation tests)

- Five models: IF, OCSVM, LOF, LSTM-AE, GRU-AE.
- W=16 causal windows, stride 1; no W=32 sensitivity experiment in the current approved scope.
- Split runs/files before preprocessing/windowing. No overlapping windows across split boundaries.
- Fit transformations on normal training data only; train only on fully normal windows.
- Shared score contract: higher = more anomalous.
- Numeric thresholds are model-specific and calibrated on validation only. Normal/early/critical use two thresholds T1/T2: score<T1 normal; T1≤score<T2 early warning; score≥T2 critical.
- Same final test runs for every model; record manifests, configs, seeds, versions, raw scores, predictions and run-level metrics.
- Any change to a locked item requires a scientific rationale, updated register, affected-result invalidation/recomputation plan, and pre-test documentation.



## Legacy conversation labels (not authoritative decision IDs)

| Eski sohbet ifadesi | Yetkili kayıt | Açıklama |
|---|---|---|
| “OPEN-001 = akış girdisi” | OPEN-DECISION-016 | Eski sohbet numarası karışıklığı; akış girdisi kararı 016'dır. |
| OPEN-DECISION-001 | OPEN-DECISION-001 (LOCKED) | Fiziksel sızıntı temsili: Qin=Qout+Q_leak ve orta noktada iki segment. |
| OPEN-DECISION-006 | OPEN-DECISION-006 (time-phase baseline and P2 post policy approved; implementation check OPEN) | Kademeli senaryo etiketleme; P2 + W=16 transition exclusion selected. |
| OPEN-DECISION-020 | OPEN-DECISION-020 (SUPERSEDED) | W=32 karşılaştırması aktif kapsamda değildir. |

`docs/decision_register.md` is the single source of truth for decision IDs/statuses. Chat shorthand must not create a new decision ID.
