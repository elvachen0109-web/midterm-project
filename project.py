"""
爬蟲網址:https://codedamn-classrooms.github.io/webscraper-python-codedamn-classroom-website/?utm_source=chatgpt.com
"""
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup



"""
從網站抓取HTML
"""
def fetch_page(url: str, timeout: int = 10) -> str | None:
    """
    取得網頁原始 HTML 內容。
    
    Args:
        url: 目標網址
        timeout: 請求逾時秒數
        
    Returns:
        成功回傳 HTML 字串，失敗回傳 None
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Demo-Scraper/1.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"請求失敗: {e}")
        return None


def parse_products(html: str) -> list[dict]:
    """
    從HTML找出商品資料:商品名稱、價格、描述、評論數
    再放入products中
    Returns:
        包含products的列表
    """
    
    soup = BeautifulSoup(html, "html.parser")
    #print(soup.prettify()[:1000])
    
    products = []

    
    
    for product in soup.select(".thumbnail"):
        title_elem = product.find("a", class_="title")
        price_elem = product.find("h4", class_="price")
        desc_elem = product.find("p", class_="description")
        review_elem = product.find("p", class_="pull-right")

        
        if title_elem and price_elem and desc_elem and review_elem:
            products.append({
                "title": title_elem.get_text(strip=True),
                "price": price_elem.get_text(strip=True),
                "description": desc_elem.get_text(strip=True),
                "reviews": review_elem.get_text(strip=True),
            })
    
    return products


def main():

    """
    抓取網站1~3頁資訊，在解析商品，印出每個商品資訊
    """
    demo_url = "https://codedamn-classrooms.github.io/webscraper-python-codedamn-classroom-website/?utm_source=chatgpt.com"
    print("正在取得網頁...")
    html = fetch_page(demo_url)
    
    if not html:
        print("無法取得網頁，請檢查網路連線。")
        return
    
    print("正在解析內容...\n")
    products = parse_products(html)

    base_url = "https://codedamn-classrooms.github.io/webscraper-python-codedamn-classroom-website/"
    all_products = []
    for page in range(1,4):
        url = f"{base_url}?page={page}"
        print(f"正在抓第{page}頁:{url}")
        html = fetch_page(url)
        if not html:
            continue
        products = parse_products(html)
        all_products.extend(products)

    ram_list = []
    
    print(f"共找到 {len(all_products)} 筆商品：\n")
    for i, p in enumerate(all_products, 1):
        print(f"{i}. 商品名稱:「{p['title']}」")
        print(f"  價格:{p['price']}")
        print(f"  描述:{p['description'][:50]}...")
        print(f"  評論數:{p['reviews']}")
        print("-" *40)
    
        """
        從描述中找到RAM的容量，再統計每種RAM出現次數
        """
        desc = p['description']
        if  "4GB" in desc:
            ram_list.append("4GB") 
        elif  "8GB" in desc:
            ram_list.append("8GB") 
        elif  "16GB" in desc:
            ram_list.append("16GB") 
    ram_count = {}
    for ram in ram_list:
        if ram in ram_count:
            ram_count[ram] += 1
        else:
            ram_count[ram] = 1
        

    print("商品數量：", len(all_products))
    print("RAM 清單：", ram_list)
    print("RAM 統計：", ram_count)

    """
    畫出RAM的統計長條圖
    """
    plt.bar(ram_count.keys(), ram_count.values())
    plt.title("RAM Distribution")
    plt.xlabel("RAM")
    plt.ylabel("Count")
    plt.show()

if __name__ == "__main__":
    main()

