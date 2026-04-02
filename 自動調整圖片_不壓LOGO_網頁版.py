# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:51:56 2026

@author: louis_chang_hhgalaxy
"""

import streamlit as st
from PIL import Image, ImageOps
import io
import zipfile

# --- 設定區 ---
OUTPUT_SIZE = (1000, 1000)

# --- 網頁介面設計 ---
st.set_page_config(page_title="圖片自動裁切神器", page_icon="✂️")
st.title("🚀 圖片批次裁切 (不壓LOGO)")
st.write("請上傳你的圖片，系統會自動幫你置中裁切成 1000x1000！")

st.divider()

# 1. 上傳要處理的圖片
st.subheader("📁 上傳要處理的圖片 (可多選)")
uploaded_images = st.file_uploader("請點擊或拖曳上傳圖片", type=['png', 'jpg', 'jpeg', 'webp', 'bmp'], accept_multiple_files=True)

# 2. 執行按鈕
if st.button("✨ 開始批次裁切", type="primary"):
    if not uploaded_images:
        st.warning("⚠️ 請務必先上傳至少一張圖片喔！")
    else:
        with st.spinner("圖片火力處理中..."):
            try:
                # 建立一個存在記憶體中的 ZIP 檔案，用來裝處理好的圖片
                zip_buffer = io.BytesIO()
                
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    for img_file in uploaded_images:
                        # 讀取上傳的圖片
                        img = Image.open(img_file).convert("RGBA")
                        
                        # 處理圖片：等比例縮放裁切至 1000x1000
                        img_resized = ImageOps.fit(img, OUTPUT_SIZE, Image.Resampling.LANCZOS, centering=(0.5, 0.5))
                        
                        # 準備存檔：轉回 RGB (去除透明度以存為 JPEG)
                        final_img = img_resized.convert("RGB")
                        
                        # 將處理好的圖片存入記憶體中
                        img_byte_arr = io.BytesIO()
                        final_img.save(img_byte_arr, format='JPEG', quality=90)
                        
                        # 將這張圖片寫入 ZIP 檔中
                        zip_file.writestr(f"processed_{img_file.name}", img_byte_arr.getvalue())
                
                st.success(f"🎉 處理成功！共完成了 {len(uploaded_images)} 張圖片。")
                
                # 產生下載按鈕，讓使用者下載打包好的 ZIP 檔
                st.download_button(
                    label="📥 下載處理好的圖片 (ZIP 壓縮檔)",
                    data=zip_buffer.getvalue(),
                    file_name="processed_images.zip",
                    mime="application/zip"
                )

            except Exception as e:
                st.error(f"發生錯誤了：{e}")