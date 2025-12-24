import streamlit as st
import os
import subprocess

st.set_page_config(page_title="Pro YouTube Clipper", page_icon="🎬")
st.title("🎬 YouTube 1080p 在线剪辑器")

# --- UI 界面 ---
url = st.text_input("YouTube 视频链接", placeholder="https://www.youtube.com/watch?v=...")
c1, c2 = st.columns(2)
with c1:
    start = st.text_input("开始时间 (HH:MM:SS)", value="00:00:10")
with c2:
    end = st.text_input("结束时间 (HH:MM:SS)", value="00:00:20")

# --- 预留的 Cookie 功能 ---
st.sidebar.title("设置 (高级)")
uploaded_cookie = st.sidebar.file_uploader("上传 cookies.txt (可选)", type=["txt"])

if st.button("🚀 开始剪辑并下载"):
    if not url:
        st.error("请输入链接")
    else:
        output = "output_clip.mp4"
        if os.path.exists(output): os.remove(output)
        
        # 基础命令
        cmd = [
            'yt-dlp',
            '-f', 'bestvideo[height<=1080]+bestaudio/best',
            '--merge-output-format', 'mp4',
            '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            '--external-downloader', 'ffmpeg',
            '--external-downloader-args', f'ffmpeg_i:-ss {start} -to {end}',
        ]

        # 逻辑：如果有上传的cookie就用上传的，没有就找根目录的
        if uploaded_cookie:
            with open("temp_cookies.txt", "wb") as f:
                f.write(uploaded_cookie.getbuffer())
            cmd.extend(['--cookies', 'temp_cookies.txt'])
        elif os.path.exists("cookies.txt"):
            cmd.extend(['--cookies', 'cookies.txt'])
        
        cmd.extend([url, '-o', output])

        with st.spinner("正在处理视频... 1080p合成较慢，请稍等..."):
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if os.path.exists(output):
                st.success("✅ 剪辑完成！")
                with open(output, "rb") as f:
                    st.download_button("💾 点击下载视频", f, file_name="clip_1080p.mp4")
            else:
                st.error("❌ 处理失败。")
                st.code(result.stderr)
