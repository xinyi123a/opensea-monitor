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
        print("❌ 未设置API密钥")
        return None
    
    url = f"https://api.opensea.io/api/v2/collections/{collection_slug}/stats"
    headers = {"accept": "application/json", "x-api-key": api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=3)
        response.raise_for_status()
        return response.json().get("total", {}).get("floor_price", 0)
    except Exception as e:
        print(f"❌ {collection_slug}查询失败: {str(e)[:50]}")
        return None

def run_query_cycle(collections):
    """执行单次查询周期"""
    results = {}
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_nft_floor_price, slug): slug for slug in collections}
        for future in concurrent.futures.as_completed(futures):
            slug = futures[future]
            results[slug] = future.result()
    
    # 清屏并打印结果（Windows用'cls'，Mac/Linux用'clear'）
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"🔄 最后更新: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    for slug, price in results.items():
        print(f"{slug.upper():<20} {price if price is not None else '--':>8} ETH")
    
    return time.time() - start_time

def main():
    collections = ["pudgypenguins", "boredapeyachtclub"]
    query_count = 0
    
    try:
        while True:
            query_count += 1
            print(f"\n▶️ 第 {query_count} 次查询开始...")
            
            cycle_time = run_query_cycle(collections)
            sleep_time = max(10 - cycle_time, 0)  # 确保至少间隔10秒
            
            print(f"\n⏳ 下次更新在 {sleep_time:.1f} 秒后 (Ctrl+C退出)")
            time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        print("\n🛑 已手动停止查询")

if __name__ == "__main__":
    main()