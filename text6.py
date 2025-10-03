from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import os

def get_product_quantity_optimized(url):
    """
    使用webdriver-manager自动管理ChromeDriver版本
    """
    chrome_options = Options()
    
    # 使用现有Chrome配置文件
    chrome_user_data_dir = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data'
    chrome_options.add_argument(f'--user-data-dir={chrome_user_data_dir}')
    chrome_options.add_argument('--profile-directory=Default')
    
    # 重要：添加这些参数避免DevToolsActivePort错误
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--remote-debugging-port=9222')
    
    # 可选：禁用自动化控制特征
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    try:
        print("正在启动Chrome浏览器...")
        
        # 使用webdriver-manager自动管理驱动版本
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 隐藏自动化特征
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("正在访问目标网页...")
        driver.get(url)
        
        # 使用显式等待而不是固定sleep
        wait = WebDriverWait(driver, 15)
        
        # 等待页面加载完成
        print("等待页面加载...")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # 检查是否成功访问目标页面
        print(f"页面标题: {driver.title}")
        print(f"当前URL: {driver.current_url}")
        
        # 如果被重定向到登录页，给出提示
        if any(keyword in driver.current_url.lower() for keyword in ['login', 'signin', 'auth']) or any(keyword in driver.title.lower() for keyword in ['登录', 'sign in']):
            print("检测到登录页面，请在浏览器中手动操作...")
            input("完成登录后按回车键继续...")
        
        # 主动查找数量元素
        quantity = find_quantity_elements(driver, wait)
        
        if quantity != "未找到数量元素":
            print(f"✅ 成功获取数量: {quantity}")
        else:
            print("❌ 未找到数量元素")
            # 保存页面信息用于调试
            driver.save_screenshot('debug_screenshot.png')
            with open('debug_page_source.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print("已保存截图和页面源代码用于调试")
        
        return quantity
        
    except Exception as e:
        print(f"❌ 程序执行失败: {e}")
        return f"执行失败: {e}"
    finally:
        if driver:
            print("正在关闭浏览器...")
            driver.quit()

def find_quantity_elements(driver, wait):
    """
    使用多种策略查找数量元素
    """
    print("开始查找数量元素...")
    
    # 策略1：等待特定元素出现
    selectors_to_try = [
        'span.count',
        '.count',
        'span[selected-disabled-search]',
        '[selected-disabled-search]',
        '[class*="count"]',
        '[class*="Count"]',
    ]
    
    for selector in selectors_to_try:
        try:
            print(f"尝试选择器: {selector}")
            elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
            if elements:
                for i, element in enumerate(elements):
                    text = element.text.strip()
                    if text and text.isdigit():
                        print(f"🎉 使用选择器 '{selector}' 找到数量: {text}")
                        return text
                    elif text:
                        print(f"找到元素但非数字: '{text}'")
        except Exception as e:
            print(f"选择器 '{selector}' 未找到元素: {e}")
    
    # 策略2：查找所有包含数字的span
    try:
        print("尝试查找所有数字span...")
        all_spans = driver.find_elements(By.TAG_NAME, 'span')
        digit_spans = [span for span in all_spans if span.text.strip().isdigit()]
        
        print(f"找到 {len(digit_spans)} 个包含数字的span")
        for span in digit_spans:
            text = span.text.strip()
            print(f"数字span: '{text}'")
            # 如果数字在合理范围内（比如点赞数、收藏数）
            if text.isdigit() and 1 <= int(text) <= 1000000:
                print(f"🎉 找到合理的数量值: {text}")
                return text
    except Exception as e:
        print(f"查找数字span失败: {e}")
    
    return "未找到数量元素"

# 测试代码
if __name__ == "__main__":
    product_url = "https://www.xiaohongshu.com/explore/68de38fc0000000004005e49?xsec_token=ABqVzw3wFZsWll1xtqZT-ZqusX4RFIji6ZKDWdilduA60=&xsec_source=pc_feed"
    
    print("=== 开始执行优化版本 ===")
    quantity = get_product_quantity_optimized(product_url)
    print(f"=== 最终结果: {quantity} ===")