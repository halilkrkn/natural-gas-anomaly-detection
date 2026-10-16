# Faz 3 — GitHub + Colab + Weymouth sayısal doğrulaması

## Durum ve sınırlar

Bu belge bir kontrol protokolüdür; GitHub deposu oluşturulduğunu, Colab kurulumunun çalıştığını veya Weymouth testlerinin geçtiğini tek başına kanıtlamaz. Sonuçlar gerçek hesap/çalışma ortamından alınmalı ve karar defterine eklenmelidir.

## A. GitHub deposu

1. GitHub hesabında `natural-gas-anomaly-detection` adlı **private** depo oluştur.
2. Bu proje klasöründeki dosyaları ilk commit olarak `main` dalına aktar. Depo oluştururken ikinci bir README veya `.gitignore` üretme; bu klasörde zaten var.
3. Secret, token, `.env`, ham veri, sentetik koşu CSV'leri, checkpoint ve büyük tahmin dosyalarını commit etme.
4. `git status --short`, `git log -1 --oneline` ve `git remote -v` ile depo durumunu doğrula.
5. Antigravity MCP bağlantısı kullanılıyorsa önce read-only depo görünürlüğünü ve araç listesini doğrula. MCP bağlantısı olduğunu yalnızca yapılandırma dosyasına bakarak varsayma.

## B. Google Colab

1. `notebooks/01_phase3_environment_and_weymouth_validation.ipynb` dosyasını GitHub üzerinden Colab'da aç veya Colab'da yeni notebook oluşturup dosyayı içeri al.
2. Notebook içindeki `GITHUB_OWNER` değerini kendi GitHub kullanıcı/organizasyon adınla değiştir. Private repo clone işlemi için Colab Secrets'a `GITHUB_TOKEN` adıyla salt `Contents: Read` yetkisine sahip secret eklenebilir. Token notebook hücresine veya Git'e yazılmaz.
3. Google Drive'ı bağla; raporlar `/content/drive/MyDrive/natural-gas-anomaly-detection/reports/metrics/` altında saklansın.
4. `python -m pip install -r requirements.txt` ve `python -m pip install -e .` komutlarını çalıştır.
5. `python -m pytest -q` çalıştır. `test_weymouth_validation.py` **skip olmamalı**; `fluids` eksikse Faz 3 doğrulanmış değildir.
6. `scripts/capture_environment.py` ile gerçek Python/platform/paket sürümlerini kaydet.

## C. Weymouth kontrolleri

`scripts/run_weymouth_validation.py` ve `notebooks/01_phase3_environment_and_weymouth_validation.ipynb` şu kontrolleri gerçek `fluids.compressible.Weymouth` fonksiyonuyla yapar:

1. Resmî belgede verilen örneğin aynı parametrelerle yeniden üretimi.
2. Proje nominal noktasında `Q0` hesabı ve `Q0` ile `P2` geri çözüm kontrolü.
3. Nominal akışın ±%5'i için pozitif/sonlu downstream pressure ve doğru monotonluk kontrolü. ±%5 burada tasarım varsayımıdır.
4. Midpoint iki-segment smoke testinde `Qin=Qout+Qleak`, pozitif basınçlar ve basınç sıralaması.

Tüm çağrılarda proje parametreleri isimli argümanlarla iletilir. Fonksiyonun kendisi yeniden yazılmaz. Resmî örnekte dokümantasyondaki varsayılan referans sıcaklığının kullanılması API karşılaştırması içindir; tez baseline'ında `Ts=288.15 K` açıkça geçirilir.

## D. OPEN-DECISION-012 kapanış standardı

Bu testlerin geçmesi sadece kütüphane API'si ve temel sayısal smoke-test davranışını doğrular. Kararı tek başına kapatmaz. Kapanış öncesi:

- Kurulu `fluids` sürümü ve JSON raporu saklanmalı.
- Nominal geri çözüm hatası ve ±%5 akış sonuçları incelenmeli.
- İki segment için `Zavg` hesabının nasıl uygulandığı açıkça belgelenmeli; burada kullanılan sabit nominal `Zavg`, yalnızca smoke-test varsayımıdır.
- Sızıntı modelinin basitleştirilmiş kütle dengesi yaklaşımı olduğu ve gerçek transient/orifice leak modeli olmadığı açıkça kayıt altına alınmalı.
- `docs/decision_register.md` ve etkilenen konfigürasyon/kod dosyaları kanıta göre güncellenmeli.

## E. Faz 3 kabul listesi

- [ ] Gerçek GitHub deposu ve ilk commit mevcut.
- [ ] Secret/ham veri ve büyük dosya politikası doğrulandı.
- [ ] Colab'da `requirements.txt` kuruldu.
- [ ] Colab'da `pip install -e .` başarılı oldu.
- [ ] `pytest -q` başarılı; Weymouth integration test skip değil.
- [ ] Gerçek ortam sürüm manifesti Drive'a kaydedildi.
- [ ] Dokümantasyon örneği, nominal geri çözüm, demand-bound ve iki segment smoke testi raporlandı.
- [ ] `OPEN-DECISION-012` ya gerekli kanıtlarla kapatıldı ya da eksik kanıtları açıkça belirtilerek OPEN bırakıldı.

Geçiş kapısı bu listenin kanıta dayalı denetiminden sonra değerlendirilir. Bu dosyanın veya notebook'un oluşturulmuş olması geçiş kapısını açmaz.
