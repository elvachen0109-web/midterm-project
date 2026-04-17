
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup


def fetch_page(url: str, timeout: int = 10) -> str | None:
   
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
    demo_url = "https://codedamn-classrooms.github.io/webscraper-python-codedamn-classroom-website/?utm_source=chatgpt.com"
    print("正在取得網頁...")
    html = fetch_page(demo_url)
    
    
    if not html:
        print("無法取得網頁，請檢查網路連線。")
        return
    
    print("正在解析內容...\n")
    products = parse_products(html)
    ram_list = []
    
    print(f"共找到 {len(products)} 筆商品：\n")
    for i, p in enumerate(products, 1):
        print(f"{i}. 商品名稱:「{p['title']}」")
        print(f"  價格:{p['price']}")
        print(f"  描述:{p['description'][:50]}...")
        print(f"  評論數:{p['reviews']}")
        print("-" *40)

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
        

    print("商品數量：", len(products))
    print("RAM 清單：", ram_list)
    print("RAM 統計：", ram_count)

    plt.bar(ram_count.keys(), ram_count.values())
    plt.title("RAM Distribution")
    plt.xlabel("RAM")
    plt.ylabel("Count")
    plt.show()

if __name__ == "__main__":
    main()