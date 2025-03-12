import re
import ipaddress
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime

def extract_ips(text):
    """Extracts and sorts unique valid IPv4, IPv6, and CIDR addresses, ensuring fe80::1 is captured."""
    words = re.findall(r'[a-fA-F0-9:.]+(?:/\d+)?', text)  # Improved regex to extract all potential IPs
    ipv4 = set()
    ipv4_cidr = set()
    ipv6 = set()
    ipv6_cidr = set()

    for word in words:
        word = word.rstrip('.')  # Strip trailing period or punctuation
        
        try:
            # Handle both single IPs and CIDR blocks
            if '/' in word:
                ip = ipaddress.ip_network(word, strict=False)
                if isinstance(ip, ipaddress.IPv4Network):
                    ipv4_cidr.add(str(ip))
                elif isinstance(ip, ipaddress.IPv6Network):
                    ipv6_cidr.add(str(ip))
            else:
                ip = ipaddress.ip_address(word)
                if isinstance(ip, ipaddress.IPv4Address):
                    ipv4.add(str(ip))
                elif isinstance(ip, ipaddress.IPv6Address):
                    ipv6.add(str(ip))
        except ValueError:
            continue  # Skip invalid entries

    # Sorting for correct numerical order
    sorted_ipv4 = sorted(ipv4, key=lambda x: tuple(map(int, x.split('.'))))
    sorted_ipv4_cidr = sorted(ipv4_cidr, key=lambda x: tuple(map(int, x.split('/')[0].split('.'))))
    sorted_ipv6 = sorted(ipv6, key=lambda x: ipaddress.IPv6Address(x))
    sorted_ipv6_cidr = sorted(ipv6_cidr, key=lambda x: ipaddress.IPv6Address(x.split('/')[0]))

    return sorted_ipv4 + sorted_ipv4_cidr + sorted_ipv6 + sorted_ipv6_cidr

def parse_data():
    """Handles text extraction and updates the parsed data textbox."""
    text = input_text.get("1.0", tk.END)
    extracted_data = extract_ips(text)
    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", "\n".join(extracted_data))

def copy_to_clipboard():
    """Copies parsed data to clipboard."""
    root.clipboard_clear()
    root.clipboard_append(output_text.get("1.0", tk.END))
    root.update()

def export_to_xlsx():
    """Exports parsed data to an Excel file."""
    extracted_data = output_text.get("1.0", tk.END).strip().split("\n")
    if not extracted_data or extracted_data == ['']:
        return
    df = pd.DataFrame(extracted_data, columns=["Extracted Data"])

    # Suggest filename with timestamp
    filename = f"parsed_ips_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=filename,
                                             filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        df.to_excel(file_path, index=False)

# Initialize GUI
root = ttk.Window(themename="darkly")
root.title("IP and CIDR Extractor")
root.geometry("600x500")
root.resizable(False, False)

# Labels (Bold, Arial 13)
ttk.Label(root, text="Pasted Data", font=("Arial", 13, "bold")).pack(pady=(10, 5))
input_text = tk.Text(root, wrap=WORD, font=("Consolas", 12), height=8)
input_text.pack(fill=X, padx=10)

ttk.Label(root, text="Parsed Data", font=("Arial", 13, "bold")).pack(pady=(10, 5))
output_text = tk.Text(root, wrap=WORD, font=("Consolas", 12), height=8)
output_text.pack(fill=X, padx=10)

# Buttons frame
btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)

parse_btn = ttk.Button(btn_frame, text="Parse this", command=parse_data, bootstyle=PRIMARY)
parse_btn.grid(row=0, column=0, padx=5)

copy_btn = ttk.Button(btn_frame, text="Copy All", command=copy_to_clipboard, bootstyle=SUCCESS)
copy_btn.grid(row=0, column=1, padx=5)

export_btn = ttk.Button(btn_frame, text="Export XLSX", command=export_to_xlsx, bootstyle=INFO)
export_btn.grid(row=0, column=2, padx=5)

# Center align the buttons
btn_frame.columnconfigure((0, 1, 2), weight=1)

# Run the app
root.mainloop()



'''
It's ultra annoying when people 192.168.7.14 give you info in a weird format 192.168.7.14/24 and you try to make sense of their rant but don't care about anything except the ip addresses 192.168.2.0/24 that they are trying to talk about when they duplicate 192.168.7.14 a bunch of garbage nonsense instead 192.168.7.14 of just giving you the facts 192.168.7.14. Did you miss any? 192.168.7.11
'''

