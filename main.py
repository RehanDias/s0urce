import random
import time
from datetime import datetime

class QuoteGenerator:
   def __init__(self, quotes_list=None):
       self.quotes = quotes_list or [
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
       self.last_quotes = set()  # Mencegah quote yang sama muncul berulang
       
   def get_random_quote(self):
       """Menghasilkan quote acak yang tidak berulang dalam siklus tertentu"""
       available_quotes = [q for q in self.quotes if q not in self.last_quotes]
       
       # Reset jika hampir semua quote sudah digunakan
       if len(available_quotes) <= 3:
           self.last_quotes.clear()
           available_quotes = self.quotes
       
       quote = random.choice(available_quotes)
       self.last_quotes.add(quote)
       
       # Pastikan last_quotes tidak terlalu besar
       if len(self.last_quotes) > len(self.quotes) // 2:
           oldest_quote = next(iter(self.last_quotes))
           self.last_quotes.remove(oldest_quote)
           
       return quote
   
   def get_formatted_quote(self):
       """Mengembalikan quote dengan format yang menarik"""
       quote = self.get_random_quote()
       return f"❝ {quote} ❞"
   
   def save_quote_history(self, quote):
       """Menyimpan quote ke file log dengan tanggal dan waktu"""
       timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
       with open("quote_history.txt", "a", encoding="utf-8") as file:
           file.write(f"{timestamp}: {quote}\n\n")


def display_quote_with_animation():
   """Menampilkan quote dengan animasi sederhana"""
   quote_gen = QuoteGenerator()
   quote = quote_gen.get_formatted_quote()
   
   print("\n" + "=" * 60)
   print(f"📌 QUOTE HARI INI | {datetime.now().strftime('%d %B %Y')}")
   print("=" * 60)
   
   # Animasi sederhana
   for char in quote:
       print(char, end='', flush=True)
       time.sleep(0.03)  # Sesuaikan kecepatan animasi
   
   print("\n" + "=" * 60)
   
   # Simpan quote ke history
   quote_gen.save_quote_history(quote)


if __name__ == "__main__":
   try:
       display_quote_with_animation()
   except KeyboardInterrupt:
       print("\n\nProgram dihentikan. Sampai jumpa lagi!")
   except Exception as e:
       print(f"\n\nTerjadi kesalahan: {e}")
