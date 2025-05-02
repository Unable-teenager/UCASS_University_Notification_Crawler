from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback
from config.settings import URL_NOTIFYLIST
from models.notification import Notification

class Scraper:
    def __init__(self, browser, storage):
        self.driver = browser.driver
        self.browser = browser
        self.storage = storage
        self.continue_on_duplicate = None
        
    def get_total_pages(self):
        """获取分页组件中的总页数"""
        self.driver.get(URL_NOTIFYLIST)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "newstitle"))
        )
        
        pagination = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "el-pagination"))
        )
        
        # 获取最后一个页码（总页数）
        last_page = pagination.find_elements(By.CSS_SELECTOR, "ul.el-pager li.number")[-1]
        return int(last_page.text)
    
    def process_notification(self, notification_element, index):
        """处理单条通知"""
        notification = Notification()
        log_errors = []
        
        try:
            # 提取通知标题
            title_element = notification_element.find_element(By.CLASS_NAME, "newstopcont")
            notification.title = title_element.text.strip()
            print(f"Title: {notification.title}")
            
            # 获取时间、通知来源
            time_container = notification_element.find_element(By.CLASS_NAME, "newsbotomcont")
            time_elements = time_container.find_elements(By.TAG_NAME, "div")
            
            # 分别提取时间、来源、通知类型
            notification.time = time_elements[0].text.strip()
            notification.source = time_elements[1].text.strip()
            notification.type = time_elements[2].text.strip()
            
            print(f"Time: {notification.time}")
            print(f"Source: {notification.source}")
            print(f"Type: {notification.type}")
            
            # 检查是否是重复通知
            if self.storage.is_notification_in_history(notification):
                print(f"警告: 检测到重复通知 '{notification.title}'")
                if self.continue_on_duplicate is None:
                    # 询问用户是否继续
                    user_input = input("检测到重复通知，是否继续爬取? (y/n): ").lower()
                    self.continue_on_duplicate = user_input.startswith('y')
                
                if not self.continue_on_duplicate:
                    print("用户选择停止爬取。")
                    return None
                
                print("继续爬取...")
            
        except Exception as e:
            error_msg = f"Error extracting notification basic info: {str(e)}"
            log_errors.append(error_msg)
            print(error_msg)
            
        try:
            # 点击通知链接进入详情页
            title_element.click()
            # 切换到新窗口
            self.driver.switch_to.window(self.driver.window_handles[-1])
            # 等待详情页加载完成
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "contenter"))
            )
            
            # 提取正文内容
            try:
                content_div = self.driver.find_element(By.CLASS_NAME, "notice-text")
                paragraphs = content_div.find_elements(By.TAG_NAME, "p")
                
                notification.content = "\n".join([p.text.strip() for p in paragraphs if p.text.strip()])
                print("正文内容已提取")
            except Exception as e:
                error_msg = f"无法提取正文内容: {str(e)}"
                log_errors.append(error_msg)
                print(error_msg)
                
            # 提取附件信息
            try:
                attachment_div = self.driver.find_element(By.CLASS_NAME, "footatext")
                attachments = attachment_div.find_elements(By.TAG_NAME, "a")
                
                for a in attachments:
                    file_name = a.get_attribute("download")
                    file_url = a.get_attribute("href")
                    notification.attachments.append({
                        "name": file_name,
                        "url": file_url
                    })
                print(f"已提取 {len(notification.attachments)} 个附件")
            except Exception as e:
                error_msg = f"无法提取附件信息: {str(e)}"
                log_errors.append(error_msg)
                print(error_msg)
                
        except Exception as e:
            error_msg = f"Error accessing notification detail page: {str(e)}"
            log_errors.append(error_msg)
            print(error_msg)
        finally:
            # 返回原列表页
            try:
                self.driver.back()
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "newstitle"))
                )
            except Exception as e:
                log_errors.append(f"Error reloading list page: {str(e)}")
        
        # 保存通知到文件
        self.storage.save_notification(notification, index)
        
        # 记录错误信息
        if log_errors:
            self.storage.log_error(notification.title, log_errors)
            
        return notification
    
    def scrape_current_page(self):
        """爬取当前页面上的所有通知"""
        time.sleep(1)
        current_notifications = self.driver.find_elements(By.CLASS_NAME, "newstitle")
        total_count = len(current_notifications)
        print(f"发现 {total_count} 条通知")
        
        for i in range(total_count):
            if i < len(current_notifications):
                print(f"正在处理第 {i+1}/{total_count} 条通知")
                result = self.process_notification(current_notifications[i], i)
                if result is None:  # 用户选择停止爬取
                    return False
                    
        return True
    
    def scrape_all_pages(self):
        """爬取所有页面的通知"""
        try:
            # 获取总页数
            total_pages = self.get_total_pages()
            print(f"检测到总页数: {total_pages}")
            
            # 导航到列表页面
            self.driver.get(URL_NOTIFYLIST)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "newstitle"))
            )

            # 遍历每一页
            for page_num in range(1, total_pages + 1):
                self.browser.random_delay()
                print(f"\n=== 正在处理第 {page_num} 页，共 {total_pages} 页 ===")
                
                # 处理当前页面上的所有通知
                continue_scraping = self.scrape_current_page()
                if not continue_scraping:
                    print("用户选择停止爬取，爬虫终止。")
                    break
                
                # 页面间添加延迟
                print(f"等待1秒后处理下一页...")
                time.sleep(1)

                # 进入下一页
                if page_num < total_pages:
                    # 点击下一页按钮
                    next_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "btn-next"))
                    )
                    next_button.click()
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "newstitle"))
                    )
                    
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "newstitle"))
                )
                
        except Exception as e:
            print(f"爬取过程中出错: {str(e)}")
            traceback.print_exc()
