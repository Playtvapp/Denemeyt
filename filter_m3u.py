# -*- coding: utf-8 -*-
import os

# --- AYARLAR ---
# Kaynak M3U dosyasının adı
SOURCE_FILE = 'rus.m3u'

# Filtrelenecek kategorileri ve çıktı dosyalarını burada tanımlayın
# Format: (Kategori Adı, Çıktı Dosyası Adı)
FILTERS_TO_APPLY = [
    ('Türkiye', 'turkey.m3u'),
    ('XXX', 'xxx.m3u')
]
# --- AYARLAR SONU ---

def read_and_parse_source(source_file):
    """
    Kaynak M3U dosyasını okur ve kanalları bloklara ayırır.
    Header'ı ve kanal bloklarının bir listesini döndürür.
    """
    print(f"'{source_file}' dosyası okunuyor...")
    if not os.path.exists(source_file):
        print(f"HATA: '{source_file}' dosyası bulunamadı.")
        print("Lütfen bu dosyayı (rus.m3u) GitHub reponuza eklediğinizden emin olun.")
        return None, None

    try:
        # Dosyayı oku ve satırları temizle
        with open(source_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
    except Exception as e:
        print(f"Dosya okunurken bir hata oluştu: {e}")
        return None, None

    header = ""
    all_channels = []
    current_channel_block = []

    # M3U dosyasını satır satır ayrıştır
    for line in lines:
        if not line:
            continue
            
        if line.startswith('#EXTM3U'):
            header = line
            continue

        if line.startswith('#EXTINF'):
            # Bir önceki kanalı bitir ve listeye ekle
            if current_channel_block:
                all_channels.append(current_channel_block)
            # Yeni kanalı başlat
            current_channel_block = [line]
        elif current_channel_block:
            # #EXTINF ile başlayan bir bloğun parçasıysa (URL, #EXTGRP vb.) ekle
            current_channel_block.append(line)
    
    # Döngü bittikten sonra son kanalı da listeye ekle
    if current_channel_block:
        all_channels.append(current_channel_block)
        
    print(f"Toplam {len(all_channels)} kanal bulundu.")
    return header, all_channels

def filter_and_write(header, all_channels, category_name, output_file):
    """
    Verilen kanal listesini kategoriye göre filtreler ve yeni dosyayı yazar.
    """
    print(f"'{category_name}' kategorisi için filtreleme yapılıyor...")
    
    filtered_channels = []
    # Kanalları filtrele
    for block in all_channels:
        block_string = '\n'.join(block)
        
        # Hem group-title="KATEGORİ" hem de #EXTGRP:KATEGORİ formatlarını kontrol et
        if f'group-title="{category_name}"' in block_string or f'#EXTGRP:{category_name}' in block_string:
            filtered_channels.append(block)

    if not filtered_channels:
        print(f"'{category_name}' kategorisinde hiç kanal bulunamadı. '{output_file}' oluşturulmadı.")
        return

    print(f"'{category_name}' kategorisinde {len(filtered_channels)} kanal bulundu. '{output_file}' dosyası oluşturuluyor...")

    # Yeni M3U dosyasını yaz
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            if header:
                f.write(header + '\n')
            else:
                f.write('#EXTM3U\n') # Başlık yoksa varsayılanı ekle
            
            # Filtrelenen kanalları dosyaya yaz
            for block in filtered_channels:
                f.write('\n'.join(block) + '\n')
        
        print(f"'{output_file}' dosyası başarıyla oluşturuldu.")

    except Exception as e:
        print(f"'{output_file}' dosyası yazılırken bir hata oluştu: {e}")

def main():
    """
    Ana betik. Dosyayı bir kez okur ve tüm filtreleri uygular.
    """
    header, all_channels = read_and_parse_source(SOURCE_FILE)
    
    if all_channels is None:
        print("Ana dosya okunamadı. İşlem durduruldu.")
        return

    # Tanımlanan tüm filtreler için döngü başlat
    for category, output_file in FILTERS_TO_APPLY:
        filter_and_write(header, all_channels, category, output_file)
        print("-" * 20) # Filtreler arası ayırıcı

if __name__ == "__main__":
    main()