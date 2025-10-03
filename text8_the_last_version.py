from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def get_xhs_quantity_with_manual_chrome(url):
    """
    使用手动指定的ChromeDriver获取小红书数量信息
    """
    # 在启动前，建议手动关闭所有Chrome浏览器进程
    chrome_options = Options()
    
    # 使用您已登录的Chrome用户配置文件，避免重复登录
    chrome_user_data_dir = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data'
    chrome_options.add_argument(f'--user-data-dir={chrome_user_data_dir}')
    chrome_options.add_argument('--profile-directory=Default')
    
    # 重要的配置选项
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = None
    try:
        print("正在启动Chrome浏览器...")
        # 关键步骤：使用手动下载的ChromeDriver
        service = Service(executable_path='./chromedriver.exe')  # 确保路径正确
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 隐藏WebDriver特征
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("正在访问小红书页面...")
        driver.get(url)
        
        # 使用WebDriverWait显式等待，而不是固定时间的time.sleep
        wait = WebDriverWait(driver, 15)  # 最长等待15秒
        print("页面加载中，等待目标元素...")
        
        # 尝试多种可能的选择器来定位数量元素
        selectors_to_try = [
            'span.count',
            '.count',
            'span[selected-disabled-search]',
            '[class*="count"]'
        ]
        
        quantity = "未找到数量元素"
        for selector in selectors_to_try:
            try:
                print(f"尝试定位元素，选择器: {selector}")
                # 等待元素出现并获取文本
                quantity_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                found_text = quantity_element.text.strip()
                if found_text and found_text.isdigit():
                    quantity = found_text
                    print(f"成功找到数量: {quantity}")
                    break
            except Exception as e:
                print(f"使用选择器 '{selector}' 未找到元素: {e}")
                continue
        
        if quantity == "未找到数量元素":
            print("所有选择器均未找到目标元素。尝试查找页面中所有数字...")
            # 备选方案：查找页面中的所有数字
            all_spans = driver.find_elements(By.TAG_NAME, 'span')
            for span in all_spans:
                text = span.text.strip()
                if text and text.isdigit() and 10 <= int(text) <= 1000000:  # 假设一个合理的范围
                    print(f"通过备选方案找到数字: {text}")
                    quantity = text
                    break

        return quantity

    except Exception as e:
        print(f"程序执行过程中出现异常: {e}")
        return f"执行失败: {e}"
    finally:
        if driver:
            print("程序执行完毕，关闭浏览器...")
            driver.quit()

# 使用示例
if __name__ == "__main__":
    product_url = "https://www.xiaohongshu.com/explore/68de38fc0000000004005e49?xsec_token=ABqVzw3wFZsWll1xtqZT-ZqusX4RFIji6ZKDWdilduA60=&xsec_source=pc_feed"
    result = get_xhs_quantity_with_manual_chrome(product_url)
    print(f"最终结果: {result}")