import random
import time
import json
import os
from datetime import datetime
from typing import List, Set, Dict, Optional, Union
import textwrap
import argparse
import sys


class QuoteCategory:
   MOTIVATION = "motivasi"
   SUCCESS = "sukses"
   LIFE = "kehidupan"
   WISDOM = "kebijaksanaan"
   PERSEVERANCE = "ketekunan"


class QuoteManager:
   """Mengelola koleksi quote dengan berbagai fitur"""

   def __init__(self, quotes_file: str = "quotes.json"):
       self.quotes_file = quotes_file
       self.quotes_by_category: Dict[str, List[Dict[str, str]]] = {}
       self.user_favorites: Set[str] = set()
       self.last_displayed: Set[str] = set()
       
       # Load or initialize quotes
       self._load_quotes()
       
   def _load_quotes(self) -> None:
       """Memuat quote dari file JSON atau menggunakan default jika file tidak ada"""
       if os.path.exists(self.quotes_file):
           try:
               with open(self.quotes_file, "r", encoding="utf-8") as f:
                   data = json.load(f)
                   self.quotes_by_category = data.get("quotes", {})
                   self.user_favorites = set(data.get("favorites", []))
           except (json.JSONDecodeError, IOError) as e:
               print(f"Error loading quotes: {e}")
               self._initialize_default_quotes()
       else:
           self._initialize_default_quotes()
           self._save_quotes()
           
   def _initialize_default_quotes(self) -> None:
       """Inisialisasi quote default"""
       default_quotes = [
           {
               "text": "Hidup bukan soal siapa yang paling cepat, tapi siapa yang paling tekun bertahan.",
               "author": "Anonymous",
               "category": QuoteCategory.PERSEVERANCE
           },
           {
               "text": "Jangan menunggu waktu yang tepat. Waktu tidak pernah benar-benar tepat — kamu yang harus membuatnya berarti.",
               "author": "Anonymous",
               "category": QuoteCategory.MOTIVATION
           },
           {
               "text": "Kegagalan adalah guru paling jujur. Ia mengajar tanpa basa-basi, tapi pelajarannya selalu abadi.",
               "author": "Anonymous",
               "category": QuoteCategory.WISDOM
           },
           {
               "text": "Tak apa berjalan lambat, asal tidak berhenti. Karena diam adalah kematian dari mimpi.",
               "author": "Anonymous",
               "category": QuoteCategory.PERSEVERANCE
           },
           {
               "text": "Semua hal besar dimulai dari langkah kecil yang dilakukan secara konsisten.",
               "author": "Anonymous",
               "category": QuoteCategory.SUCCESS
           },
           {
               "text": "Jangan biarkan keraguan membungkam keberanianmu. Suara hati yang tulus selalu layak diikuti.",
               "author": "Anonymous", 
               "category": QuoteCategory.MOTIVATION
           },
           {
               "text": "Ketika kamu lelah, istirahatlah — tapi jangan pernah berhenti.",
               "author": "Anonymous",
               "category": QuoteCategory.PERSEVERANCE
           },
           {
               "text": "Mimpi itu gratis. Tapi untuk mewujudkannya, kamu harus bayar dengan kerja keras dan komitmen.",
               "author": "Anonymous",
               "category": QuoteCategory.SUCCESS
           },
           {
               "text": "Jangan takut terlihat bodoh saat belajar. Takutlah saat kamu pura-pura tahu dan berhenti bertumbuh.",
               "author": "Anonymous",
               "category": QuoteCategory.WISDOM
           },
           {
               "text": "Langkahmu hari ini menentukan jarakmu esok hari. Pilih untuk maju, walau sedikit demi sedikit.",
               "author": "Anonymous",
               "category": QuoteCategory.LIFE
           },
           {
               "text": "Terkadang, yang kamu butuhkan bukan motivasi — tapi keputusan untuk tetap jalan meski tidak ada yang melihat.",
               "author": "Anonymous",
               "category": QuoteCategory.PERSEVERANCE
           },
           {
               "text": "Orang hebat bukan yang tak pernah jatuh, tapi yang memilih untuk bangkit setiap kali dijatuhkan.",
               "author": "Anonymous",
               "category": QuoteCategory.SUCCESS
           },
           {
               "text": "Tertinggal bukan berarti kalah. Mungkin kamu hanya sedang mengambil ancang-ancang untuk lompatan besar.",
               "author": "Anonymous",
               "category": QuoteCategory.MOTIVATION
           },
           {
               "text": "Sinar mentari tidak selalu tampak, tapi kamu tahu dia ada. Begitu juga dengan harapan.",
               "author": "Anonymous",
               "category": QuoteCategory.LIFE
           },
           {
               "text": "Keberanian bukan berarti tidak takut — tapi memilih untuk terus melangkah meski takut itu ada.",
               "author": "Anonymous",
               "category": QuoteCategory.WISDOM
           },
           {
               "text": "Kamu bukan produk dari masa lalumu. Kamu adalah pilihan-pilihan yang kamu buat hari ini.",
               "author": "Anonymous",
               "category": QuoteCategory.LIFE
           },
           {
               "text": "Jika jalan terasa berat, mungkin karena kamu sedang mendaki menuju tempat yang lebih tinggi.",
               "author": "Anonymous",
               "category": QuoteCategory.PERSEVERANCE
           }
       ]
       
       # Organize quotes by category
       self.quotes_by_category = {}
       for quote in default_quotes:
           category = quote["category"]
           if category not in self.quotes_by_category:
               self.quotes_by_category[category] = []
           self.quotes_by_category[category].append(quote)
   
   def _save_quotes(self) -> None:
       """Menyimpan quote ke file JSON"""
       try:
           data = {
               "quotes": self.quotes_by_category,
               "favorites": list(self.user_favorites)
           }
           with open(self.quotes_file, "w", encoding="utf-8") as f:
               json.dump(data, f, ensure_ascii=False, indent=2)
       except IOError as e:
           print(f"Error saving quotes: {e}")
   
   def get_random_quote(self, category: Optional[str] = None) -> Dict[str, str]:
       """Menghasilkan quote acak dengan menghindari pengulangan"""
       if category and category in self.quotes_by_category:
           quotes_pool = self.quotes_by_category[category]
       else:
           # Gabungkan semua quote dari setiap kategori
           quotes_pool = []
           for cat_quotes in self.quotes_by_category.values():
               quotes_pool.extend(cat_quotes)
       
       # Filter quote yang belum ditampilkan dalam siklus saat ini
       available_quotes = [q for q in quotes_pool if q["text"] not in self.last_displayed]
       
       # Reset jika hampir semua quote sudah digunakan
       if len(available_quotes) <= max(3, len(quotes_pool) // 5):
           self.last_displayed.clear()
           available_quotes = quotes_pool
       
       if not available_quotes:  # Penanganan untuk kasus yang tidak mungkin terjadi
           return {"text": "Maaf, tidak ada quote tersedia.", "author": "System", "category": ""}
           
       quote = random.choice(available_quotes)
       self.last_displayed.add(quote["text"])
       
       # Batasi ukuran history
       max_history = min(len(quotes_pool) // 2, 10)
       if len(self.last_displayed) > max_history:
           self.last_displayed.pop()
           
       return quote
       
   def add_quote(self, text: str, author: str = "Anonymous", category: str = QuoteCategory.WISDOM) -> bool:
       """Menambahkan quote baru ke koleksi"""
       if not text.strip():
           return False
           
       if category not in self.quotes_by_category:
           self.quotes_by_category[category] = []
           
       new_quote = {"text": text, "author": author or "Anonymous", "category": category}
       self.quotes_by_category[category].append(new_quote)
       self._save_quotes()
       return True
   
   def toggle_favorite(self, quote_text: str) -> bool:
       """Menambah atau menghapus quote dari daftar favorit"""
       if quote_text in self.user_favorites:
           self.user_favorites.remove(quote_text)
           result = False
       else:
           self.user_favorites.add(quote_text)
           result = True
       self._save_quotes()
       return result
   
   def get_all_categories(self) -> List[str]:
       """Mendapatkan semua kategori yang tersedia"""
       return list(self.quotes_by_category.keys())
   
   def get_quote_count(self, category: Optional[str] = None) -> int:
       """Menghitung jumlah quote yang tersedia"""
       if category:
           return len(self.quotes_by_category.get(category, []))
       else:
           count = 0
           for quotes in self.quotes_by_category.values():
               count += len(quotes)
           return count
   
   def log_quote_view(self, quote: Dict[str, str]) -> None:
       """Mencatat quote yang telah ditampilkan dengan timestamp"""
       timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
       log_entry = {
           "timestamp": timestamp,
           "quote": quote["text"],
           "author": quote["author"],
           "category": quote["category"]
       }
       
       try:
           # Buat file log jika belum ada
           if not os.path.exists("quote_history.json"):
               with open("quote_history.json", "w", encoding="utf-8") as f:
                   json.dump({"history": []}, f)
           
           # Muat data log yang ada
           with open("quote_history.json", "r", encoding="utf-8") as f:
               log_data = json.load(f)
           
           # Tambahkan entry baru
           log_data["history"].append(log_entry)
           
           # Batasi ukuran log (simpan 100 entri terakhir)
           if len(log_data["history"]) > 100:
               log_data["history"] = log_data["history"][-100:]
               
           # Simpan kembali log
           with open("quote_history.json", "w", encoding="utf-8") as f:
               json.dump(log_data, f, ensure_ascii=False, indent=2)
               
       except Exception as e:
           print(f"Error logging quote: {e}")


class QuoteDisplayer:
   """Menangani tampilan dan animasi quote"""
   
   COLORS = {
       "reset": "\033[0m",
       "bold": "\033[1m",
       "blue": "\033[34m",
       "cyan": "\033[36m",
       "green": "\033[32m",
       "yellow": "\033[33m",
       "red": "\033[31m",
       "magenta": "\033[35m"
   }
   
   CATEGORY_COLORS = {
       QuoteCategory.MOTIVATION: "yellow",
       QuoteCategory.SUCCESS: "green",
       QuoteCategory.LIFE: "blue",
       QuoteCategory.WISDOM: "cyan",
       QuoteCategory.PERSEVERANCE: "magenta"
   }
   
   def __init__(self, quote_manager: QuoteManager):
       self.quote_manager = quote_manager
       self.width = 70  # Default width for display
       self.animation_speed = 0.02  # Kecepatan animasi default
       self._update_terminal_size()
       
   def _update_terminal_size(self) -> None:
       """Update ukuran terminal jika memungkinkan"""
       try:
           import shutil
           columns, _ = shutil.get_terminal_size()
           self.width = min(columns - 4, 100)  # Batas maksimum 100 karakter
       except:
           # Tetap gunakan default jika ada masalah
           pass
           
   def _colorize(self, text: str, color: str) -> str:
       """Memberikan warna pada teks"""
       if color in self.COLORS:
           return f"{self.COLORS[color]}{text}{self.COLORS['reset']}"
       return text
   
   def _get_category_color(self, category: str) -> str:
       """Mendapatkan warna untuk kategori tertentu"""
       return self.CATEGORY_COLORS.get(category, "reset")
       
   def _format_quote(self, quote: Dict[str, str], include_author: bool = True) -> str:
       """Format quote untuk tampilan dengan warna dan indentasi"""
       category_color = self._get_category_color(quote["category"])
       
       # Atur lebar teks
       quote_lines = textwrap.wrap(quote["text"], width=self.width - 8)
       formatted_text = "\n      ".join(quote_lines)
       
       # Format dasar dengan emoji dan warna
       formatted = f"{self._colorize('╭─ 💬', category_color)}\n"
       formatted += f"│  {self._colorize(formatted_text, category_color)}\n"
       
       if include_author and quote["author"]:
           formatted += f"│  {self._colorize('~ ' + quote['author'], 'bold')}\n"
           
       formatted += f"{self._colorize('╰', category_color)}─{'─' * (self.width - 2)}"
       
       return formatted
       
   def display_header(self, title: str = "QUOTE HARI INI") -> None:
       """Menampilkan header dengan tanggal"""
       self._update_terminal_size()
       date_str = datetime.now().strftime("%d %B %Y")
       print("\n" + "═" * self.width)
       print(f"  {self._colorize('📌 ' + title, 'bold')} │ {date_str}")
       print("═" * self.width)
       
   def display_footer(self, quote_count: int) -> None:
       """Menampilkan footer dengan informasi"""
       print("\n" + "─" * self.width)
       print(f"  {self._colorize('ℹ️', 'blue')} Total koleksi: {quote_count} quotes dalam {len(self.quote_manager.get_all_categories())} kategori")
       print("═" * self.width + "\n")
       
   def animate_text(self, text: str) -> None:
       """Menampilkan text dengan animasi typing"""
       for char in text:
           print(char, end='', flush=True)
           time.sleep(self.animation_speed)
       print()
       
   def display_quote_with_animation(self, category: Optional[str] = None) -> None:
       """Menampilkan quote dengan animasi"""
       quote = self.quote_manager.get_random_quote(category)
       self.quote_manager.log_quote_view(quote)
       
       self.display_header()
       
       formatted_quote = self._format_quote(quote)
       self.animate_text(formatted_quote)
       
       is_favorite = quote["text"] in self.quote_manager.user_favorites
       favorite_mark = "❤️ " if is_favorite else ""
       
       category_color = self._get_category_color(quote["category"])
       print(f"\n  {self._colorize('Kategori:', 'bold')} {self._colorize(quote['category'], category_color)} {favorite_mark}")
       
       self.display_footer(self.quote_manager.get_quote_count())
       
   def display_all_categories(self) -> None:
       """Menampilkan semua kategori yang tersedia"""
       categories = self.quote_manager.get_all_categories()
       
       self.display_header("KATEGORI QUOTE")
       
       for i, category in enumerate(sorted(categories), 1):
           count = self.quote_manager.get_quote_count(category)
           color = self._get_category_color(category)
           print(f"  {i}. {self._colorize(category, color)} ({count} quotes)")
           
       self.display_footer(self.quote_manager.get_quote_count())


def parse_arguments():
   """Parse command line arguments"""
   parser = argparse.ArgumentParser(description="Quote Generator - Tampilkan quote inspiratif")
   parser.add_argument("-c", "--category", help="Pilih kategori quote tertentu")
   parser.add_argument("-l", "--list", action="store_true", help="Tampilkan daftar kategori yang tersedia")
   parser.add_argument("-a", "--add", action="store_true", help="Tambahkan quote baru")
   parser.add_argument("-s", "--speed", type=float, default=0.02, help="Kecepatan animasi (dalam detik)")
   parser.add_argument("--version", action="version", version="Quote Generator v1.0")
   return parser.parse_args()


def interactive_add_quote(quote_manager: QuoteManager):
   """Tambahkan quote baru secara interaktif"""
   print("\n=== Tambah Quote Baru ===")
   
   text = input("Masukkan quote: ").strip()
   if not text:
       print("Quote tidak boleh kosong!")
       return
       
   author = input("Masukkan nama penulis (kosongkan untuk 'Anonymous'): ").strip()
   
   # Tampilkan kategori yang tersedia
   print("\nKategori yang tersedia:")
   categories = quote_manager.get_all_categories()
   for i, category in enumerate(categories, 1):
       print(f"{i}. {category}")
   print(f"{len(categories) + 1}. Lainnya (masukkan sendiri)")
   
   try:
       choice = int(input(f"\nPilih kategori (1-{len(categories) + 1}): "))
       if 1 <= choice <= len(categories):
           category = categories[choice - 1]
       else:
           category = input("Masukkan kategori baru: ").strip().lower()
   except ValueError:
       category = QuoteCategory.WISDOM  # Default jika input tidak valid
   
   success = quote_manager.add_quote(text, author, category)
   if success:
       print("\n✅ Quote berhasil ditambahkan!")
   else:
       print("\n❌ Gagal menambahkan quote")


def main():
   """Program utama"""
   args = parse_arguments()
   
   try:
       # Inisialisasi quote manager
       quote_manager = QuoteManager()
       quote_displayer = QuoteDisplayer(quote_manager)
       
       # Sesuaikan kecepatan animasi
       quote_displayer.animation_speed = args.speed
       
       if args.list:
           quote_displayer.display_all_categories()
       elif args.add:
           interactive_add_quote(quote_manager)
       else:
           quote_displayer.display_quote_with_animation(args.category)
   
   except KeyboardInterrupt:
       print("\n\nProgram dihentikan. Sampai jumpa!")
   except Exception as e:
       print(f"\n\nTerjadi kesalahan: {e}")
       return 1
   
   return 0


if __name__ == "__main__":
   sys.exit(main())
