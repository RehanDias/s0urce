import requests
import re

def unduh_dan_bersihkan(url, nama_sumber):
    """Mengunduh dan menyaring kata dari satu URL sumber."""
    print(f"[{nama_sumber}] Sedang mengunduh...")
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"[{nama_sumber}] Gagal mengunduh. Kode error: {response.status_code}")
        return set()
    
    daftar_mentah = response.text.splitlines()
    kata_bersih = set()
    
    for kata in daftar_mentah:
        kata = kata.strip().lower()

        # PRE-PROCESS: Buang suffix kode kamus seperti /DkMkO0k0nl, /B0, /i0, dst.
        # Contoh: "abadi/DkMkO0k0nl" → "abadi"
        if '/' in kata:
            kata = kata.split('/')[0].strip()

        # Filter 1: Kosong
        if not kata:
            continue
        # Filter 2: Baris yang hanya berisi angka (misal baris pertama "31128")
        if kata.isdigit():
            continue
        # Filter 3: Frasa (ada spasi/tab) → "(air) susu dibalas...", "abad al-abīd"
        if ' ' in kata or '\t' in kata:
            continue
        # Filter 4: Kata majemuk dengan tanda hubung → "kura-kura", "abu-abu", "a-"
        if '-' in kata:
            continue
        # Filter 5: Ada tanda kurung → "(me)rentan", "(bagai)"
        if '(' in kata or ')' in kata:
            continue
        # Filter 6: Ada titik → "a.n.", "a.p.", ".gitignore"
        if '.' in kata:
            continue
        # Filter 7: Hanya huruf murni (menolak angka, simbol, dll.)
        if not kata.isalpha():
            continue
        # Filter 8: Tidak boleh ada karakter non-ASCII (menolak: à, é, ñ, ī, dll.)
        if not kata.isascii():
            continue
        # Filter 9: Minimal 2 karakter
        if len(kata) < 2:
            continue
        # Filter 10: Double-check hanya a-z
        if not re.fullmatch(r'[a-z]+', kata):
            continue

        kata_bersih.add(kata)
    
    print(f"[{nama_sumber}] Berhasil disaring: {len(kata_bersih)} kata murni.")
    return kata_bersih


def gabungkan_semua_kata():
    sumber = [
        (
            "https://raw.githubusercontent.com/damzaky/kumpulan-kata-bahasa-indonesia-KBBI/master/list_1.0.0.txt",
            "KBBI"
        ),
        (
            "https://raw.githubusercontent.com/sastrawi/sastrawi/master/data/kata-dasar.txt",
            "Sastrawi"
        ),
        (
            "https://raw.githubusercontent.com/RehanDias/s0urce/refs/heads/main/kamus.txt",
            "RehanDias"
        ),
        (
            "https://raw.githubusercontent.com/titoBouzout/Dictionaries/refs/heads/master/Indonesia.dic",
            "titoBouzout"
        ),
        (
            "https://raw.githubusercontent.com/Wikidepia/indonesian_datasets/refs/heads/master/dictionary/wordlist/data/wordlist.txt",
            "Wikidepia"
        ),
    ]
    
    gabungan = set()
    
    for url, nama in sumber:
        hasil = unduh_dan_bersihkan(url, nama)
        sebelum = len(gabungan)
        gabungan |= hasil  # union set: otomatis hapus duplikat
        tambahan = len(gabungan) - sebelum
        print(f"  → {tambahan} kata baru ditambahkan dari {nama} (duplikat dibuang otomatis)\n")
    
    # Urutkan sesuai abjad
    kata_final = sorted(gabungan)
    
    print(f"{'='*50}")
    print(f"Total kata unik gabungan: {len(kata_final)}")
    print(f"{'='*50}\n")
    
    # Simpan ke file
    nama_file = "daftar_kata_gabungan.txt"
    with open(nama_file, "w", encoding="utf-8") as f:
        for kata in kata_final:
            f.write(kata + "\n")
    
    print(f"File disimpan: {nama_file}")
    return kata_final


# ── Jalankan ──────────────────────────────────────────────
kumpulan_kata = gabungkan_semua_kata()

# Contoh preview hasil
if kumpulan_kata:
    print("\nContoh hasil (urutan ke-20000 s/d 20004):")
    for i in range(20000, min(20005, len(kumpulan_kata))):
        print(f"  [{i}] {kumpulan_kata[i]}")
