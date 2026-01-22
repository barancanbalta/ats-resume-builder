# 📄 ATS-Friendly Resume Builder

> **Streamlit tabanlı, ATS uyumlu CV oluşturma ve analiz platformu**

Profesyonel CV'nizi kolayca oluşturun, optimize edin ve iş ilanlarına uyumluluğunu analiz edin. Türkçe ve İngilizce dil desteği ile PDF ve DOCX formatlarında çıktı alın.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow.svg)](https://github.com)

## ⚠️ Proje Durumu

**🚧 Bu proje aktif geliştirme aşamasındadır.**

Mevcut sürüm temel işlevleri içermektedir ancak hala geliştirmeler devam etmektedir. Kararlı sürüm için lütfen release notlarını takip edin.

## ✨ Özellikler

### 🎯 Çekirdek Özellikler
- **Çok Dilli Destek**: Türkçe ve İngilizce arayüz ve CV oluşturma
- **ATS Optimizasyonu**: Başvuru takip sistemlerine uyumlu CV formatları
- **3 Profesyonel Şablon**: Klasik, Modern ve Akademik tasarımlar
- **Otomatik Çeviri**: Türkçe CV'nizi otomatik olarak İngilizceye çevirin
- **İş İlanı Analizi**: CV'nizin iş ilanlarıyla uyumluluğunu hesaplama

### 📊 Analiz Araçları
- **ATS Anahtar Kelime Analizi**: İş ilanındaki kritik kelimeleri tespit etme
- **Eşleşme Skoru**: CV ve iş ilanı arasındaki uyumluluğu yüzdesel gösterme
- **Eksik Beceriler**: CV'nizde bulunmayan önemli becerileri belirleme
- **Canlı Önizleme**: CV'nizi oluşturmadan önce görüntüleyin

### 📁 Çıktı Formatları
- **PDF**: 3 farklı şablon (Klasik, Modern, Akademik)
- **DOCX**: ATS uyumlu Word formatı
- **JSON**: Veri yedekleme ve geri yükleme

## 🚀 Kurulum

### Gereksinimler
- Python 3.8 veya üzeri
- pip paket yöneticisi

### Adım 1: Repository'yi klonlayın
```bash
git clone https://github.com/kullanici-adiniz/ats-resume-builder.git
cd ats-resume-builder
```

### Adım 2: Gerekli paketleri yükleyin
```bash
pip install -r requirements.txt
```

### Adım 3: Kullanıcı verisi oluşturun
```bash
# Örnek dosyayı kopyalayın
cp user_data.example.py user_data.py

# user_data.py dosyasını düzenleyin ve kendi bilgilerinizi ekleyin
```

### Adım 4: Uygulamayı çalıştırın
```bash
streamlit run app.py
```

Tarayıcınızda `http://localhost:8501` adresine gidin.

## 📖 Kullanım

### 1️⃣ Dil Seçimi
Uygulama açıldığında Türkçe veya İngilizce dil seçimi yapın.

### 2️⃣ Kişisel Bilgiler
- Ad Soyad, e-posta, telefon
- LinkedIn ve GitHub profil linkleri
- Profesyonel özet

### 3️⃣ İş Deneyimi
- Pozisyon, şirket, lokasyon
- Başlangıç ve bitiş tarihleri
- Başarılarınızı maddeler halinde ekleyin

### 4️⃣ Eğitim Bilgileri
- Üniversite, bölüm, mezuniyet tarihi
- GPA ve sıralama bilgileri

### 5️⃣ Projeler ve Sertifikalar
- Kişisel/profesyonel projeler
- Aldığınız eğitim ve sertifikalar

### 6️⃣ Beceriler
- Programlama dilleri
- Framework ve kütüphaneler
- Araçlar ve yazılımlar
- Yabancı diller

### 7️⃣ İş İlanı Analizi (Opsiyonel)
İş ilanını yapıştırarak CV'nizin uyumluluğunu analiz edin.

### 8️⃣ Şablon Seçimi ve İndirme
CV şablonunu seçin ve PDF/DOCX formatında indirin.

## 🏗️ Proje Yapısı

```
ats-resume-builder/
├── app.py                      # Ana uygulama dosyası
├── user_data.example.py        # Örnek kullanıcı verisi
├── user_data.py               # Kişisel veri (gitignore'da)
├── requirements.txt           # Python bağımlılıkları
├── .gitignore                # Git ignore kuralları
│
├── cv_generator.py           # PDF oluşturma modülü
├── cv_generator_docx.py      # DOCX oluşturma modülü
├── translator_utils.py       # Çeviri yardımcıları
├── matcher_utils.py          # İş ilanı eşleştirme
├── localization.py           # Dil dosyaları
├── ui_components.py          # UI bileşenleri
├── pdf_utils.py             # PDF önizleme
│
└── fonts/                   # Font dosyaları
    ├── DejaVuSans.ttf
    └── ...
```

## 🔒 Güvenlik ve Gizlilik

**ÖNEMLİ**: Bu uygulama kişisel verilerinizi içerir. GitHub'a yüklerken dikkat edin!

### Korunan Dosyalar (.gitignore ile)
- `user_data.py` - Kişisel bilgileriniz
- `CV_*.pdf` / `CV_*.docx` - Oluşturulan CV'ler
- `Resume_*.pdf` / `Resume_*.docx` - İngilizce CV'ler
- Tüm test dosyaları ve çıktılar

### Güvenli Kullanım
1. **ASLA** `user_data.py` dosyasını GitHub'a yüklemeyin
2. **ASLA** oluşturduğunuz CV dosyalarını commit etmeyin
3. `.gitignore` dosyasını silmeyin veya değiştirmeyin
4. Kendi fork'unuzu oluştururken "Private" seçeneğini kullanın

## 🛠️ Teknolojiler

- **Python 3.8+**: Ana programlama dili
- **Streamlit**: Web arayüzü framework'ü
- **FPDF2**: PDF oluşturma
- **python-docx**: Word belgeleri oluşturma
- **deep-translator**: Otomatik çeviri
- **Pandas**: Veri işleme

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen şu adımları izleyin:

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun

## 🐛 Bilinen Sorunlar ve Geliştirmeler

- [ ] Daha fazla CV şablonu eklenmesi
- [ ] Cover letter (ön yazı) oluşturma özelliği
- [ ] LinkedIn entegrasyonu
- [ ] Daha gelişmiş ATS analiz algoritmaları
- [ ] Çoklu dil desteği genişletilmesi

## 📧 İletişim

Sorularınız veya önerileriniz için:
- Issue açın
- Pull Request gönderin

---

⭐ **Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!**
