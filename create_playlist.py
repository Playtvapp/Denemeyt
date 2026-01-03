# -*- coding: utf-8 -*-

import requests
import sys
import os  # Ortam değişkenlerini okumak için eklendi

# Kaydedilecek dosya adı
OUTPUT_FILENAME = "indirilen_playlist.m3u"

def fetch_and_save_m3u():
    """
    Ortam değişkenlerinden alınan bilgilerle M3U playlist'ini çeker
    ve bir dosyaya kaydeder.
    """
    
    # Adım 1: Hassas bilgileri GitHub Secrets'tan (ortam değişkenleri aracılığıyla) al
    # GitHub Actions workflow'unda bu değişkenler 'env:' bloğu ile sağlanacak.
    username = os.environ.get("VOD_USERNAME")
    password = os.environ.get("VOD_PASSWORD")
    
    # Bilgilerin eksik olup olmadığını kontrol et
    if not username or not password:
        print("[HATA] VOD_USERNAME veya VOD_PASSWORD ortam değişkenleri ayarlanmamış.", file=sys.stderr)
        print("Lütfen GitHub Depo Ayarları > Secrets and variables > Actions kısmından bu sırları ekleyin.", file=sys.stderr)
        sys.exit(1) # Hata koduyla çık

    # Adım 2: URL'yi güvenli bilgilerle dinamik olarak oluştur
    base_url = "http://plusjustone.xyz:8080"
    params = {
        "username": username,
        "password": password,
        "type": "m3u_plus",
        "output": "m3u"
    }
    
    # requests kütüphanesi, 'params' sözlüğünü URL'ye güvenli bir şekilde ekler
    # (örn: https://.../get.php?username=...&password=... vb.)

    print(f"Playlist çekiliyor: {base_url}?username={username}&type=m3u_plus (Şifre gizlendi)")
    
    try:
        # Adım 3: İsteği gönder
        response = requests.get(base_url, params=params, timeout=20)
        
        # HTTP hata kodlarını (4xx, 5xx) kontrol et
        response.raise_for_status()
        
        # Yanıtın metin içeriğini al (M3U içeriği)
        playlist_content = response.text
        
        # İçeriği yerel bir dosyaya yaz
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            f.write(playlist_content)
            
        print(f"\nBaşarılı!")
        print(f"Playlist '{OUTPUT_FILENAME}' dosyasına başarıyla kaydedildi.")

    except requests.exceptions.HTTPError as errh:
        print(f"\n[HATA] HTTP Hatası: {errh}", file=sys.stderr)
        if response.status_code == 401:
            print("Erişim reddedildi (401 Unauthorized). Lütfen GitHub Secrets'taki kullanıcı adı/şifreyi kontrol edin.", file=sys.stderr)
        
    except requests.exceptions.ConnectionError as errc:
        print(f"\n[HATA] Bağlantı Hatası: {errc}", file=sys.stderr)
    except requests.exceptions.Timeout as errt:
        print(f"\n[HATA] Zaman Aşımı: {errt}", file=sys.stderr)
    except Exception as e:
        print(f"\n[BEKLENMEDİK HATA]: {e}", file=sys.stderr)
        sys.exit(1) # Genel hata durumunda da çık

# Betiği ana program olarak çalıştır
if __name__ == "__main__":
    fetch_and_save_m3u()