from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

def simple_test():
    """最简单的测试版本"""
    chrome_options = Options()
    
    # 最小化配置
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # 不使用用户数据，先测试基本功能
    # chrome_options.add_argument('--headless')  # 可以先注释掉
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ Chrome启动成功")
        driver.get("https://www.baidu.com")
        print(f"✅ 页面访问成功，标题: {driver.title}")
        
        time.sleep(3)
        driver.quit()
        print("✅ 测试完成")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")

# 先运行基础测试
print("运行基础功能测试...")
simple_test()