import tkinter as tk
from tkinter import ttk
import socket
import platform
import threading
import urllib.request

APP_TITLE = "NETCHECK - Network Checker"

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "Tidak diketahui"
    finally:
        s.close()

def check_internet():
    try:
        urllib.request.urlopen("https://www.google.com", timeout=4)
        return True
    except Exception:
        return False

class NetCheckApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("720x540")
        self.root.minsize(600, 450)
        self.root.configure(bg="#eef3f8")

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TButton", font=("Arial", 10), padding=8)

        header = tk.Frame(root, bg="#163a5f", padx=20, pady=18)
        header.pack(fill="x")
        tk.Label(header, text="NETCHECK", font=("Arial", 24, "bold"),
                 fg="white", bg="#163a5f").pack(anchor="w")
        tk.Label(header, text="Network Checker • Proyek TKJ",
                 font=("Arial", 10), fg="#dceaf7", bg="#163a5f").pack(anchor="w")

        info = tk.Frame(root, bg="#eef3f8", padx=18, pady=14)
        info.pack(fill="x")
        self.status = tk.Label(info, text="STATUS: BELUM DIPERIKSA",
                               font=("Arial", 12, "bold"), fg="#6b7280", bg="#eef3f8")
        self.status.pack(anchor="w")
        tk.Label(info, text=f"Perangkat: {platform.node() or 'Tidak diketahui'}",
                 font=("Arial", 10), bg="#eef3f8", fg="#243447").pack(anchor="w", pady=(5, 0))
        self.ip_label = tk.Label(info, text="IP lokal: belum diperiksa",
                                 font=("Arial", 10), bg="#eef3f8", fg="#243447")
        self.ip_label.pack(anchor="w", pady=(3, 0))

        buttons = tk.Frame(root, bg="#eef3f8", padx=18, pady=4)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Cek Internet", command=self.start_internet_check).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Cek IP", command=self.check_ip).pack(side="left", padx=8)
        ttk.Button(buttons, text="Cek Google", command=self.start_google_check).pack(side="left", padx=8)
        ttk.Button(buttons, text="Hapus Hasil", command=self.clear_results).pack(side="left", padx=8)

        result_frame = tk.LabelFrame(root, text="Hasil Pengecekan", font=("Arial", 11, "bold"),
                                     bg="#ffffff", fg="#163a5f", padx=10, pady=10)
        result_frame.pack(fill="both", expand=True, padx=18, pady=14)
        self.output = tk.Text(result_frame, wrap="word", font=("Consolas", 10),
                              bg="#fbfdff", fg="#243447", relief="flat", height=12)
        self.output.pack(fill="both", expand=True)
        self.log("NETCHECK siap digunakan.")
        self.log("Pilih tombol di atas untuk mulai memeriksa jaringan.")

    def log(self, message):
        self.output.insert("end", message + "\n")
        self.output.see("end")

    def set_status(self, message, color):
        self.status.config(text="STATUS: " + message, fg=color)

    def start_internet_check(self):
        self.set_status("SEDANG MEMERIKSA...", "#b7791f")
        self.log("Memeriksa akses internet...")
        threading.Thread(target=self._internet_worker, daemon=True).start()

    def _internet_worker(self):
        ok = check_internet()
        self.root.after(0, lambda: self._show_internet_result(ok))

    def _show_internet_result(self, ok):
        if ok:
            self.set_status("INTERNET TERHUBUNG", "#16803c")
            self.log("BERHASIL: perangkat dapat mengakses internet.")
        else:
            self.set_status("INTERNET TIDAK TERDETEKSI", "#c53030")
            self.log("GAGAL: periksa Wi-Fi, router, kabel, atau jaringan.")

    def check_ip(self):
        ip = get_local_ip()
        self.ip_label.config(text=f"IP lokal: {ip}")
        self.log(f"Alamat IP lokal: {ip}")

    def start_google_check(self):
        self.set_status("MENGUJI KONEKSI GOOGLE...", "#b7791f")
        self.log("Menguji koneksi ke www.google.com...")
        threading.Thread(target=self._google_worker, daemon=True).start()

    def _google_worker(self):
        try:
            with socket.create_connection(("www.google.com", 443), timeout=4):
                result = True
        except OSError:
            result = False
        self.root.after(0, lambda: self._show_google_result(result))

    def _show_google_result(self, ok):
        if ok:
            self.set_status("SERVER GOOGLE DAPAT DIJANGKAU", "#16803c")
            self.log("BERHASIL: koneksi ke www.google.com port 443 berhasil.")
        else:
            self.set_status("SERVER GOOGLE TIDAK TERJANGKAU", "#c53030")
            self.log("GAGAL: periksa internet, DNS, atau firewall.")

    def clear_results(self):
        self.output.delete("1.0", "end")
        self.set_status("BELUM DIPERIKSA", "#6b7280")
        self.log("Hasil dibersihkan. NETCHECK siap digunakan.")

if __name__ == "__main__":
    root = tk.Tk()
    NetCheckApp(root)
    root.mainloop()
