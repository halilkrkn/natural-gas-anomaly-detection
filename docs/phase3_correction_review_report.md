# Faz 3 dosyası düzeltme raporu

Tarih: 16 Ekim 2026  
Kapsam: Kullanıcının yüklediği “ChatGPT'ye Gönderilecek Düzeltme Talimatı — Tez Faz 3.md” maddeleri 1–15.  
Durum: **Düzeltmeler uygulandı. A1 ve A4 politika kararları kapatıldı; A2 ve A3 onaylı baseline/pilot olarak kaydedildi, ilgili pilot veya alt kararlar açık kaldı. OPEN-014 onaylı geçici varsayımdır; sonuçlar bekleniyor.**

## Madde bazında değerlendirme

1. **Katılıyorum.** A1 işlendi: sabit `Zavg=0.8065` v1 için seçildi. Bu alt karar kapalı; genel `OPEN-DECISION-012` Colab sayısal doğrulaması tamamlanana kadar açık.
2. **Katılıyorum.** `OPEN-DECISION-016` seçenekleri gözlenebilirlik ve görevi yapay biçimde kolaylaştırma riski açısından karşılaştırıldı. Qin ve Qout ayrı gözlenen kanallar pilot adayı olarak onaylandı; türetilmiş dengesizlik otomatik eklenmeyecek. Q_leak, severity, senaryo ID ve ground-truth-only alanlar model girdisinden hariç tutuldu.
3. **Katılıyorum.** A3 işlendi: zaman/faz etiket baseline'ı onaylandı. Post fazının üç sınıflı kalibrasyondaki işlenişi alt karar olarak açık kaldı; seçilmeden kodlanmayacak.
4. **Katılıyorum.** A4 işlendi: bağımsız gürültü tohumu + 0–24 saat talep fazı kaydırması seçildi. ±%5 talep genliği değişmedi; politika kapalı, manifest uygulama kontrolü bekliyor.
5. **Katılıyorum.** OPEN-014 geçici gürültü adayları ve tüm sigmaları 2× yapma duyarlılık kontrolü kullanıcı onayıyla pilot için kabul edildi. Sonuçlar gelene kadar OPEN kalıyor.
6. **Katılıyorum.** `OPEN-DECISION-017` kararının kendisi değiştirilmedi. Tek T1 aşımının yanlış alarmı şişirebilme riski kaydedildi; point-level FPR ve en az bir alarm veren normal koşu oranı raporlama şartı korundu.
7. **Katılıyorum.** `docs/thesis_method_contract.md` içine pencere sayısının bağımsız deney sayısı olmadığı ve run-level özetlerin raporlanacağı eklendi.
8. **Katılıyorum.** Aynı sentetik üretici ve basit periyodik talep profiline bağlı genellenebilirlik sınırlılığı tez diliyle eklendi. Ek deney eklenmedi.
9. **Katılıyorum.** SKAB'da ikili, Weymouth kademeli senaryolarda üç sınıflı değerlendirme gerekçesi eklendi; danışmana sorulacak konu karar defterine yazıldı.
10. **Katılıyorum.** Yöntem metninde eğitim normal veriyle yapılsa da T1/T2'nin etiketli validation senaryolarında Macro-F1 ile seçildiği açıkça belirtildi. Bu, test sızıntısı değildir; ancak eşik kalibrasyonu validation-supervised/semi-supervised olarak şeffaf anlatılmalıdır.
11. **Katılıyorum.** `docs/parameter_source_audit.md` eklendi. Her parametrede kaynak, kaynakta doğrulanabilen iddia, bağlama uygunluk ve statü ayrıldı. D=0.75 m, L=100 km, P1=9 MPa, SG=0.675 ve Tavg=283.15 K değerlerinin tam kaynak tablosu/satırı bu incelemede bağımsız doğrulanamadı; bu nedenle **doğrulanamadı** olarak yazıldı. Bunları henüz “literatürle doğrulanmış” diye sunmuyoruz.
12. **Katılıyorum.** `scripts/sync_agent_skills.py` paketten kaldırıldı; skill paketi geçiş kapısı açılana kadar kapsam dışı.
13. **Katılıyorum.** `requirements.txt` ve `pyproject.toml` notları güncellendi. Tahmini paket sürümleri eklenmedi; tam sürüm sabitlemesi Colab manifestinden sonra yapılacak.
14. **Katılıyorum.** Notebook'ta `git rev-parse` ve pytest stdout/stderr açıkça yazdırılıyor. `GITHUB_OWNER` placeholder'ı korundu. Kurulum sonrası runtime yeniden başlarsa notebook'u baştan çalıştırma uyarısı eklendi.
15. **Katılıyorum.** `docs/decision_register.md` tek yetkili kayıt olarak belirlendi ve sohbet içi eski kısa adları eşleyen tablo eklendi. Eski “OPEN-001 = akış” ifadesi `OPEN-DECISION-016`'ya; `OPEN-DECISION-001` ise kilitli fiziksel sızıntı temsiline eşlendi.

## İşlenen kararlar ve kalan açık alt kararlar

### A1 — OPEN-DECISION-012: Zavg politikası
- **Seçim:** A — iki segmentte sabit `Zavg=0.8065`.
- **Durum:** Politika alt kararı kapandı. Genel OPEN-DECISION-012, Colab sayısal doğrulaması tamamlanana kadar açık.
- **Gerekçe/sınırlılık:** v1'i sade tutar; değer evrensel literatür sabiti değil, türetilmiş sadeleştirici varsayımdır. Mutlak basınçlar Z varsayımına duyarlı olabilir.

### A2 — OPEN-DECISION-016: Model akış girdisi
- **Seçim:** `Qin` ve `Qout` ayrı gözlenen kanallar olarak onaylı pilot adayıdır; türetilmiş `Qin-Qout` farkı ana girdiye otomatik eklenmeyecek.
- **Durum:** Açık; önceden sabitlenmiş validation koşularında pilot karşılaştırması ve gözlenebilirlik kontrolü bekleniyor.
- **Kural:** `Q_leak`, severity, senaryo ID ve diğer ground-truth-only alanlar model girdisi olmayacak. Simülatörde `Qin-Qout=Q_leak` olması, farkın görevi yapay biçimde kolaylaştırabileceği anlamına gelir.

### A3 — OPEN-DECISION-006: Kademeli senaryo etiketleri
- **Seçim:** Zaman/faz temelli etiket baseline'ı onaylandı: 0–6h normal, 6–12h ramp/early-warning, 12–18h critical hold, 18–24h post. Şiddet temelli etiketlemeye geçilmiyor; özellikle drift için kaynakla gerekçelendirilmiş eşik yok.
- **Durum:** Baseline onaylı; post-fazın üç sınıflı kalibrasyondaki işlenişi açık alt karar.
- **Bekleyen seçim:** post'u normal saymak, W=16 history flush tamamlanana kadar kalibrasyondan çıkarmak veya ayrı recovery sınıfı yapmak. Seçim yapılmadan post etiketleme kodlanmayacak.

### A4 — OPEN-DECISION-021: Koşular arası değişkenlik
- **Seçim:** B — bağımsız gürültü tohumu + talep profilinde 0–24 saat faz kaydırması; talep genliği ±%5 olarak sabit.
- **Durum:** Politika kapalı `design-choice`; manifest uygulama kontrolü Phase 3'te yapılacak. Literatürden alınmış fiziksel sabit veya gerçek operatör profili değildir.

### OPEN-DECISION-014: Gürültü varsayımları
- **Seçim:** pilot için geçici `explicit-assumption` değerleri onaylandı: basınç σ=5 kPa, debi σ=Q0'ın %0.5'i, sıcaklık σ=0.1 K.
- **Duyarlılık kontrolü:** tüm sigmaları birlikte 2× yap; diğer ayarları sabit tut.
- **Durum:** Açık; Colab pilotu ve duyarlılık sonuçları kaydedilip uygunluğu değerlendirilene kadar final fiziksel parametre olarak kilitlenmeyecek. Bunlar operatör sensör özellikleri değildir.

## Dosya değişiklikleri

Değişen/eklenen dosyalar (bu düzeltme turunda):
- `configs/simulation.yaml` — sabit Zavg seçimi, onaylı noise adayları, Qin/Qout pilot adayı ve run-phase jitter
- `configs/experiments.yaml` — OPEN-021 politikasının onaylı run variability tanımı
- `docs/decision_register.md` — A1/A4 politika kararları kapalı; A2/A3 baseline/pilot onaylı; OPEN-014 sonuç bekliyor
- `docs/thesis_method_contract.md` — parametre kanıt etiketleri audit ile eşitlendi
- `docs/parameter_source_audit.md` — noise ve Zavg statüleri güncellendi
- `docs/open_decision_closure_plan.md` — onaylanan kararlar ve kalan kanıt koşulları
- `docs/phase2_architecture_gate.md`, `docs/global_framework_audit.md`, `README.md` — Zavg kapanış koşulu tutarlı hâle getirildi
- `docs/phase3_correction_review_report.md` — kararlar ve test durumu raporlandı
- `notebooks/01_phase3_environment_and_weymouth_validation.ipynb` — seçilen sabit-Z varsayımıyla açıklamalar tutarlı hâle getirildi

Bu turda model eğitimi veya simülasyon üretim kodu eklenmedi; GitHub/Colab çalıştırması yapılmadı.

## Test ve doğrulama durumu

- YAML parse: `configs/*.yaml` dosyalarının tamamı başarıyla ayrıştırıldı.
- Notebook JSON parse: başarılı.
- `pyproject.toml` TOML parse: başarılı.
- pytest: **1 passed, 1 skipped**. Atlanan test gerçek `fluids` entegrasyon testidir; bu ortamda `fluids` bulunmadığı için atlandı. Bu **Colab Weymouth doğrulamasının geçtiği anlamına gelmez**.
- Kullanıcının yüklediği talimatta Claude ortamı için raporlanan `fluids==1.3.1`, Q0 ve P2 değerleri dışarıdan sağlanan test raporu olarak not edilmiştir; bu inceleme ortamında bağımsız yeniden üretilmiş sonuçlar değildir.
- GitHub remote ve Colab bağlantısı bu düzenleme adımında yapılmadı.


## Güncelleme özeti — 2026-10-16

- **A1 / OPEN-DECISION-012 politika alt kararı:** sabit Zavg=0.8065 seçildi ve politika tercihi kapatıldı. Genel OPEN-DECISION-012, Colab sayısal doğrulaması bitene kadar açık.
- **A2 / OPEN-DECISION-016:** Qin+Qout ayrı gözlenen kanallar pilot adayı olarak onaylandı; karar pilot karşılaştırmasına kadar açık.
- **A3 / OPEN-DECISION-006:** zaman/faz etiketleri onaylandı; post-fazın üç sınıflı kalibrasyondaki işlenişi açık alt karar olarak kaldı.
- **A4 / OPEN-DECISION-021:** bağımsız noise seed + 0–24 saat demand-phase jitter seçildi; politika kapalı, manifest uygulaması kontrol edilecek.
- **OPEN-DECISION-014:** σ değerleri ve 2× duyarlılık kontrolü geçici explicit assumptions olarak onaylandı; sonuçlar gelene kadar OPEN.
- **OPEN-016 dil düzeltmesi:** teknik riski “görevi yapay biçimde kolaylaştırma” olarak ifade ettim.
- **Literatür etiketleri:** contract, `parameter_source_audit.md` sınıflandırmasına uyarlandı; doğrulanmamış sayısal parametreler literatürden kesin alınmış gibi sunulmuyor.


## Bu turdaki düzeltmeler ve OPEN-006 post-faz analizi

### Değişen dosyalar
- `src/natural_gas_anomaly_detection/simulation/weymouth_validation.py`: docstring ve `scope_warning` yalnızca açıklama metni olarak güncellendi; pass/fail mantığı değiştirilmedi.
- `docs/decision_register.md`: OPEN-006, post-faz fiziksel senaryosu ve etiketleme alt kararı açık olduğu için `OPEN decisions` bölümüne taşındı; OPEN-021, `Closed / locked decisions` altında toplandı. OPEN-006'ya Early sınıfı sınırlılık notu eklendi.
- `docs/limitations.md`: zaman-temelli Early etiketi ve sentetik veri sınırlılığı için tez dilinde not eklendi.

### OPEN-006 fiziksel post-faz seçenekleri — karar verilmedi, kodlanmadı

**Seçenek P1 — Anomali son şiddette sürer (18–24 h).**
- **Leak:** `Q_leak` 10% seviyesinde sürer; `Qin=Qout+Q_leak` dengesi devam eder.
- **Drift:** Sensör drift'i 18. saatte ulaşılan son offset'te kalır; ölçüm normale sıfırlanmaz.
- **Lead time / OPEN-015:** `t_critical` 12. saatteki önceden belirlenmiş kritik uç nokta olarak kalır. `LeadTime=t_critical-t_detect`; 18–24 h, kritik noktadan sonraki hold/izleme süresidir, yeni lead-time başlangıcı değildir.
- **T1/T2:** Post pencerelerini `normal` etiketlemek fiziksel ground truth ile çelişir. En tutarlı seçenek `critical` etiketini 24. saate kadar sürdürmektir. W=16 geçmişini boşaltmak bu durumda fiziksel anomaliyi bitirmediği için normal etiket gerekçesi oluşturmaz.
- **OPEN-017:** İlk T1 aşımı yine tespit olayıdır; persistence filtresi eklenmez. Anomali sürerken tek bir crossing tespit zamanı olarak kalır; normal koşularda point-level FPR ve en az bir alarm veren normal koşu oranı raporlanır.

**Seçenek P2 — Anomali 18. saatte biter ve sistem/sensör normale döner.**
- **Leak:** 18. saatte `Q_leak` sıfırlanır ve fiziksel işletim normal senaryoya döner.
- **Drift:** 18. saatte drift/bias sıfırlanır veya sensör yeniden kalibre edilerek ölçüm normale döner. Bu, açıkça tanımlanması gereken bir senaryo varsayımıdır.
- **Lead time / OPEN-015:** `t_critical` yine 12. saat olarak kalır; `LeadTime=t_critical-t_detect` geriye dönük değişmez. Post-fazdaki recovery süresi, kritik noktadan önceki erken tespit süresine eklenmez.
- **T1/T2:** W=16 dört saatlik geçmiş taşıdığı için 18. saatin hemen sonrasındaki pencereler hâlâ anomali geçmişi içerir. Bunları doğrudan `normal` etiketlemek skor/etiket uyuşmazlığı yaratabilir. En sade tutarlı seçenek, normal etikete geçmeden önce bu geçiş pencerelerini üç-sınıflı kalibrasyondan dışlamaktır. `recovery` sınıfı da fiziksel olarak anlamlı olabilir ama yeni sınıf ve kalibrasyon kuralı gerektirir.
- **OPEN-017:** İlk T1 aşımı tespit zamanı olmaya devam eder; post-fazdaki ek crossing'ler ilk tespiti değiştirmez. Anomali bittikten sonra skorlar hâlâ yüksek kalırsa, normal kabul edilen pencerelerde alarm/FPR artabilir; bu risk raporlanmalı, primary persistence kuralı değiştirilmemelidir.

**Seçenek P3 — Leak biter ama boru durumu kademeli döner / drift kademeli sıfırlanır.** Bu ayrı bir dinamik dönüş profili varsayar. Leak için basınç/akışın normale dönüş eğrisi; drift için offset'in sıfıra iniş süresi ayrıca tanımlanır. `OPEN-015` gereği lead time yine önceden belirlenmiş kritik nokta 12. saate göre hesaplanır. T1/T2 etiketi dönüş tamamlanana kadar normal olamaz; geçiş penceresini dışlama veya recovery sınıfı, dönüş süresi tanımlandıktan sonra seçilebilir. `OPEN-017` bir crossing'i olay saymaya devam eder. Yeni dönüş eğrisi ve süre parametreleri kapsamı büyüteceğinden şimdilik kodlanmamalıdır.

**Seçenek P3 — Sızıntı biter ama boru basıncı yeni kararlı duruma kademeli döner / drift kalibrasyonla kademeli sıfırlanır.** Bu ayrı bir dinamik dönüş profili varsayar. Lead-time tanımı yine kritik noktaya bağlı kalabilir, fakat dönüş dinamiği yeni parametreler ve fiziksel gerekçe gerektirir. T1/T2 etiketlemesi için normal, geçiş penceresini dışlama veya recovery arasında seçim ancak dönüş süresi tanımlandıktan sonra yapılabilir. Şimdilik yeni dönüş eğrisi kodlanmamalıdır.

### Leak ve drift için etiketleme eşlemesi
| Fiziksel senaryo | Normal say | W=16 geçiş penceresini dışla | Recovery sınıfı |
|---|---|---|---|
| P1: son anomali şiddeti sürer | **Tutarsız** | Sadece sınıf geçişi/kalibrasyon dışlama gerekçesi varsa; varsayılan çözüm değil | Gereksiz; fiziksel recovery yok |
| P2: anomali biter ve normale döner | İlk geçiş pencereleri için **tutarsız**; pencere geçmişi hâlâ anomalili | **En sade tutarlı seçenek** | Tutarlı olabilir ama yeni sınıf gerektirir |
| P3: kademeli dönüş | Dönüş tamamlanmadan **tutarsız** | Dönüş süresi tanımlanırsa tutarlı | Tutarlı olabilir ama kapsamı genişletir |

### En sade öneri (onay bekliyor)
Yeni sınıf eklememek için, fiziksel senaryo olarak P2 seçilecekse post-fazın ilk W=16 geçmişi temizlenene kadar üç sınıflı kalibrasyondan dışlanması önerilir; sonrasında yalnızca fiziksel/sensör durumunun gerçekten normale döndüğü doğrulanmış pencereler normal etiketlenir. Ancak leak ve drift için “biter ve normale döner” davranışı kullanıcı tarafından seçilmeden bu öneri uygulanmayacak. P1 seçilirse bunun yerine post-faz critical hold devamı olarak ele alınmalıdır.

### Kod/config değişikliği yapılmadan önce eklenecek yerler
- `docs/decision_register.md` → OPEN-006 altında, fiziksel post-faz davranışını kullanıcı seçimi olarak kaydet; ardından etiketleme alt kararını kaydet.
- `configs/experiments.yaml` → `thresholds.three_class` altında `label_timeline` veya `post_phase_policy` alanı eklenmesi ancak karar sonrası; `run_variability` veya alarm eşik mantığına dokunmadan. Önerilen gelecekteki alanlar yalnızca şema taslağıdır, mevcut config'e eklenmedi: `post_phase_physics: <user-selected-option>` ve `post_phase_label_policy: <user-selected-option>`.
- Fiziksel davranış ayrıca `configs/simulation.yaml` içinde faz zaman çizelgesi/olay enjeksiyon tanımına yansıtılmalıdır; ancak kullanıcı seçmeden hiçbir seçenek kodlanmayacaktır.

### Doğrulama
Bu turda Weymouth testlerinin pass/fail mantığı değiştirilmedi. Bu çalışma ortamında `fluids` kurulu olmadığı için entegrasyon testi yeniden çalıştırılırsa atlanabilir; kullanıcı tarafından raporlanan Claude sonucu (2/2 test ve `all_passed=True`) bağımsız olarak yeniden üretilmiş sayılmaz.
