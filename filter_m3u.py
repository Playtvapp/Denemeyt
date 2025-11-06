# -*- coding: utf-8 -*-
import os

# --- AYARLAR ---
# Kaynak M3U dosyasının adı (Bu dosyanın reponuzda, bu script ile aynı dizinde olması gerekir)
SOURCE_FILE = 'rus.m3u'
# Çıktı olarak oluşturulacak yeni M3U dosyasının adı
OUTPUT_FILE = 'turkey.m3u'
# Filtrelenmesini istediğiniz kategori adı (Büyük/küçük harfe duyarlıdır)
CATEGORY_NAME = 'Türkiye'
# --- AYARLAR SONU ---

def filter_m3u_channels():
    """
    Ana M3U dosyasını okur, belirtilen kategoriye göre filtreler
    ve yeni bir M3U dosyası oluşturur.
    """
    print(f"'{SOURCE_FILE}' dosyası okunuyor...")
    
    # Kaynak dosyanın var olup olmadığını kontrol et
    if not os.path.exists(SOURCE_FILE):
        print(f"HATA: '{SOURCE_FILE}' dosyası bulunamadı.")
        print("Lütfen bu dosyayı (rus.m3u) GitHub reponuza eklediğinizden emin olun.")
        return

    try:
        # Dosyayı oku ve satırları temizle
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
    except Exception as e:
        print(f"Dosya okunurken bir hata oluştu: {e}")
        return

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

    print(f"Toplam {len(all_channels)} kanal bulundu. '{CATEGORY_NAME}' kategorisi için filtreleme yapılıyor...")

    filtered_channels = []
    # Kanalları filtrele
    for block in all_channels:
        block_string = '\n'.join(block)
        
        # Hem group-title="Türkiye" hem de #EXTGRP:Türkiye formatlarını kontrol et
        if f'group-title="{CATEGORY_NAME}"' in block_string or f'#EXTGRP:{CATEGORY_NAME}' in block_string:
            filtered_channels.append(block)

    if not filtered_channels:
        print(f"'{CATEGORY_NAME}' kategorisinde hiç kanal bulunamadı. Çıktı dosyası oluşturulmadı.")
        # İsteğe bağlı olarak boş bir turkey.m3u oluşturabilirsiniz
        # with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        #     f.write(header + '\n' if header else '#EXTM3U\n')
        return

    print(f"'{CATEGORY_NAME}' kategorisinde {len(filtered_channels)} kanal bulundu. '{OUTPUT_FILE}' dosyası oluşturuluyor...")

    # Yeni M3U dosyasını yaz
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            if header:
                f.write(header + '\n')
            else:
                f.write('#EXTM3U\n') # Başlık yoksa varsayılanı ekle
            
            # Filtrelenen kanalları dosyaya yaz
            for block in filtered_channels:
                f.write('\n'.join(block) + '\n')
        
        print(f"'{OUTPUT_FILE}' dosyası başarıyla oluşturuldu.")

    except Exception as e:
        print(f"'{OUTPUT_FILE}' dosyası yazılırken bir hata oluştu: {e}")

if __name__ == "__main__":
    filter_m3u_channels()