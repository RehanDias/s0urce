import random

quotes = [
    "Hidup adalah perjuangan — jangan pernah menyerah, karena setiap luka akan sembuh seiring waktu.",
    "Sukses bukan soal seberapa cepat kamu sampai, tapi seberapa konsisten kamu melangkah.",
    "Kerja keras akan selalu mengalahkan bakat, terutama saat bakat hanya bermalas-malasan.",
    "Jangan takut gagal — kegagalan adalah tanda bahwa kamu sedang mencoba sesuatu yang berani.",
    "Setiap hari adalah kesempatan untuk menulis ulang kisah hidupmu menjadi lebih baik.",
    "Kamu nggak harus hebat untuk memulai, tapi kamu harus memulai untuk menjadi hebat.",
    "Langit tak selalu cerah, tapi badai pasti akan berlalu. Bertahanlah.",
    "Fokus pada proses, bukan hasil. Karena proseslah yang membentuk dirimu sebenarnya.",
    "Orang sukses bukan yang tidak pernah jatuh, tapi yang selalu bangkit setiap kali terjatuh.",
    "Motivasi datang dan pergi, tapi disiplin adalah pondasi keberhasilan sejati.",
    "Kadang hal kecil yang kamu lakukan hari ini, bisa jadi keputusan terbesar dalam hidupmu nanti.",
    "Jangan bandingkan dirimu dengan orang lain — bandingkan dirimu hari ini dengan dirimu kemarin.",
    "Mimpi besar itu penting, tapi tindakan kecil setiap hari yang akan mewujudkannya.",
    "Saat kamu merasa ingin menyerah, ingat kenapa kamu memulainya dulu.",
    "Rasa takut itu wajar. Yang penting, kamu tetap jalan meskipun takut.",
    "Semua orang memulai dari nol. Nggak apa-apa lambat, yang penting nggak berhenti."
]

def get_random_quote():
    return random.choice(quotes)

if __name__ == "__main__":
    print("💬 Quote Hari Ini:")
    print(get_random_quote())
