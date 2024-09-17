import tkinter as tk
from tkinter import ttk, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import threading
import sqlite3

# Cài đặt chromedriver
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

class FacebookAutoPosterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Auto Poster")
        self.root.geometry("600x600")

        # Khởi tạo cơ sở dữ liệu SQLite và bảng accounts
        self.conn = sqlite3.connect('facebook_accounts.db')
        self.create_table()

        self.create_widgets()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                password TEXT
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        # Frame for login information
        login_frame = ttk.LabelFrame(self.root, text="Thông tin đăng nhập Facebook")
        login_frame.pack(padx=20, pady=20, fill="both")

        # Email and Password fields
        email_label = ttk.Label(login_frame, text="Email:")
        email_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = ttk.Entry(login_frame, width=40)
        self.email_entry.grid(row=0, column=1, padx=10, pady=5)

        password_label = ttk.Label(login_frame, text="Mật khẩu:")
        password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = ttk.Entry(login_frame, show="*", width=40)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Button to add account
        add_account_button = ttk.Button(login_frame, text="Thêm tài khoản", command=self.add_account)
        add_account_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Start button
        start_button = ttk.Button(self.root, text="Bắt đầu đăng bài", command=self.start_posting)
        start_button.pack(pady=10)

        # Button to join group
        join_group_button = ttk.Button(self.root, text="Tham gia nhóm", command=self.show_join_group_window)
        join_group_button.pack(pady=10)

        # Button to delete post
        delete_post_button = ttk.Button(self.root, text="Xóa bài viết", command=self.show_delete_post_window)
        delete_post_button.pack(pady=10)

    def add_account(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ email và mật khẩu")
            return

        self.save_account(email, password)
        messagebox.showinfo("Thành công", "Đã thêm tài khoản thành công!")

    def save_account(self, email, password):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO accounts (email, password)
            VALUES (?, ?)
        ''', (email, password))
        self.conn.commit()

    def start_posting(self):
        # Validate accounts
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM accounts')
        accounts = cursor.fetchall()

        if not accounts:
            messagebox.showerror("Lỗi", "Vui lòng thêm ít nhất một tài khoản trước khi bắt đầu đăng bài")
            return

        # Sử dụng threading để thực hiện đồng thời trên các tài khoản
        threads = []
        for account in accounts:
            thread = threading.Thread(target=self.perform_actions, args=(account[1], account[2]))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Thông báo khi hoàn thành
        messagebox.showinfo("Hoàn thành", "Đã hoàn thành đăng bài vào các nhóm Facebook!")

    def perform_actions(self, email, password):
        try:
            # Khởi tạo trình duyệt
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-notifications")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-popup-blocking")
            driver = webdriver.Chrome(options=options)

            # Hàm đăng nhập
            def login(driver, email, password):
                driver.get("https://www.facebook.com/")
                time.sleep(2)
                email_field = driver.find_element(By.ID, "email")
                password_field = driver.find_element(By.ID, "pass")
                login_button = driver.find_element(By.NAME, "login")

                email_field.send_keys(email)
                password_field.send_keys(password)
                login_button.click()
                time.sleep(2)

            # Thực hiện đăng nhập
            login(driver, email, password)

            # Truy cập vào trang Nhóm trên Facebook
            driver.get('https://www.facebook.com/groups/?category=membership')
            time.sleep(3)

            # Tìm kiếm nhóm và lấy các liên kết
            content_search = "Lập trình"
            box_search = driver.find_element(By.XPATH, "//input[@aria-label='Tìm kiếm nhóm']")
            box_search.click()
            box_search.send_keys(content_search)
            box_search.send_keys(Keys.RETURN) # type: ignore
            time.sleep(2)

            # Lấy các liên kết nhóm
            group_links = set()
            links = driver.find_elements(By.TAG_NAME, 'a')
            for link in links:
                href = link.get_attribute('href')
                if '/groups/' in href and 32 < len(href) < 100:
                    cleaned_href = href.split("?__tn__=")[0]
                    group_links.add(cleaned_href)

            print(f"Logged in and found {len(group_links)} groups with account: {email}")

            # Đăng bài vào từng nhóm
            post_content = """Bác nào cần các khóa này ib mk nhé :
            1. LẬP TRÌNH JAVA (4 tuần, cơ bản, nâng cao, WEB, SPRING MVC, SPRING BOOT)
            LẬP TRÌNH ANDROID - từ cơ bản đến nâng cao
            LẬP TRÌNH PYTHON - 4 tuần, từ zero -hero, ứng dụng thực tế
            LẬP TRÌNH C++, c#
            LẬP TRÌNH PHP
            18 KHÓA LẬP TRÌNH FRONTEN nhe """
            image_path = "D:/KHLT.jpg"

            def post_to_group(driver, group_link, post_content, image_path):
                driver.get(group_link)
                time.sleep(2)

                try:
                    create_post_button = driver.find_element(By.XPATH, "//div[@class='xi81zsa x1lkfr7t xkjl1po x1mzt3pk xh8yej3 x13faqbe']")
                    create_post_button.click()
                    time.sleep(2)

                    photo_video_button = driver.find_element(By.XPATH, "//div[@aria-label='Ảnh/video']")
                    photo_video_button.click()
                    time.sleep(2)

                    for _ in range(2):
                        upload_input = driver.find_element(By.XPATH, "//input[@type='file']")
                        upload_input.send_keys(image_path)
                        time.sleep(2)

                    post_box = driver.find_element(By.XPATH, "//div[contains(@aria-label,'Bạn viết gì đi...') or contains(@aria-label, 'Tạo bài viết công khai...')]")
                    post_box.click()

                    for char in post_content:
                        post_box.send_keys(char)
                        time.sleep(0.000001)
                    time.sleep(2)

                    post_button = driver.find_element(By.XPATH, "//div[@aria-label='Đăng']")
                    post_button.click()
                    time.sleep(4)

                    if driver.find_element(By.XPATH, "//div[contains(text(), 'Để bảo vệ cộng đồng khỏi spam, chúng tôi giới hạn tần suất bạn đăng bài, bình luận hoặc làm các việc khác trong khoảng thời gian nhất định. Bạn có thể thử lại sau.')]").is_displayed():
                        print("Phần tử mong muốn hiển thị, dừng lại!")
                        driver.quit()
                    else:
                        print("Thực hiện thành công group_link: " + group_link)

                except Exception as e:
                    print(f"Failed to post in group {group_link}: {e}")

            # Đăng bài vào từng nhóm đã tìm thấy
            for group_link in group_links:
                post_to_group(driver, group_link, post_content, image_path)

        except Exception as e:
            print(f"Error with account {email}: {e}")

        finally:
            driver.quit()

    def show_join_group_window(self):
        # Tạo giao diện cho chức năng tham gia nhóm
        join_group_window = tk.Toplevel(self.root)
        join_group_window.title("Tham gia nhóm")
        join_group_window.geometry("400x200")

        # Label và Entry cho URL nhóm
        group_url_label = ttk.Label(join_group_window, text="URL nhóm:")
        group_url_label.pack(pady=10)
        self.group_url_entry = ttk.Entry(join_group_window, width=40)
        self.group_url_entry.pack(pady=5)

        # Button thực hiện tham gia nhóm
        join_button = ttk.Button(join_group_window, text="Tham gia nhóm", command=self.join_group)
        join_button.pack(pady=10)

    def join_group(self):
        group_url = self.group_url_entry.get()

        if not group_url:
            messagebox.showerror("Lỗi", "Vui lòng nhập URL nhóm")
            return

        messagebox.showinfo("Thông báo", f"Đã tham gia nhóm {group_url}")

        # Thực hiện hành động tham gia nhóm tại đây (có thể thêm code sau này)

    def show_delete_post_window(self):
        # Tạo giao diện cho chức năng xóa bài viết
        delete_post_window = tk.Toplevel(self.root)
        delete_post_window.title("Xóa bài viết")
        delete_post_window.geometry("400x200")

        # Label và Entry cho nội dung cần xóa
        delete_content_label = ttk.Label(delete_post_window, text="Nội dung cần xóa:")
        delete_content_label.pack(pady=10)
        self.delete_content_entry = ttk.Entry(delete_post_window, width=40)
        self.delete_content_entry.pack(pady=5)

        # Button thực hiện xóa bài viết
        delete_button = ttk.Button(delete_post_window, text="Xóa bài viết", command=self.delete_post)
        delete_button.pack(pady=10)

    def delete_post(self):
        delete_content = self.delete_content_entry.get()

        if not delete_content:
            messagebox.showerror("Lỗi", "Vui lòng nhập nội dung cần xóa")
            return

        messagebox.showinfo("Thông báo", f"Đã xóa bài viết có nội dung: {delete_content}")

        # Thực hiện hành động xóa bài viết tại đây (có thể thêm code sau này)

    def __del__(self):
        self.conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = FacebookAutoPosterApp(root)
    root.mainloop()
