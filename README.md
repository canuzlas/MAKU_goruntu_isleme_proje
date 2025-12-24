# MAKU Görüntü İşleme Projesi - Mesafe Ölçer

Bu proje, görüntü işleme teknikleri kullanarak kamera karşısındaki nesne veya yüzün kameraya olan uzaklığını gerçek zamanlı olarak ölçmeyi amaçlayan bir Python uygulamasıdır. Proje, Burdur Mehmet Akif Ersoy Üniversitesi (MAKÜ) görüntü işleme çalışmaları kapsamında geliştirilmiştir.

## 📂 Proje Yapısı

- **mesafe_olcer.py**: Projenin ana çalışma dosyasıdır. Görüntü işleme ve mesafe hesaplama algoritmalarını içerir.
- **ayarlar.json**: Programın konfigürasyon (kamera ayarları, kalibrasyon değerleri vb.) dosyasını barındırır.
- **face_map.jpg**: Yüz tanıma veya referans noktaları için kullanılan harita/görsel dosyasıdır.
- **assets/**: Proje için gerekli ek görsellerin veya kaynakların bulunduğu klasör.
- **requirements.txt**: Projenin çalışması için gerekli Python kütüphanelerinin listesi.

## 🚀 Kurulum

Projeyi bilgisayarınıza kurmak ve çalıştırmak için aşağıdaki adımları izleyebilirsiniz.

### 1. Projeyi Klonlayın
```bash
git clone [https://github.com/canuzlas/MAKU_goruntu_isleme_proje.git](https://github.com/canuzlas/MAKU_goruntu_isleme_proje.git)
cd MAKU_goruntu_isleme_proje
2. Gerekli Kütüphaneleri Yükleyin
Projenin çalışması için gerekli olan bağımlılıkları (OpenCV, cvzone vb.) yüklemek için:

Bash

pip install -r requirements.txt
⚙️ Kullanım
Kurulum tamamlandıktan sonra uygulamayı başlatmak için terminal veya komut satırında aşağıdaki komutu çalıştırın:

Bash

python mesafe_olcer.py
Ayarlar
Eğer ölçüm hassasiyetini değiştirmek veya kamera parametrelerini güncellemek isterseniz ayarlar.json dosyasını bir metin editörü ile düzenleyebilirsiniz.

🛠️ Kullanılan Teknolojiler
Python 3

OpenCV: Görüntü işleme işlemleri için.

JSON: Veri yapılandırması ve ayarlar için.

🤝 Katkıda Bulunma
Projeye katkıda bulunmak isterseniz, lütfen bir "Fork" oluşturun ve değişikliklerinizi "Pull Request" ile gönderin.

📝 Lisans
Bu proje açık kaynaklıdır ve eğitim amaçlı geliştirilmiştir.
