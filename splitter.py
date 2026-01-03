import os
import requests
import re

# --- AYARLAR ---
# Buraya kendi M3U linkini yaz (veya GitHub Secrets'tan çekebilirsin)
M3U_URL = "http://plusjustone.xyz:8080/get.php?username=b4h8feZC&password=cRzefU4&type=m3u"

# Klasör İsimleri
DIR_LIVE = "CanliTV"
DIR_MOVIES = "Filmler"
DIR_SERIES = "Diziler"

# Dosya İsimlerinde Olmaması Gereken Karakterler
def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '', name).strip()

def main():
    print("Playlist indiriliyor...")
    try:
        response = requests.get(M3U_URL, timeout=30)
        response.raise_for_status()
        content = response.text
    except Exception as e:
        print(f"Hata oluştu: {e}")
        exit(1)

    lines = content.split('\n')
    
    # Klasörleri oluştur (Varsa temizle ve yeniden oluştur mantığı eklenebilir ama basit tutuyoruz)
    os.makedirs(DIR_LIVE, exist_ok=True)
    os.makedirs(DIR_MOVIES, exist_ok=True)
    os.makedirs(DIR_SERIES, exist_ok=True)

    # Ana listeler (Toplu Listeler)
    master_live = ["#EXTM3U"]
    master_movies = ["#EXTM3U"]
    master_series = ["#EXTM3U"]

    # Kategori bazlı geçici sözlükler
    cat_live = {}
    cat_movies = {}
    cat_series = {}

    current_group = "Diger"
    is_extinf = False
    buffer_line = ""

    print("Playlist analiz ediliyor ve ayrıştırılıyor...")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("#EXTINF"):
            is_extinf = True
            buffer_line = line
            
            # Grup ismini yakala (group-title="Spor")
            match = re.search(r'group-title="([^"]+)"', line)
            if match:
                current_group = match.group(1)
            else:
                current_group = "Genel"
            
        elif not line.startswith("#") and is_extinf:
            # Bu bir URL satırıdır, işlemi tamamla
            url = line
            full_entry = f"{buffer_line}\n{url}"
            
            # --- KATEGORİ ANALİZİ VE AYRIŞTIRMA MANTIĞI ---
            # Grup ismine bakarak Canlı TV mi, Film mi, Dizi mi karar veriyoruz.
            group_upper = current_group.upper()

            # Filmler için anahtar kelimeler
            if any(x in group_upper for x in ["VOD", "FILM", "MOVIE", "SINEMA", "CINEMA", "2023", "2024", "2025"]):
                # Bu bir Filmdir
                master_movies.append(full_entry)
                if current_group not in cat_movies: cat_movies[current_group] = ["#EXTM3U"]
                cat_movies[current_group].append(full_entry)

            # Diziler için anahtar kelimeler
            elif any(x in group_upper for x in ["DIZI", "SERIES", "SEZON", "SEASON", "EPISODE"]):
                # Bu bir Dizidir
                master_series.append(full_entry)
                if current_group not in cat_series: cat_series[current_group] = ["#EXTM3U"]
                cat_series[current_group].append(full_entry)

            # Geri kalan her şey Canlı TV'dir
            else:
                master_live.append(full_entry)
                if current_group not in cat_live: cat_live[current_group] = ["#EXTM3U"]
                cat_live[current_group].append(full_entry)

            is_extinf = False # Sıfırla

    # --- DOSYALARI YAZDIRMA ---

    # 1. Kategori Dosyalarını Yaz
    def write_categories(category_dict, base_folder):
        for cat_name, entries in category_dict.items():
            safe_name = sanitize_filename(cat_name)
            if not safe_name: safe_name = "Isimsiz_Grup"
            file_path = os.path.join(base_folder, f"{safe_name}.m3u")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(entries))

    write_categories(cat_live, DIR_LIVE)
    write_categories(cat_movies, DIR_MOVIES)
    write_categories(cat_series, DIR_SERIES)

    # 2. Toplu (Master) Dosyaları Yaz
    with open(os.path.join(DIR_LIVE, "TUM_CANLI_TV.m3u"), "w", encoding="utf-8") as f:
        f.write("\n".join(master_live))
    
    with open(os.path.join(DIR_MOVIES, "TUM_FILMLER.m3u"), "w", encoding="utf-8") as f:
        f.write("\n".join(master_movies))

    with open(os.path.join(DIR_SERIES, "TUM_DIZILER.m3u"), "w", encoding="utf-8") as f:
        f.write("\n".join(master_series))

    print("İşlem tamamlandı! Dosyalar ayrıştırıldı.")

if __name__ == "__main__":
    main()
