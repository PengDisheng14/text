from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import os

def get_product_quantity_edge(url):
    """
    使用Edge浏览器访问网页
    """
    edge_options = Options()
    
    # 使用Edge用户数据（如果已登录）
    edge_user_data_dir = os.path.expanduser('~') + r'\AppData\Local\Microsoft\Edge\User Data'
    if os.path.exists(edge_user_data_dir):
        edge_options.add_argument(f'--user-data-dir={edge_user_data_dir}')
        edge_options.add_argument('--profile-directory=Default')
    
    # 其他配置
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')
    edge_options.add_argument('--disable-blink-features=AutomationControlled')
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    try:
        print("正在启动Edge浏览器...")
        
        # 自动管理Edge驱动
        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=edge_options)
        
        # 隐藏自动化特征
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("正在访问目标网页...")
        driver.get(url)
        
        # 等待页面加载
        wait = WebDriverWait(driver, 20)
        print("等待页面加载完成...")
        
        # 检查页面状态
        print(f"页面标题: {driver.title}")
        print(f"当前URL: {driver.current_url}")
        
        # 如果被重定向到登录页，手动处理
        if any(keyword in driver.current_url.lower() for keyword in ['login', 'signin', 'auth']) or any(keyword in driver.title.lower() for keyword in ['登录', 'sign in']):
            print("检测到登录页面...")
            input("请在浏览器中完成登录，然后按回车键继续...")
        
        # 查找数量元素
        quantity = find_quantity_elements_comprehensive(driver, wait)
        
        if quantity != "未找到数量元素":
            print(f"✅ 成功获取数量: {quantity}")
        else:
            print("尝试其他查找策略...")
            quantity = alternative_search_strategies(driver)
        
        return quantity
        
    except Exception as e:
        print(f"❌ 程序执行失败: {e}")
        return f"执行失败: {e}"
    finally:
        if driver:
            print("正在关闭浏览器...")
            driver.quit()

def find_quantity_elements_comprehensive(driver, wait):
    """综合查找策略"""
    print("开始查找数量元素...")
    
    # 多种选择器
    selectors = [
        'span.count',
        '.count',
        'span[selected-disabled-search]',
        '[selected-disabled-search]',
        '[class*="count"]',
        '[class*="Count"]',
        '.like-count',
        '.likes-count',
        '[data-v-dc3a3972]',  # 您HTML中的data属性
    ]
    
    for selector in selectors:
        try:
            print(f"尝试选择器: {selector}")
            elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
            for element in elements:
                text = element.text.strip()
                if text and text.isdigit():
                    print(f"🎉 使用选择器 '{selector}' 找到数量: {text}")
                    return text
        except:
            continue
    
    return "未找到数量元素"

def alternative_search_strategies(driver):
    """备选查找策略"""
    print("使用备选策略查找...")
    
    # 查找所有包含数字的元素
    all_elements = driver.find_elements(By.XPATH, "//*[text()[number(.)=number(.)]]")
    for element in all_elements:
        text = element.text.strip()
        if text.isdigit() and 10 <= int(text) <= 100000:  # 合理的数量范围
            print(f"🎉 通过数字查找找到: {text}")
            return text
    
    # 保存调试信息
    driver.save_screenshot('edge_debug.png')
    with open('edge_page_source.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("已保存调试信息")
    
    return "未找到数量元素"

# 测试
if __name__ == "__main__":
    product_url = "https://www.xiaohongshu.com/explore/68de38fc0000000004005e49?xsec_token=ABqVzw3wFZsWll1xtqZT-ZqusX4RFIji6ZKDWdilduA60=&xsec_source=pc_feed"
    
    print("=== 使用Edge浏览器 ===")
    quantity = get_product_quantity_edge(product_url)
    print(f"=== 最终结果: {quantity} ===")