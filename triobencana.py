"""
Social Media Video Downloader TRIO BENCANA
===========================

Project Otomatisasi Download Video Social Media
Dibuat oleh: Trio Bencana

Deskripsi:
Program ini mengotomatisasi proses download video dari berbagai platform social media
menggunakan konsep OOP inheritance.

Fitur:
- Download video TikTok tanpa watermark
- Download video/reels Facebook dengan kualitas HD
- Download video/reels/foto Instagram dengan kualitas terbaik
- Penyimpanan otomatis dengan format nama terstruktur
- Interface command line yang user-friendly
"""

import os  
import requests  
from datetime import datetime  
from typing import Optional  

# Kelas dasar untuk downloader
class BaseDownloader:
    def __init__(self):
        self.download_path = "downloads"  # Path untuk menyimpan video yang diunduh
        self.api_key = "e2b637ab25msh618e9bb20ad3300p1d90aejsn35940e09de89"  # Kunci API untuk akses layanan

    def create_download_folder(self) -> None:
        # Membuat folder untuk menyimpan video jika belum ada
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

    def download_video(self, url: str, filename: str) -> bool:
        # Mengunduh video dari URL yang diberikan
        try:
            response = requests.get(url, stream=True)  # Mengambil konten video
            if response.status_code == 200:
                print("\nMendownload video...")
                with open(filename, 'wb') as f:
                    for data in response.iter_content(chunk_size=8192):
                        if data:
                            f.write(data)  # Menyimpan data video ke file
                print("Download selesai!")
                file_name = os.path.basename(filename)  # Mengambil nama file
                print(f"Video disimpan dengan nama: {file_name}")
                return True
            return False
        except Exception as e:
            print(f"Error saat download video: {str(e)}")
            return False

# Kelas turunan untuk TikTok
class TikTokDownloader(BaseDownloader):
    def __init__(self):
        super().__init__()  # Memanggil konstruktor kelas dasar
        self.api_url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"  # URL API untuk TikTok
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
        }

    def get_video_info(self, url: str) -> Optional[dict]:
        # Mengambil informasi video dari URL TikTok
        try:
            response = requests.get(
                self.api_url,
                headers=self.headers,
                params={"url": url}
            )
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error saat mengambil info TikTok: {str(e)}")
            return None

    def process_download(self, url: str) -> bool:
        # Memproses pengunduhan video TikTok
        self.create_download_folder()
        print("Mengambil informasi video...")
        
        video_info = self.get_video_info(url)
        if not video_info or "data" not in video_info:
            print("Gagal mendapatkan informasi video")
            return False
        
        download_url = video_info["data"].get("play")
        if not download_url:
            print("URL video tidak ditemukan")
            return False
        
        print("URL video ditemukan")
        filename = f"{self.download_path}/tiktok_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        return self.download_video(download_url, filename)

# Kelas turunan untuk Facebook
class FacebookDownloader(BaseDownloader):
    def __init__(self):
        super().__init__()
        self.api_url = "https://facebook-reel-and-video-downloader.p.rapidapi.com/app/main.php"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "facebook-reel-and-video-downloader.p.rapidapi.com"
        }

    def get_video_info(self, url: str) -> Optional[dict]:
        # Mengambil informasi video dari URL Facebook
        try:
            response = requests.get(
                self.api_url,
                headers=self.headers,
                params={"url": url}
            )
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error saat mengambil info Facebook: {str(e)}")
            return None

    def process_download(self, url: str) -> bool:
        # Memproses pengunduhan video Facebook
        self.create_download_folder()
        print("Mengambil informasi video...")
        
        video_info = self.get_video_info(url)
        if not video_info or not video_info.get("success"):
            print("Gagal mendapatkan informasi video")
            return False
        
        if "links" in video_info:
            download_url = video_info["links"].get("Download High Quality") or video_info["links"].get("Download Low Quality")
        elif "media" in video_info and video_info["media"]:
            media = video_info["media"][0]
            download_url = media.get("hd_url") or media.get("sd_url")
        else:
            print("URL video tidak ditemukan")
            return False
            
        print("URL video ditemukan")
        filename = f"{self.download_path}/facebook_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        return self.download_video(download_url, filename)

# Kelas turunan untuk Instagram
class InstagramDownloader(BaseDownloader):
    def __init__(self):
        super().__init__()
        self.api_url = "https://instagram-premium-api-2023.p.rapidapi.com/v2/media/by/url"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "instagram-premium-api-2023.p.rapidapi.com"
        }

    def get_video_info(self, url: str) -> Optional[dict]:
        # Mengambil informasi media dari URL Instagram
        try:
            response = requests.get(
                self.api_url,
                headers=self.headers,
                params={"url": url}
            )
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error saat mengambil info Instagram: {str(e)}")
            return None

    def process_download(self, url: str) -> bool:
        # Memproses pengunduhan media Instagram
        self.create_download_folder()
        print("Mengambil informasi media...")
        
        media_info = self.get_video_info(url)
        if not media_info or "items" not in media_info or not media_info["items"]:
            print("Gagal mendapatkan informasi media")
            return False
        
        media_item = media_info["items"][0]
        if "video_versions" in media_item and media_item["video_versions"]:
            video_versions = sorted(
                media_item["video_versions"],
                key=lambda x: x.get("height", 0),
                reverse=True
            )
            download_url = video_versions[0]["url"]
            extension = "mp4"
        elif "image_versions2" in media_item and media_item["image_versions2"]["candidates"]:
            download_url = media_item["image_versions2"]["candidates"][0]["url"]
            extension = "jpg"
        else:
            print("URL media tidak ditemukan")
            return False
            
        print("URL media ditemukan")
        filename = f"{self.download_path}/instagram_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"
        return self.download_video(download_url, filename)

def main():
    # Fungsi utama untuk menjalankan program
    print("=== Triobencana Video Downloader Euyy ===")
    print("\nPilih Sosmednya:")
    print("1. TikTok")
    print("2. Facebook")
    print("3. Instagram")
    
    # Dictionary untuk menyimpan instance downloader
    downloaders = {
        "1": TikTokDownloader(),
        "2": FacebookDownloader(),
        "3": InstagramDownloader()
    }
    
    while True:
        choice = input("\nPilih platform (1/2/3) atau ketik 'rampung' untuk keluar: ")
        
        if choice.lower() == 'rampung':
            print("\nTerima kasih Euyy")
            break
        
        if choice not in downloaders:
            print("Pilihan tidak valid!")
            continue
        
        url = input("Masukkan URL: ")
        if not url:
            print("URL tidak boleh kosong!")
            continue
            
        print("\nMemulai proses download...")
        downloaders[choice].process_download(url)

if __name__ == "__main__":
    main()  