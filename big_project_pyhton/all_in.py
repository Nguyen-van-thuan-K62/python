import tkinter as tk
import sqlite3
from tkinter import ttk
from tkinter import messagebox
from add_group import Add_group
from post_group import Post_group

class FacebookAuto:

    # Connect to the database
    conn = sqlite3.connect('via.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS acc (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT
    )
    ''')

    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Automation")
        self.root.geometry("700x700")

        information_frame = ttk.LabelFrame(self.root, text="Nhập thông tin")
        information_frame.pack(padx=20, pady=20, fill="both")

        email_label = ttk.Label(information_frame, text="Email/ID:")
        email_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = ttk.Entry(information_frame, width=40)
        self.email_entry.grid(row=0, column=1, padx=10, pady=5)

        password_label = ttk.Label(information_frame, text="Mật khẩu:")
        password_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.password_entry = ttk.Entry(information_frame, show="*", width=40)
        self.password_entry.grid(row=0, column=3, padx=10, pady=5)

        function_frame = ttk.LabelFrame(self.root, text="Chỉnh Sửa Thông Tin Tài Khoản")
        function_frame.pack(padx=20, pady=20, fill="both")

        add_button = ttk.Button(function_frame, text="Thêm", command=self.add_entry)
        add_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        update_button = ttk.Button(function_frame, text="Sửa", command=self.update_entry)
        update_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        delete_button = ttk.Button(function_frame, text="Xóa", command=self.delete_entry)
        delete_button.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        key_label = ttk.Label(function_frame, text="Từ Khóa Tìm Kiếm:")
        key_label.grid(row=0, column=3, padx=10, pady=5, sticky="w")
        self.key_entry = ttk.Entry(function_frame, width=40)
        self.key_entry.grid(row=0, column=4, padx=10, pady=5)

        search_button = ttk.Button(function_frame, text="Tìm Kiếm", command=self.search_entry)
        search_button.grid(row=0, column=5, padx=10, pady=5, sticky="w")

        list_frame = ttk.LabelFrame(self.root, text="Danh sách tài khoản")
        list_frame.pack(padx=20, pady=20, fill="both")

        columns = ("id", "email", "password")
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        self.tree.heading("id", text="ID")
        self.tree.heading("email", text="Email")
        self.tree.heading("password", text="Password")

        function_frame = ttk.LabelFrame(self.root, text="Các chức năng khác")
        function_frame.pack(padx=20, pady=20, fill="both")

        add_group_button = ttk.Button(function_frame, text="Tham gia nhóm", command=self.add_group)
        add_group_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        post_group_button = ttk.Button(function_frame,text="Đăng bài trong nhóm",command=self.post_group)
        post_group_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.tree.pack(expand=True, fill='both')

        self.load_entries()  # Load data initially

        self.email_entry.bind('<Return>', lambda event: self.add_entry())
        self.password_entry.bind('<Return>', lambda event: self.add_entry())

        self.key_entry.bind('<Return>', lambda event: self.search_entry())
    # load va hien thi danh sach tai khoan
    def load_entries(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.cursor.execute("SELECT * FROM acc")
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

    # theem tai khoan
    def add_entry(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập email và mật khẩu")
        else:
            self.cursor.execute('INSERT INTO acc (email, password) VALUES (?, ?)', (email, password))
            self.conn.commit()
            messagebox.showinfo("Success", "Bạn chắc chắn muốn thêm.")
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.load_entries()  # Reload the table

    # sua thong tin tai khoan
    def update_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Vui lòng chọn tài khoản để sửa")
            return

        item = self.tree.item(selected_item)
        user_id = item['values'][0]

        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Vui lòng nhập email và mật khẩu")
        else:
            self.cursor.execute('UPDATE acc SET email = ?, password = ? WHERE id = ?', (email, password, user_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Bạn chắc chắn muốn sửa.")
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.load_entries()  # Reload the table

    # xoa tai khoan
    def delete_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Vui lòng chọn tài khoản để xóa")
            return

        item = self.tree.item(selected_item)
        user_id = item['values'][0]

        self.cursor.execute('DELETE FROM acc WHERE id = ?', (user_id,))
        self.conn.commit()
        messagebox.showinfo("Success", "Bạn chắc chắn muốn xóa.")
        self.load_entries()  # Reload the table

    # tim kiem tai khoan
    def search_entry(self):
        keyword = self.key_entry.get()

        for row in self.tree.get_children():
            self.tree.delete(row)

        self.cursor.execute("SELECT * FROM acc WHERE email LIKE ?", ('%' + keyword + '%',))
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)
    # Chuyen sang add_group       
    def add_group(self):
        self.root.destroy()
        root = tk.Tk()
        Add_group(root)
        root.mainloop()
    
    #Chuyen sang post_group
    def post_group(self):
        self.root.destroy()
        root = tk.Tk()
        Post_group(root)
        root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = FacebookAuto(root)
    root.mainloop()
