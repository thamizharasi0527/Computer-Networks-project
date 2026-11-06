import socket
import tkinter as tk
from tkinter import filedialog

HOST = "127.0.0.1"
PORT = 5000

def send_file():
    file_path = filedialog.askopenfilename()
    
    if not file_path:
        return

    with open(file_path,"r") as f:
        data = f.read().strip()

    client = socket.socket()
    client.connect((HOST,PORT))

    client.send(data.encode())

    result = client.recv(4096).decode()

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, result)

    client.close()


# ---------- GUI ----------
root = tk.Tk()
root.title("Hamming Code File Transfer")

root.geometry("500x400")

btn = tk.Button(root, text="Select File & Send", command=send_file)
btn.pack(pady=10)

output_box = tk.Text(root, height=20, width=60)
output_box.pack()

root.mainloop()