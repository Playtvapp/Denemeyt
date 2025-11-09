# -*- coding: utf-8 -*-

def create_m3u_playlist(filename="my_playlist.m3u"):
    """
    Basit bir .m3u çalma listesi dosyası oluşturur.
    """
    
    # Çalma listesine eklenecek örnek içerikler
    # Her bir öğe bir sözlüktür:
    # 'title': Parça başlığı
    # 'duration': Süre (saniye cinsinden, -1 genellikle canlı yayınlar için kullanılır)
    # 'url': Medya kaynağının URL'si
    tracks = [
        {
            "title": "Örnek Kanal 1 (Canlı)",
            "duration": -1,
            "url": "http://example.com/stream/channel1"
        },
        {
            "title": "Örnek Film",
            "duration": 7200,  # 2 saat (saniye cinsinden)
            "url": "http://example.com/movie/sample_movie.mp4"
        },
        {
            "title": "Örnek Müzik",
            "duration": 185,   # 3 dakika 5 saniye
            "url": "http://example.com/music/track1.mp3"
        }
    ]

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # M3U dosyasının standart başlığı
            f.write("#EXTM3U\n")
            
            for track in tracks:
                # Her parça için #EXTINF etiketi
                # format: #EXTINF:<süre>,<başlık>
                f.write(f"#EXTINF:{track['duration']},{track['title']}\n")
                
                # Medya URL'si
                f.write(f"{track['url']}\n")
                
            print(f"Başarılı: '{filename}' dosyası oluşturuldu.")

    except IOError as e:
        print(f"Hata: Dosya yazılırken bir sorun oluştu. {e}")

# Betiği çalıştır
if __name__ == "__main__":
    create_m3u_playlist()