# -*- coding: utf-8 -*-

import requests
import sys
import os

# --- !!! UYARI: GÜVENLİ DEĞİL !!! ---
# Bu URL, kullanıcı adınızı ve şifrenizi herkesin görebileceği
# şekilde içerir. Bu dosyayı herkese açık bir GitHub
# deposuna yüklerseniz, hesabınız çalınabilir.
# --- !!! UYARI: GÜVENLİ DEĞİL !!! ---
PLAYLIST_URL = "http://plusjustone.xyz:8080/get.php?username=b4h8feZC&password=cRzefU4&type=m3u_plus&output=m3u"

# İndirilen içeriğin kaydedileceği dosya adı
OUTPUT_FILENAME = "indirilen_playlist.m3u"

def fetch_and_save_m3u():
    """
    Doğrudan (hardcoded) URL'den M3U playlist'ini çeker ve bir dosyaya kaydeder.
    """
    print(f"Playlist çekiliyor (Güvensiz Yöntem)...")
    
    try:
        # Belirtilen URL'ye GET isteği gönder
        response = requests.get(PLAYLIST_URL, timeout=20)
        
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
            print("Erişim reddedildi (401 Unauthorized). URL'deki kullanıcı adı/şifreyi kontrol edin.", file=sys.stderr)
        
    except requests.exceptions.ConnectionError as errc:
        print(f"\n[HATA] Bağlantı Hatası: {errc}", file=sys.stderr)
    except requests.exceptions.Timeout as errt:
        print(f"\n[HATA] Zaman Aşımı: {errt}", file=sys.stderr)
    except Exception as e:
        print(f"\n[BEKLENMEDİK HATA]: {e}", file=sys.stderr)
        sys.exit(1)

# Betiği ana program olarak çalıştır
if __name__ == "__main__":
    fetch_and_save_m3u()