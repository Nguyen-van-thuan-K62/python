"""url = ""
length = len(url)
print(length)"""
import tkinter as tk
from tkinter import messagebox

def show_new_window():
    # Ẩn cửa sổ hiện tại
    #root.withdraw()

    # Tạo cửa sổ giao diện mới
    new_window = tk.Toplevel()
    new_window.title("Giao diện mới")

    #

    # Tạo các widget cho cửa sổ mới
    label = tk.Label(new_window, text="Đây là giao diện mới!")
    label.pack(padx=20, pady=20)

    button_back = tk.Button(new_window, text="Quay lại", command=lambda: close_new_window(new_window))
    button_back.pack(pady=10)

def close_new_window(window):
    # Đóng cửa sổ mới
    window.destroy()

    # Hiển thị lại cửa sổ chính
    root.deiconify()

# Tạo cửa sổ giao diện chính
root = tk.Tk()
root.title("Chuyển đổi giao diện")

# Tạo các widget cho cửa sổ chính
label = tk.Label(root, text="Nhấn nút để chuyển sang giao diện mới")
label.pack(padx=20, pady=20)

button = tk.Button(root, text="Chuyển sang giao diện mới", command=show_new_window)
button.pack(pady=10)

# Chạy chương trình
root.mainloop()

