# GitHub repo oluşturma ve ilk push

Bu klasörün içinde `.git` dizini yoktur; ZIP bir **repo içeriği** paketidir. GitHub hesabında depoyu oluşturup aşağıdaki adımlarla yerel çalışma klasörünü bağla.

## GitHub arayüzü veya yetkili MCP üzerinden

1. `natural-gas-anomaly-detection` adında **private** bir depo oluştur.
2. Depo oluştururken README, `.gitignore` veya lisans dosyasını otomatik ekleme; bu proje bunları zaten içeriyor.
3. Antigravity içindeki GitHub MCP kullanılacaksa repo oluşturma/yazma işlemlerinden önce mevcut izinleri ve aktif araç listesini kontrol et. Bu belge MCP'nin bağlandığını varsaymaz.

## Yerel klasörden ilk push

ZIP'i açtıktan sonra terminalde proje köküne geç:

```bash
git init -b main
git add .
git status --short
git diff --cached --stat
```

`git status` çıktısında `.env`, token, raw/synthetic veri, model ağırlığı veya büyük sonuç dosyaları olmadığını kontrol ettikten sonra:

```bash
git commit -m "Add Phase 3 research scaffold"
git remote add origin https://github.com/<GITHUB_OWNER>/natural-gas-anomaly-detection.git
git push -u origin main
```

`<GITHUB_OWNER>` yer tutucusunu kullanıcı/organizasyon adınla değiştir. GitHub kimlik doğrulamasını GitHub CLI/credential manager veya Antigravity'deki onaylı MCP bağlantısı üzerinden yap; token'ı komuta, dosyaya ya da notebook'a yapıştırma.

## Başarı kanıtı

- GitHub'da repo sayfası açılıyor.
- `main` dalında ilk commit ve proje dosyaları var.
- Son commit hash'i not edildi.
- `git status --short` boş veya yalnızca bilerek yerel bırakılmış dosyaları gösteriyor.
- Secret/veri güvenliği gözden geçirildi.
