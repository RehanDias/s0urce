import random

quotes = [
    "Hidup bukan soal siapa yang paling cepat, tapi siapa yang paling tekun bertahan.",
    "Jangan menunggu waktu yang tepat. Waktu tidak pernah benar-benar tepat — kamu yang harus membuatnya berarti.",
    "Kegagalan adalah guru paling jujur. Ia mengajar tanpa basa-basi, tapi pelajarannya selalu abadi.",
    "Tak apa berjalan lambat, asal tidak berhenti. Karena diam adalah kematian dari mimpi.",
    "Semua hal besar dimulai dari langkah kecil yang dilakukan secara konsisten.",
    "Jangan biarkan keraguan membungkam keberanianmu. Suara hati yang tulus selalu layak diikuti.",
    "Ketika kamu lelah, istirahatlah — tapi jangan pernah berhenti.",
    "Mimpi itu gratis. Tapi untuk mewujudkannya, kamu harus bayar dengan kerja keras dan komitmen.",
    "Jangan takut terlihat bodoh saat belajar. Takutlah saat kamu pura-pura tahu dan berhenti bertumbuh.",
    "Langkahmu hari ini menentukan jarakmu esok hari. Pilih untuk maju, walau sedikit demi sedikit.",
    "Terkadang, yang kamu butuhkan bukan motivasi — tapi keputusan untuk tetap jalan meski tidak ada yang melihat.",
    "Orang hebat bukan yang tak pernah jatuh, tapi yang memilih untuk bangkit setiap kali dijatuhkan.",
    "Tertinggal bukan berarti kalah. Mungkin kamu hanya sedang mengambil ancang-ancang untuk lompatan besar.",
    "Sinar mentari tidak selalu tampak, tapi kamu tahu dia ada. Begitu juga dengan harapan.",
    "Keberanian bukan berarti tidak takut — tapi memilih untuk terus melangkah meski takut itu ada.",
    "Kamu bukan produk dari masa lalumu. Kamu adalah pilihan-pilihan yang kamu buat hari ini.",
    "Jika jalan terasa berat, mungkin karena kamu sedang mendaki menuju tempat yang lebih tinggi."
]

def get_random_quote():
    return random.choice(quotes)

if __name__ == "__main__":
    print("💬 Quote Hari Ini:")
    print(f"\"{get_random_quote()}\"")
