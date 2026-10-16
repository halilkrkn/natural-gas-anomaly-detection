# Faz 2 — Kısa Mimari Kontrol Kaydı

**Durum:** Faz C mimari kontrolü kullanıcı tarafından kabul edildi. Bu belge mimari kararların kısa özetidir; GitHub/Colab çalışırlığını veya nihai platform paketini doğruladığı iddiasında değildir.

## Kabul edilen modül sınırları

- `data/`: yükleme, şema, kalite kontrolleri ve deney/run bazlı split manifesti.
- `preprocessing/`: eksik veri işlemleri, StandardScaler ve causal windowing.
- `simulation/`: `fluids.compressible.Weymouth` çağrısı ve fiziksel koşu üretimi.
- `anomaly/`: fiziksel sızıntı senaryosu ile sensör ölçüm bias/drift enjeksiyonu.
- `features/`: klasik modeller için mean, standard deviation, min, max, slope.
- `models/`: IF, OCSVM, LOF, LSTM-AE, GRU-AE uygulamaları.
- `evaluation/`: skor yönü, validation-only eşik kalibrasyonu, metrikler, olay/lead-time analizi.
- `visualization/`: yalnızca sonuç grafikleri; model eğitimi veya eşik seçimi yapmaz.

## Kabul edilen dosya sorumlulukları

- `configs/data.yaml`: veri ve W=16 pencere baseline'ı.
- `configs/simulation.yaml`: fiziksel ve senaryo parametreleri; OPEN değerleri açık kalır.
- `configs/models.yaml`: Faz 1.5.9 v1.1 adayları; pilot kanıtı olmadan nihai değildir.
- `configs/experiments.yaml`: split, seed/tekrar, eşik ve metrik protokolü.
- `docs/decision_register.md`: küresel karar statüsünün otoriter kaydı.

## Notebook ve test sınırı

- Notebook: EDA, sıralı deney akışı, sonuç gösterimi ve rapor üretimi.
- `src/`: yeniden kullanılabilir algoritmalar; notebook içine kopyalanmaz.
- Birim testi: windowing, features, score direction, thresholds, data leakage invariants.
- Entegrasyon testi: gerçek fluids çağrısı, nominal pressure-flow round trip, iki-segment smoke check.
- Smoke testi: paket importu ve küçük veri üzerinde temel çalışabilirlik.

## Mimari ilkeler

1. Yeni framework veya gereksiz soyutlama ekleme.
2. `Weymouth` denklemini elle yeniden uygulama; resmî `fluids` fonksiyonuna ince adaptör uygula.
3. Fiziksel sızıntı ile sensör ölçüm arızasını ayrı uygulama katmanlarında tut.
4. Konfigürasyondaki sayı karar kapanışı değildir; kanıt ve decision register güncellemesi gerekir.
5. W=16 v1 tasarım baseline'ıdır. W=32 duyarlılık önerisi `SUPERSEDED` durumundadır.

## Açık sınırlar

- `OPEN-DECISION-012` gerçek Colab'da API/round-trip smoke testleri gerektirir. v1 için sabit `Zavg=0.8065` politikası seçilmiştir; sınırlılığı belgelenmelidir.
- Açık kararlar, kod/konfigürasyon varsayılanlarına bakılarak kapatılamaz.
- Bu mimari onayı GitHub deposunun var olduğu veya Colab kurulumunun geçtiği anlamına gelmez.
