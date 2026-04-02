import tkinter as tk
from tkinter import filedialog, messagebox
import os
# 注意：這裡新增了 ImageOps 的引入
from PIL import Image, ImageOps

def process_images():
    # 取得輸入框中的路徑
    input_folder = entry_input.get()
    logo_path = entry_logo.get()
    output_folder = entry_output.get()

    # 檢查是否都有填寫
    if not input_folder or not output_folder or not logo_path:
        messagebox.showwarning("警告", "請先選擇所有需要的資料夾與 LOGO 檔案！")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 載入 LOGO
    try:
        logo = Image.open(logo_path).convert("RGBA")
    except Exception as e:
        messagebox.showerror("錯誤", f"無法讀取 LOGO 圖片：{e}")
        return

    # 設定目標尺寸為 1000 x 1000
    target_size = (1000, 1000)

    # 確保 LOGO 本身也是等比例縮放，不會變形
    # (此處假設 LOGO 最大的限制為 300x300，並保持其原比例)
    logo_width, logo_height = logo.size
    if logo_width > 1000 or logo_height > 1000:
        logo.thumbnail((300, 300), Image.Resampling.LANCZOS)
        logo_width, logo_height = logo.size

    supported_formats = ('.png', '.jpg', '.jpeg', '.webp', '.bmp')
    count = 0

    # 更新狀態文字
    lbl_status.config(text="處理中，請稍候...", fg="blue")
    window.update() # 強制更新畫面

    # 開始處理圖片
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_formats):
            img_path = os.path.join(input_folder, filename)
            try:
                img = Image.open(img_path).convert("RGBA")

                # 🚀 關鍵修正點：使用 ImageOps.fit 進行等比例縮放並置中裁切 🚀
                # centering=(0.5, 0.5) 表示從圖片的中央開始裁切
                img_resized = ImageOps.fit(img, target_size, Image.Resampling.LANCZOS, centering=(0.5, 0.5))
                
                # 更新：將 LOGO 位置移至左上角，如你的手動範例所示
                margin = 10
                position = (margin, margin) 
                
                # 貼上 LOGO (保留透明度)
                img_resized.paste(logo, position, logo)
                
                # 準備存檔：轉回 RGB 並儲存
                final_img = img_resized.convert("RGB")
                output_filename = f"processed_{filename}"
                output_path = os.path.join(output_folder, output_filename)
                
                final_img.save(output_path, "JPEG", quality=90)
                count += 1
            except Exception as e:
                print(f"處理 {filename} 時發生錯誤: {e}")

    # 處理完成通知
    lbl_status.config(text=f"處理完成！共處理了 {count} 張圖片。", fg="green")
    messagebox.showinfo("成功", f"太棒了！已經成功處理並儲存 {count} 張圖片。")


# --- 以下為介面 (UI) 設計區塊 (保持不變，只增加一個提示) ---

# 按鈕對應的功能：打開選擇視窗，並把路徑填入輸入框
def select_input():
    folder = filedialog.askdirectory(title="選擇原始圖片資料夾")
    entry_input.delete(0, tk.END)
    entry_input.insert(0, folder)

def select_logo():
    file = filedialog.askopenfilename(title="選擇 LOGO 檔案", filetypes=[("圖片檔", "*.png *.jpg *.jpeg")])
    entry_logo.delete(0, tk.END)
    entry_logo.insert(0, file)

def select_output():
    folder = filedialog.askdirectory(title="選擇儲存資料夾")
    entry_output.delete(0, tk.END)
    entry_output.insert(0, folder)

# 建立主視窗
window = tk.Tk()
window.title("圖片批次處理小工具 (比例修正版)")
window.geometry("450x380")
window.resizable(False, False) # 固定視窗大小

# 1. 選擇原始圖片資料夾
tk.Label(window, text="1. 選擇「原始圖片」資料夾：", font=("Arial", 10)).pack(pady=(15, 2))
entry_input = tk.Entry(window, width=50)
entry_input.pack()
tk.Button(window, text="📁 瀏覽...", command=select_input).pack(pady=(2, 10))

# 2. 選擇 LOGO 檔案
tk.Label(window, text="2. 選擇「LOGO」圖片檔 (建議使用去背 PNG)：", font=("Arial", 10)).pack(pady=(5, 2))
entry_logo = tk.Entry(window, width=50)
entry_logo.pack()
tk.Button(window, text="🖼️ 瀏覽...", command=select_logo).pack(pady=(2, 10))

# 3. 選擇儲存資料夾
tk.Label(window, text="3. 選擇「處理後儲存」的資料夾：", font=("Arial", 10)).pack(pady=(5, 2))
entry_output = tk.Entry(window, width=50)
entry_output.pack()
tk.Button(window, text="📁 瀏覽...", command=select_output).pack(pady=(2, 10))

# 執行按鈕
tk.Button(window, text="🚀 開始批次處理 ", command=process_images, bg="#4CAF50", fg="black", font=("Arial", 12, "bold")).pack(pady=15)

# 狀態顯示標籤
lbl_status = tk.Label(window, text="準備就緒", fg="gray", font=("Arial", 9))
lbl_status.pack()

# 讓視窗持續運行
window.mainloop()