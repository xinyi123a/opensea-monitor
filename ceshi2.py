import os
import requests
from dotenv import load_dotenv
import time
import concurrent.futures

# 加载环境变量
load_dotenv()

def get_nft_floor_price(collection_slug):
    """获取NFT地板价"""
    api_key = os.getenv("OPENSEA_API_KEY")
    if not api_key:
        return None
    
    url = f"https://api.opensea.io/api/v2/collections/{collection_slug}/stats"
    headers = {"accept": "application/json", "x-api-key": api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=3)
        response.raise_for_status()
        return response.json().get("total", {}).get("floor_price", 0)
    except:
        return None

def main():
    collections = ["pudgypenguins", "boredapeyachtclub"]
    results = {}
    
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_nft_floor_price, slug): slug for slug in collections}
        for future in concurrent.futures.as_completed(futures):
            slug = futures[future]
            results[slug] = future.result()
    
    print("\nNFT地板价查询结果：")
    for slug, price in results.items():
        print(f"{slug.upper():<20} {price if price is not None else '查询失败'} ETH")
    
    print(f"\n总耗时: {time.time() - start_time:.2f}秒")

if __name__ == "__main__":
    main()