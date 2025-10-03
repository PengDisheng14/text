from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import base64

def debug_page_analysis(url):
    """
    详细诊断页面，找出问题所在
    """
    chrome_options = Options()
    # 先不使用无头模式，以便观察
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("=== 开始页面诊断 ===")
        driver.get(url)
        
        # 等待更长时间
        print("等待页面加载...")
        time.sleep(10)
        
        # 1. 检查页面标题
        print(f"1. 页面标题: {driver.title}")
        
        # 2. 检查当前URL（看是否被重定向）
        print(f"2. 当前URL: {driver.current_url}")
        
        # 3. 截图保存，查看页面实际显示内容
        driver.save_screenshot('page_screenshot.png')
        print("3. 页面截图已保存为 'page_screenshot.png'")
        
        # 4. 获取页面源代码
        page_source = driver.page_source
        print(f"4. 页面源代码长度: {len(page_source)} 字符")
        
        # 5. 搜索包含"425"或"count"的文本
        print("5. 搜索包含数字和count的内容:")
        if "425" in page_source:
            print("   - 找到 '425' 在源代码中")
            # 找到425周围的上下文
            index = page_source.find("425")
            context = page_source[max(0, index-100):min(len(page_source), index+100)]
            print(f"   上下文: ...{context}...")
        else:
            print("   - 未找到 '425' 在源代码中")
            
        if "count" in page_source.lower():
            print("   - 找到 'count' 在源代码中")
            # 找到所有count出现的位置
            count_index = page_source.lower().find("count")
            context = page_source[max(0, count_index-150):min(len(page_source), count_index+150)]
            print(f"   上下文: ...{context}...")
        else:
            print("   - 未找到 'count' 在源代码中")
        
        # 6. 尝试多种选择器查找元素
        print("6. 尝试各种选择器:")
        selectors = [
            'span.count',
            '.count',
            '[class*="count"]',
            'span[selected-disabled-search]',
            '[selected-disabled-search]'
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                print(f"   选择器 '{selector}': 找到 {len(elements)} 个元素")
                for i, element in enumerate(elements):
                    print(f"     元素 {i+1}: 文本='{element.text}'")
            except Exception as e:
                print(f"   选择器 '{selector}': 错误 - {e}")
        
        # 7. 查找所有span元素
        print("7. 查看所有span元素:")
        spans = driver.find_elements(By.TAG_NAME, 'span')
        count_spans = [span for span in spans if span.text.isdigit()]
        print(f"   找到 {len(count_spans)} 个包含数字的span")
        for span in count_spans[:10]:  # 只显示前10个
            print(f"   数字span: '{span.text}'")
            
    except Exception as e:
        print(f"诊断过程中出错: {e}")
    finally:
        input("按回车键关闭浏览器...")  # 暂停，让你有时间查看浏览器
        driver.quit()

# 运行诊断
product_url = "https://www.xiaohongshu.com/explore/68de38fc0000000004005e49?xsec_token=ABqVzw3wFZsWll1xtqZT-ZqusX4RFIji6ZKDWdilduA60=&xsec_source=pc_feed"
debug_page_analysis(product_url)