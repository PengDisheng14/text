from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

def get_product_quantity_with_profile(url):
    """
    使用已登录的Chrome配置文件访问网页
    """
    chrome_options = Options()
    
    # 获取Chrome用户数据目录路径
    # 通常路径如下，您可能需要根据实际情况调整
    chrome_user_data_dir = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data'
    
    chrome_options.add_argument(f'--user-data-dir={chrome_user_data_dir}')
    
    # 指定配置文件（Default是默认配置文件）
    chrome_options.add_argument('--profile-directory=Default')
    
    # 不使用无头模式，以便观察
    # chrome_options.add_argument('--headless')
    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        print("使用已登录的Chrome配置文件访问网页...")
        driver.get(url)
        
        # 等待页面加载
        time.sleep(8)
        
        # 检查当前页面标题和URL
        print(f"页面标题: {driver.title}")
        print(f"当前URL: {driver.current_url}")
        
        # 尝试多种方式查找数量元素
        selectors = [
            'span.count',
            '.count',
            'span[selected-disabled-search]',
            '[selected-disabled-search]'
        ]
        
        found = False
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"使用选择器 '{selector}' 找到 {len(elements)} 个元素:")
                    for i, element in enumerate(elements):
                        text = element.text.strip()
                        print(f"  元素 {i+1}: '{text}'")
                        if text and text.isdigit():
                            print(f"✅ 找到数量: {text}")
                            found = True
                            return text
            except Exception as e:
                print(f"选择器 '{selector}' 查找失败: {e}")
        
        if not found:
            # 保存截图和源代码用于调试
            driver.save_screenshot('with_profile_screenshot.png')
            with open('with_profile_source.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print("❌ 未找到数量元素，已保存截图和源代码")
            return "未找到数量元素"
            
    except Exception as e:
        print(f"错误: {e}")
        return f"执行失败: {e}"
    finally:
        if 'driver' in locals():
            input("按回车键关闭浏览器...")  # 暂停以便查看
            driver.quit()

# 测试代码
if __name__ == "__main__":
    product_url = "https://www.xiaohongshu.com/explore/68de38fc0000000004005e49?xsec_token=ABqVzw3wFZsWll1xtqZT-ZqusX4RFIji6ZKDWdilduA60=&xsec_source=pc_feed"
    
    quantity = get_product_quantity_with_profile(product_url)
    print(f"最终结果 - 数量是：{quantity}")