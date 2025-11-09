# -*- coding: utf-8 -*-

import requests
import sys  # Hata mesajlarını standart hata çıkışına (stderr) yazdırmak için

# --- !!! ÇOK ÖNEMLİ GÜVENLİK UYARISI !!! ---
# Bu URL, kullanıcı adı ve şifre gibi hassas bilgileri (credentials) içermektedir.
# Bu betiği veya bu URL'yi ASLA başkalarıyla paylaşmayın veya
# herkese açık bir depoya (GitHub gibi) yüklemeyin.
# Bu bilgileri kodun içine "hardcode" yapmak (doğrudan yazmak)
# son derece güvensiz bir yöntemdir.
# -------------------------------------------------
PLAYLIST_URL = "https://goldvod.org/get.php?username=hpgdisco&password=123456&type=m3u_plus&output=m3u"

# İndirilen içeriğin kaydedileceği dosya adı
OUTPUT_FILENAME = "indirilen_playlist.m3u"

def fetch_and_save_m3u():
    """
    Belirtilen URL'den M3U playlist'ini çeker ve bir dosyaya kaydeder.
    """
    print(f"Playlist çekiliyor: {PLAYLIST_URL}")
    
    try:
        # Belirtilen URL'ye GET isteği gönder
        # timeout=10: Sunucudan 10 saniye içinde yanıt gelmezse hata ver.
        response = requests.get(PLAYLIST_URL, timeout=10)
        
        # HTTP hata kodlarını (4xx, 5xx) kontrol et
        # Eğer bir hata varsa (örn: 401 Unauthorized, 404 Not Found)
        # bir istisna (exception) fırlatacaktır.
        response.raise_for_status()
        
        # Yanıtın metin içeriğini al (M3U içeriği)
        # response.text, içeriğin kodlamasını (encoding) tahmin etmeye çalışır
        playlist_content = response.text
        
        # İçeriği yerel bir dosyaya yaz
        # encoding='utf-8' Türkçe karakterler ve özel semboller için önemlidir.
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            f.write(playlist_content)
            
        print(f"\nBaşarılı!")
        print(f"Playlist '{OUTPUT_FILENAME}' dosyasına başarıyla kaydedildi.")

    except requests.exceptions.HTTPError as errh:
        print(f"\n[HATA] HTTP Hatası:", file=sys.stderr)
        print(f"Detay: {errh}", file=sys.stderr)
        print("Lütfen URL'yi, kullanıcı adınızı veya şifrenizi kontrol edin.", file=sys.stderr)
        print("Sunucu erişime izin vermemiş olabilir (örn: 401 Unauthorized).", file=sys.stderr)
        
    except requests.exceptions.ConnectionError as errc:
        print(f"\n[HATA] Bağlantı Hatası:", file=sys.stderr)
        print(f"Detay: {errc}", file=sys.stderr)
        print("Sunucuya bağlanılamadı. İnternet bağlantınızı veya URL'yi kontrol edin.", file=sys.stderr)
        
    except requests.exceptions.Timeout as errt:
        print(f"\n[HATA] Zaman Aşımı:", file=sys.stderr)
        print(f"Detay: {errt}", file=sys.stderr)
        print("Sunucu 10 saniye içinde yanıt vermedi.", file=sys.stderr)
        
    except requests.exceptions.RequestException as err:
        # Diğer 'requests' kütüphanesi hataları için
        print(f"\n[HATA] İstek Hatası:", file=sys.stderr)
        print(f"Detay: {err}", file=sys.stderr)
        
    except IOError as e:
        # Dosya yazma hataları için
        print(f"\n[HATA] Dosya Yazma Hatası:", file=sys.stderr)
        print(f"Detay: {e}", file=sys.stderr)
        print(f"'{OUTPUT_FILENAME}' dosyası yazılamadı. İzinlerinizi kontrol edin.", file=sys.stderr)
    except Exception as e:
        # Beklenmedik diğer tüm hatalar
        print(f"\n[BEKLENMEDİK HATA]: {e}", file=sys.stderr)


# Betiği ana program olarak çalıştır
if __name__ == "__main__":
    fetch_and_save_m3u()