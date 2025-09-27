import requests
from bs4 import BeautifulSoup

def get_product_quantity(url):
    """
    该函数用于从指定 URL 的网页中抓取产品数量数据。
    """
    try:
        # 添加一个伪装成浏览器的 User-Agent
        headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/', # 可选，伪装成从谷歌搜索进入
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}
        # 发送 HTTP GET 请求到目标 URL，并带上自定义的头部
        response = requests.get(url, headers=headers)
        
        # 检查响应状态码，确保请求成功（状态码 200）
        response.raise_for_status()

        # 使用 Beautiful Soup 解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # === 这里是您需要修改的部分 ===
        # 假设数量数据在一个 <span class="quantity"> 标签中
        # 您需要根据您在开发者工具中找到的标签、类名或ID来更改它
        quantity_element = soup.find('div', id='post-wpulike')
        
        # 检查是否找到了元素
        if quantity_element:
            # 提取文本内容并去除首尾空白
            quantity_text = quantity_element.text.strip()
            return quantity_text
        else:
            return "未找到指定的数量元素"

    except requests.exceptions.RequestException as e:
        # 处理可能的网络或请求错误
        return f"请求失败: {e}"

# === 这里也需要您修改，替换成您想要抓取的具体网页 URL ===
product_url = "https://momon-ga.com/fanzine/mo2748134/"
quantity = get_product_quantity(product_url)

# 在终端中打印结果
print(f"该产品的数量是：{quantity}")