import tkinter as tk
from tkinter import ttk, messagebox
import requests
import re
import urllib.parse
import os
import threading
import sys

# Try to import default values from config if available
try:
    import config
    DEFAULT_URL = getattr(config, 'PANO_URL', '')
    DEFAULT_NAME = getattr(config, 'IMAGE_NAME', 'panorama.jpg')
except ImportError:
    DEFAULT_URL = ''
    DEFAULT_NAME = 'panorama.jpg'

class PanoramaDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Street View Panorama Downloader")
        self.root.geometry("600x250")
        self.root.resizable(False, False)

        # Style
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")
        style.configure("TLabel", padding=6, font=("Helvetica", 10))
        style.configure("TEntry", padding=6)

        # Main Frame
        frame = ttk.Frame(root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # URL Input
        ttk.Label(frame, text="Panorama URL:").grid(row=0, column=0, sticky=tk.W)
        self.url_var = tk.StringVar(value=DEFAULT_URL)
        self.url_entry = ttk.Entry(frame, textvariable=self.url_var, width=50)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        # Image Name Input
        ttk.Label(frame, text="Output Filename:").grid(row=1, column=0, sticky=tk.W)
        self.name_var = tk.StringVar(value=DEFAULT_NAME)
        self.name_entry = ttk.Entry(frame, textvariable=self.name_var, width=50)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        # Progress / Status
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(frame, textvariable=self.status_var, foreground="white")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=10)

        # Save Button
        self.save_btn = ttk.Button(frame, text="Save Panorama", command=self.start_download_thread)
        self.save_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # Column config
        frame.columnconfigure(1, weight=1)

    def start_download_thread(self):
        url = self.url_var.get().strip()
        name = self.name_var.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
        if not name:
            messagebox.showerror("Error", "Please enter an output filename")
            return

        self.save_btn.config(state=tk.DISABLED)
        self.status_var.set("Starting download...")
        
        thread = threading.Thread(target=self.download_panorama, args=(url, name))
        thread.daemon = True
        thread.start()

    def download_panorama(self, url, image_name):
        try:
            self.update_status(f"Resolving URL...")
            session = requests.Session()
            resp = session.get(url, allow_redirects=True)
            final_url = resp.url
            
            target_url = final_url
            if "consent.google.com" in final_url:
                self.update_status("Hit consent page, extracting continue url...")
                parsed = urllib.parse.urlparse(final_url)
                qs = urllib.parse.parse_qs(parsed.query)
                if 'continue' in qs:
                    target_url = qs['continue'][0]
            
            # Find encoded URL
            match = re.search(r'!6s(.*?)!', target_url)
            if not match:
                unquoted_target = urllib.parse.unquote(target_url)
                match = re.search(r'!6s(.*?)!', unquoted_target)

            if not match:
                self.download_finished("Error: Could not find image URL in the resolved link.", error=True)
                return

            image_url_segment = match.group(1)
            decoded_url = image_url_segment
            for _ in range(3):
                if decoded_url.startswith("https://") or decoded_url.startswith("http://"):
                    break
                decoded_url = urllib.parse.unquote(decoded_url)
            
            if not (decoded_url.startswith("https://") or decoded_url.startswith("http://")):
                 self.download_finished("Error: Failed to decode image URL.", error=True)
                 return

            base_image_url = decoded_url.split('=')[0]
            
            # Extract resolution
            unquoted_target = urllib.parse.unquote(target_url)
            width_match = re.search(r'!7i(\d+)', unquoted_target)
            height_match = re.search(r'!8i(\d+)', unquoted_target)
            
            width = width_match.group(1) if width_match else "8192"
            height = height_match.group(1) if height_match else "4096"
            
            self.update_status(f"Found dimensions: {width}x{height}. Downloading...")
            
            full_res_url = f"{base_image_url}=w{width}-h{height}-k-no"
            
            # Directory setup
            download_dir = "download"
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
            
            output_path = os.path.join(download_dir, image_name)
            
            r = requests.get(full_res_url, stream=True)
            if r.status_code == 200:
                with open(output_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024*1024):
                        f.write(chunk)
                self.download_finished(f"Saved to {output_path}")
            else:
                self.download_finished(f"Failed status: {r.status_code}", error=True)

        except Exception as e:
            self.download_finished(f"Exception: {str(e)}", error=True)

    def update_status(self, text):
        self.root.after(0, lambda: self.status_var.set(text))

    def download_finished(self, message, error=False):
        def _finish():
            self.status_var.set(message)
            self.save_btn.config(state=tk.NORMAL)
            if error:
                messagebox.showerror("Error", message)
            else:
                messagebox.showinfo("Success", message)
        self.root.after(0, _finish)

if __name__ == "__main__":
    root = tk.Tk()
    app = PanoramaDownloaderApp(root)
    root.mainloop()
