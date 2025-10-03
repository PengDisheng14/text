import requests
from bs4 import BeautifulSoup
import time
import random

def get_product_quantity(url):
    """
    该函数用于从指定 URL 的网页中抓取数量数据。
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.xiaohongshu.com/', 
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Cache-Control': 'max-age=0'
        }
        
        # 添加随机延迟，避免请求过于频繁
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # 方法1：使用CSS选择器（推荐）
        quantity_element = soup.select_one('span.count[selected-disabled-search]')
        
        # 方法2：如果方法1不行，尝试这个
        if not quantity_element:
            quantity_element = soup.find('span', class_='count')
        
        # 方法3：如果还不行，尝试包含data-v属性
        if not quantity_element:
            quantity_element = soup.find('span', attrs={'class': 'count', 'selected-disabled-search': ''})
        
        if quantity_element:
            quantity_text = quantity_element.text.strip()
            return quantity_text
        else:
            # 调试信息：打印页面标题和部分HTML，帮助诊断问题
            print("页面标题:", soup.title.string if soup.title else "无标题")
            print("前500字符:", response.text[:500])
            return "未找到指定的数量元素"

    except requests.exceptions.RequestException as e:
        return f"请求失败: {e}"
    except Exception as e:
        return f"解析失败: {e}"

# 测试代码
product_url = "https://www.xiaohongshu.com/explore/68de38fc0000000004005e49?xsec_token=ABqVzw3wFZsWll1xtqZT-ZqusX4RFIji6ZKDWdilduA60=&xsec_source=pc_feed"
quantity = get_product_quantity(product_url)

print(f"数量是：{quantity}")