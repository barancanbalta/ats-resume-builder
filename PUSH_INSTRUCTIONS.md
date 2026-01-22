# 🚀 GitHub'a Push Yapma Kılavuzu

## Yöntem 1: GitHub CLI ile Push (Önerilen)

### Adım 1: GitHub CLI Kurulumu (Homebrew ile)

Terminal'de sırasıyla şu komutları çalıştırın:

```bash
# Homebrew'i kur (eğer yoksa)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# GitHub CLI'yi kur
brew install gh

# GitHub'a giriş yap (tarayıcı açılacak)
gh auth login
```

**gh auth login** komutunda:
- **? What account do you want to log into?** → GitHub.com
- **? What is your preferred protocol for Git operations?** → HTTPS
- **? Authenticate Git with your GitHub credentials?** → Yes
- **? How would you like to authenticate GitHub CLI?** → Login with a web browser

Tarayıcıda açılan sayfada kodu girin ve onaylayın.

### Adım 2: Push Yapın

```bash
cd "/Users/baran/Desktop/Github Portfolio/Resume Builder"
git push -u origin main
```

✅ **Tamamlandı!** Repository GitHub'da: https://github.com/barancanbalta/ats-resume-builder

---

## Yöntem 2: GitHub Desktop ile Push (En Kolay)

1. **GitHub Desktop'ı indirin**: https://desktop.github.com/
2. Uygulamayı açın ve GitHub hesabınızla giriş yapın
3. **File → Add Local Repository** seçin
4. Klasörü seçin: `/Users/baran/Desktop/Github Portfolio/Resume Builder`
5. **Publish repository** butonuna tıklayın
6. ✅ Bitti!

---

## Yöntem 3: Git Credential Helper (Manuel)

```bash
cd "/Users/baran/Desktop/Github Portfolio/Resume Builder"

# Credential helper'ı etkinleştir
git config --global credential.helper osxkeychain

# Remote'u HTTPS olarak ayarla
git remote set-url origin https://github.com/barancanbalta/ats-resume-builder.git

# Push yap
git push -u origin main
```

İlk push'ta GitHub kullanıcı adı ve şifrenizi soracak.
**Şifre yerine Personal Access Token kullanmalısınız:**
- Token oluşturun: https://github.com/settings/tokens
- "Generate new token (classic)"
- Scope: `repo` seçin
- Token'ı kopyalayın ve şifre yerine yapıştırın

---

## ✅ Push Başarılı mı Kontrol Edin

```bash
cd "/Users/baran/Desktop/Github Portfolio/Resume Builder"
git remote -v
git log --oneline -5
```

Tarayıcıda kontrol: https://github.com/barancanbalta/ats-resume-builder

---

## 🔒 Güvenlik Kontrolü

Push sonrası mutlaka kontrol edin:
- ❌ `user_data.py` görünmemeli
- ❌ CV_*.pdf dosyaları görünmemeli
- ❌ Resume_*.docx dosyaları görünmemeli
- ✅ `.gitignore` görünmeli
- ✅ `user_data.example.py` görünmeli
- ✅ `README.md` görünmeli

Eğer kişisel dosyalarınız görünüyorsa **HEMEN** bana haber verin!

