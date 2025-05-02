from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from config.settings import URL_LOGIN, USERNAME, PASSWORD, CHROME_DATA_DIR, MIN_DELAY, MAX_DELAY

class Browser:
    def __init__(self, headless=False):
        self.driver = None
        self.headless = headless
        
    def setup(self):
        """初始化浏览器"""
        chrome_options = Options()
        chrome_options.add_argument(f"--user-data-dir={CHROME_DATA_DIR}")
        chrome_options.add_argument("--profile-directory=Default")
        
        # 添加无头模式选项
        if self.headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")  # 某些系统上需要
            chrome_options.add_argument("--window-size=1920,1080")  # 设置窗口大小
            
            # 添加一些额外参数，减少无头模式被检测的可能性
            chrome_options.add_argument("--no-sandbox") 
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            
            # 模拟正常用户代理
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
            
            print("启用无头模式，浏览器将在后台运行")
            
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        # 在无头模式下执行额外步骤以避免被检测
        if self.headless:
            # 禁用webdriver特征标识，降低被检测为自动化工具的可能
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
        return self.driver
        
    def login(self):
        """登录到校园门户"""
        self.driver.get(URL_LOGIN)
        self.random_delay()
        
        self.driver.find_element(By.ID, "username").send_keys(USERNAME)
        self.random_delay()
        
        self.driver.find_element(By.ID, "password").send_keys(PASSWORD)
        self.random_delay()
        
        self.driver.find_element(By.ID, "login_submit").click()
        
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("personCenter")
        )
        print("登录成功")
        
    def random_delay(self):
        """随机延迟，模拟人类行为"""
        delay = random.uniform(MIN_DELAY, MAX_DELAY)
        time.sleep(delay)
        
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
