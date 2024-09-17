import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
import time
from selenium.webdriver.common.by import By

class FacebookAutoPosterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Auto Poster")
        self.root.geometry("600x700")

        # Frame for login information
        login_frame = ttk.LabelFrame(self.root, text="Đăng nhập Facebook")
        login_frame.pack(padx=20, pady=20, fill="both")

        # Email field
        email_label = ttk.Label(login_frame, text="Email:")
        email_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = ttk.Entry(login_frame, width=40)
        self.email_entry.grid(row=0, column=1, padx=10, pady=5)

        # Password field
        password_label = ttk.Label(login_frame, text="Mật khẩu:")
        password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = ttk.Entry(login_frame, show="*", width=40)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Keyword for group search
        keyword_label = ttk.Label(login_frame, text="Từ khóa tìm kiếm nhóm:")
        keyword_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.keyword_entry = ttk.Entry(login_frame, width=40)
        self.keyword_entry.grid(row=2, column=1, padx=10, pady=5)

        # Post content
        content_label = ttk.Label(login_frame, text="Nội dung bài đăng:")
        content_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.content_text = scrolledtext.ScrolledText(login_frame, width=40, height=10)
        self.content_text.grid(row=3, column=1, padx=10, pady=5)

        # Image path
        image_label = ttk.Label(login_frame, text="Đường dẫn ảnh:")
        image_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.image_entry = ttk.Entry(login_frame, width=30)
        self.image_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.browse_button = ttk.Button(login_frame, text="Chọn ảnh", command=self.browse_image)
        self.browse_button.grid(row=4, column=2, padx=10, pady=5)

        # Start button
        start_button = ttk.Button(self.root, text="Bắt đầu đăng bài", command=self.start_posting)
        start_button.pack(pady=20)

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.image_entry.delete(0, tk.END)
            self.image_entry.insert(0, file_path)

    def start_posting(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        keyword = self.keyword_entry.get()
        content = self.content_text.get("1.0", tk.END)
        image_path = self.image_entry.get()

        # Validate inputs
        if not email or not password:
            tk.messagebox.showerror("Lỗi", "Vui lòng nhập email và mật khẩu")
            return

        # Call your function to start posting
        self.root.withdraw()  # Hide the main window during posting process
        self.post_to_facebook(email, password, keyword, content, image_path)
        self.root.deiconify()  # Show the main window again after posting

    def post_to_facebook(self, email, password, keyword, content, image_path):
        # Your existing code for posting to Facebook
        import requests
        from bs4 import BeautifulSoup
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        import chromedriver_autoinstaller
        import time
        from selenium.common.exceptions import UnexpectedAlertPresentException
        from selenium.webdriver.common.alert import Alert
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.keys import Keys

        # Cài đặt chromedriver
        chromedriver_autoinstaller.install()

        # Khởi tạo trình duyệt
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")  # Mở trình duyệt ở chế độ toàn màn hình
        options.add_argument("--disable-popup-blocking")

        # Hàm login
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

        # Khởi tạo driver
        driver = webdriver.Chrome(options=options)

        # Thực hiện login
        login(driver, email, password)

        # Truy cập vào trang Nhóm
        driver.get('https://www.facebook.com/groups/?category=membership')
        time.sleep(5)

        # Từ khóa tìm kiếm
        content_search = keyword

        # Click vào tìm kiếm và thực hiện chức năng tìm kiếm nhóm
        box_search = driver.find_element(By.XPATH, "//input[@aria-label='Tìm kiếm nhóm']")
        box_search.click()
        box_search.send_keys(content_search)
        box_search.send_keys(Keys.RETURN)  # Nhấn phím Enter
        time.sleep(2)

        # Click vào nhóm vừa tìm kiếm
        url = "https://www.facebook.com/groups/search/groups/?q=" + content_search + "&__tsid__=0.6966745255588549&__epa__=SERP_TAB&__eps__=GROUPS_HOME_SERP_ALL_TAB"
        driver.get(url)
        time.sleep(2)

        #truy cap vao  nhom cua toi
        group_search_output = driver.find_element(By.XPATH, "//input[@aria-label='Nhóm của tôi']")
        group_search_output .click()
        time.sleep(2)

        #auto keo luot cac nhom
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Cuộn xuống cuối trang
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2.5)  # Chờ trang tải thêm nội dung

            # Lấy chiều cao mới của trang sau khi tải thêm
            new_height = driver.execute_script("return document.body.scrollHeight")
        
            # Nếu không có thêm nội dung được tải, dừng lại
            if new_height == last_height:
                break
        
            last_height = new_height

        # Lấy các liên kết nhóm
        group_links = set()  # Sử dụng set để tránh trùng lặp
        links = driver.find_elements(By.TAG_NAME, 'a')

        # Lọc các liên kết nhóm
        max_url_length = 100
        min_url_length = 32
        for link in links:
            href = link.get_attribute('href')
            if '/groups/' in href and 32 < len(href) < 100:
                cleaned_href = href.split("?__tn__=")[0]  # Xóa phần thừa trong link
                group_links.add(cleaned_href)

        print(len(group_links))
        print("Nhóm :")
        #in ra link
        for link in group_links:
            print(link)       

        # Đăng bài vào từng nhóm
        for group_link in group_links:
            post_to_group(driver, group_link, content, image_path)
            current_window_handle = driver.current_window_handle
            driver.execute_script("window.open('{group_link}');")
            driver.switch_to.window(current_window_handle)
            driver.close()  # Đóng tab trước đó
            driver.switch_to.window(driver.window_handles[-1])

        # Đóng trình duyệt sau khi hoàn thành
        driver.quit()

def post_to_group(driver, group_link, content, image_path):
    driver.get(group_link)
    time.sleep(3)

    try:
        create_post_button = driver.find_element(By.XPATH, "//div[@class='xi81zsa x1lkfr7t xkjl1po x1mzt3pk xh8yej3 x13faqbe']")
        create_post_button.click()
        time.sleep(2)

        # Thêm ảnh nếu có
        if image_path:
            photo_video_button = driver.find_element(By.XPATH, "//div[@aria-label='Ảnh/video']")
            photo_video_button.click()
            time.sleep(2)

            for _ in range(2):
                upload_input = driver.find_element(By.XPATH, "//input[@type='file']")
                upload_input.send_keys(image_path)
                time.sleep(2)

        # Viết nội dung bài đăng
        post_box = driver.find_element(By.XPATH, "//div[contains(@aria-label,'Bạn viết gì đi...') or contains(@aria-label, 'Tạo bài viết công khai...')]")
        post_box.click()
        for char in content:
            post_box.send_keys(char)
            time.sleep(0.000001)
        time.sleep(2)

        # Đăng bài
        '''post_button = driver.find_element(By.XPATH, "//div[@aria-label='Đăng']")
        post_button.click()
        time.sleep(3)'''

    except Exception as e:
        print(f"Failed to post in group {group_link}: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FacebookAutoPosterApp(root)
    root.mainloop()
