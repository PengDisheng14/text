from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_product_quantity_selenium(url):
    """
    使用Selenium从指定URL的网页中抓取数量数据
    """
    # Chrome浏览器选项设置
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式，不显示浏览器窗口
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # 设置User-Agent
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = None
    try:
        # 启动浏览器
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 访问网页
        print("正在访问网页...")
        driver.get(url)
        
        # 等待页面加载
        time.sleep(5)
        
        # 方法1：使用显式等待查找元素
        print("尝试查找数量元素...")
        try:
            wait = WebDriverWait(driver, 10)
            quantity_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span.count[selected-disabled-search]'))
            )
            quantity_text = quantity_element.text.strip()
            print(f"找到元素，文本内容: '{quantity_text}'")
            return quantity_text
            
        except Exception as e:
            print(f"方法1失败: {e}")
            
        # 方法2：尝试其他选择器
        try:
            quantity_element = driver.find_element(By.CLASS_NAME, 'count')
            quantity_text = quantity_element.text.strip()
            print(f"方法2找到元素，文本内容: '{quantity_text}'")
            return quantity_text
        except Exception as e:
            print(f"方法2失败: {e}")
            
        # 方法3：查找包含特定属性的span
        try:
            quantity_element = driver.find_element(By.CSS_SELECTOR, 'span[class="count"]')
            quantity_text = quantity_element.text.strip()
            print(f"方法3找到元素，文本内容: '{quantity_text}'")
            return quantity_text
        except Exception as e:
            print(f"方法3失败: {e}")
            
        # 方法4：打印页面源代码帮助调试
        print("=== 页面源代码前2000字符 ===")
        print(driver.page_source[:2000])
        print("=== 源代码结束 ===")
        
        return "未找到指定的数量元素"
        
    except Exception as e:
        return f"Selenium执行失败: {e}"
        
    finally:
        # 确保浏览器被关闭
        if driver:
            driver.quit()
            print("浏览器已关闭")

# 测试代码
if __name__ == "__main__":
    product_url = "https://www.xiaohongshu.com/explore/68de38fc0000000004005e49?xsec_token=ABqVzw3wFZsWll1xtqZT-ZqusX4RFIji6ZKDWdilduA60=&xsec_source=pc_feed"
    
    print("开始使用Selenium获取数量...")
    quantity = get_product_quantity_selenium(product_url)
    print(f"数量是：{quantity}")