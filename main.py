import random

quotes = [
    "Hidup adalah perjuangan, jangan menyerah.",
    "Sukses butuh proses, bukan instan.",
    "Kerja keras mengalahkan bakat saat bakat tidak bekerja keras.",
    "Jangan takut gagal, takutlah untuk tidak mencoba.",
    "Setiap hari adalah kesempatan baru untuk menjadi lebih baik."
]

def get_random_quote():
    return random.choice(quotes)

if __name__ == "__main__":
    print("💬 Quote Hari Ini:")
    print(get_random_quote())
