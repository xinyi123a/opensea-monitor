import streamlit as st
import requests
import os
from datetime import datetime

# 直接复用.env中的API密钥
from dotenv import load_dotenv
load_dotenv()  

# 网页界面
st.set_page_config(page_title="NFT监控", layout="wide")
st.title("🔍 我的私人NFT监控面板")

# 复用ceshi.py中的查询逻辑
def get_price(collection_slug):
    url = f"https://api.opensea.io/api/v2/collections/{collection_slug}/stats"
    headers = {"X-API-KEY": os.getenv("OPENSEA_API_KEY")}
    try:
        data = requests.get(url, headers=headers).json()
        return data["total"]["floor_price"]
    except:
        return None

# 侧边栏控制
with st.sidebar:
    st.header("控制面板")
    nft_name = st.text_input("NFT集合名称", "boredapeyachtclub")
    if st.button("实时查询"):
        price = get_price(nft_name)
        if price:
            st.success(f"当前地板价: {price:.4f} ETH")
            # 自动记录到原有日志文件
            with open("nft_price_log.txt", "a") as f:
                f.write(f"{datetime.now()} {nft_name} {price}\n")
        else:
            st.error("查询失败")

# 显示历史日志
if st.checkbox("查看完整记录"):
    with open("nft_price_log.txt") as f:
        st.code(f.read())