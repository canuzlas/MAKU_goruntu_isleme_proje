import cv2
import mediapipe as mp
import pygame
import os
import sys
import time
import json

GERCEK_GOZ_ARALIGI = 6.3  # İnsanın iki göz bebeği arası ortalama mesafe (cm)
ODAK_UZAKLIGI = 650       # w:640 h480 için kalibre edilmiş odak uzaklığı (focal length) (reddit)
SES_DOSYASI = os.path.join(os.path.dirname(__file__), "assets/uzaklas.mp3")
AYAR_DOSYASI = os.path.join(os.path.dirname(__file__), "ayarlar.json")
MOLA_SURESI = 20 * 60     # 20 dakikada bir mola hatırlatması (saniye)

VARSAYILAN_AYARLAR = {
    "uyari_mesafesi": 30,
    "ses_acik": True
}

def ayarlari_oku():
    """Ayarları dosyadan oku, yoksa varsayılanları döndür"""
    try:
        with open(AYAR_DOSYASI, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return VARSAYILAN_AYARLAR.copy()

def ayarlari_kaydet(uyari_mesafesi, ses_acik):
    """Ayarları dosyaya kaydet"""
    ayarlar = {
        "uyari_mesafesi": uyari_mesafesi,
        "ses_acik": ses_acik
    }
    with open(AYAR_DOSYASI, 'w') as f:
        json.dump(ayarlar, f, indent=2)

# Ayarları yükle
ayarlar = ayarlari_oku()
uyari_mesafesi = ayarlar["uyari_mesafesi"]
ses_acik = ayarlar["ses_acik"]
print(f"Ayarlar yüklendi: Uyarı mesafesi={uyari_mesafesi}cm, Ses={'Açık' if ses_acik else 'Kapalı'}")

pygame.mixer.init()
try:
    uyari_sesi = pygame.mixer.Sound(SES_DOSYASI)
except FileNotFoundError:
    print(f"HATA: '{SES_DOSYASI}' bulunamadı!")
    sys.exit()

mesafe_listesi = []       
baslangic_zamani = time.time()  
son_mola_zamani = time.time()  

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    refine_landmarks=True 
)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Program çalışıyor...")
print("Kontroller: 'q' = Çık | '+' = Mesafe artır | '-' = Mesafe azalt | 'm' = Ses aç/kapa")

while True:
    basarili, kare = cap.read()
    if not basarili:
        break

    kare = cv2.flip(kare, 1)
    
    rgb_kare = cv2.cvtColor(kare, cv2.COLOR_BGR2RGB)
    
    sonuclar = face_mesh.process(rgb_kare)
    
    gecen_sure = time.time() - baslangic_zamani
    dakika = int(gecen_sure // 60)
    saniye = int(gecen_sure % 60)
    
    mola_uyarisi = False
    if time.time() - son_mola_zamani >= MOLA_SURESI:
        mola_uyarisi = True

    if sonuclar.multi_face_landmarks:
        for yuz_noktalari in sonuclar.multi_face_landmarks:
            

            sol_iris = yuz_noktalari.landmark[468]
            sag_iris = yuz_noktalari.landmark[473]

            h, w, _ = kare.shape
            x1, y1 = int(sol_iris.x * w), int(sol_iris.y * h)
            x2, y2 = int(sag_iris.x * w), int(sag_iris.y * h)

            piksel_mesafe = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
            
            mesafe_cm = (ODAK_UZAKLIGI * GERCEK_GOZ_ARALIGI) / piksel_mesafe
            
            mesafe_listesi.append(mesafe_cm)
            if len(mesafe_listesi) > 100:
                mesafe_listesi.pop(0)
            
            ortalama_mesafe = sum(mesafe_listesi) / len(mesafe_listesi)

            if mesafe_cm < uyari_mesafesi:
                durum = "COK YAKIN!"
                renk = (0, 0, 255) # Kırmızı
                
                if ses_acik and not pygame.mixer.get_busy():
                    uyari_sesi.play()
            else:
                durum = "GUVENLI"
                renk = (0, 255, 0) # Yeşil

        
            cv2.circle(kare, (x1, y1), 3, (0, 255, 255), -1)
            cv2.circle(kare, (x2, y2), 3, (0, 255, 255), -1)
            
            cv2.putText(kare, f"Mesafe: {int(mesafe_cm)} cm", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, renk, 2)
            cv2.putText(kare, f"Durum: {durum}", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, renk, 2)
            cv2.putText(kare, f"Ort: {int(ortalama_mesafe)} cm", (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
            # Ekran başında geçen süre
            cv2.putText(kare, f"Sure: {dakika:02d}:{saniye:02d}", (480, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Uyarı mesafesi göstergesi
            ses_durumu = "ON" if ses_acik else "OFF"
            cv2.putText(kare, f"Uyari: {uyari_mesafesi}cm | Ses: {ses_durumu}", (30, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            
            # Mola hatırlatması
            if mola_uyarisi:
                cv2.rectangle(kare, (100, 200), (540, 280), (0, 165, 255), -1)
                cv2.putText(kare, "MOLA ZAMANI!", (150, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)

            cv2.imshow('Mesafe Olcer', kare)

    # Klavye kontrolleri
    tus = cv2.waitKey(5) & 0xFF
    
    if tus == ord('q'):  # Çık
        break
    elif tus == ord('+') or tus == ord('='):  # Uyarı mesafesini artır
        uyari_mesafesi += 5
        ayarlari_kaydet(uyari_mesafesi, ses_acik)
        print(f"Uyarı mesafesi: {uyari_mesafesi} cm (kaydedildi)")
    elif tus == ord('-'):  # Uyarı mesafesini azalt
        uyari_mesafesi = max(10, uyari_mesafesi - 5)
        ayarlari_kaydet(uyari_mesafesi, ses_acik)
        print(f"Uyarı mesafesi: {uyari_mesafesi} cm (kaydedildi)")
    elif tus == ord('m'):  # Ses aç/kapa
        ses_acik = not ses_acik
        ayarlari_kaydet(uyari_mesafesi, ses_acik)
        print(f"Ses: {'Açık' if ses_acik else 'Kapalı'} (kaydedildi)")
    elif tus == ord('r'):  # Mola zamanlayıcısını sıfırla
        son_mola_zamani = time.time()
        print("Mola zamanlayıcısı sıfırlandı!")

# Çıkışta ayarları kaydet
ayarlari_kaydet(uyari_mesafesi, ses_acik)
print("Ayarlar kaydedildi!")

cap.release()
cv2.destroyAllWindows()

# çalıştırmak için terminalde:
# 1) pip install -r requirements.txt
# 2) .venv/bin/python mesafe_olcer.py