from lib.browser import Browser
from lib.storage import Storage
from lib.scraper import Scraper
import argparse

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description='UCASS校园门户通知爬虫')
    parser.add_argument('--headless', action='store_true', help='以无头模式运行(不显示浏览器界面)')
    args = parser.parse_args()
    
    # 初始化浏览器，根据参数决定是否使用无头模式
    browser = Browser(headless=args.headless)
    browser.setup()
    
    try:
        # 登录
        browser.login()
        
        # 初始化存储
        storage = Storage()
        
        # 初始化爬虫
        scraper = Scraper(browser, storage)
        
        # 开始爬取
        scraper.scrape_all_pages()
        
    except Exception as e:
        print(f"程序运行出错: {str(e)}")
    finally:
        browser.close()

if __name__ == "__main__":
    main()
