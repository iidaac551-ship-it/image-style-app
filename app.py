import streamlit as st
from PIL import Image
import base64
import io

st.set_page_config(page_title="Fashion Studio", layout="centered")

st.title("🎨 Fashion Studio")

# --- ステップ状態管理 ---
if 'step' not in st.session_state:
    st.session_state.step = 2  # 画面2から開始
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 画像アップロード ---
source_image = st.file_uploader("モデル写真をアップロード", type=['png', 'jpg', 'jpeg'], key='source')
target_image = st.file_uploader("服装写真をアップロード", type=['png', 'jpg', 'jpeg'], key='target')

def pil_to_bytes(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

def save_history(img):
    st.session_state.history.append(img)

# --- プレビュー ---
if source_image:
    source_pil = Image.open(source_image)
    st.image(source_pil, caption="モデル画像", use_column_width=True)

if target_image:
    target_pil = Image.open(target_image)
    st.image(target_pil, caption="服装画像", use_column_width=True)

# --- ステップ 3: 画角・ポーズ ---
if st.session_state.step == 3:
    st.subheader("画角・ポーズ選択")
    pose_options = [f"ポーズ{i+1}" for i in range(80)]  # 80パターン
    selected_pose = st.selectbox("ポーズを選択", pose_options)
    if st.button("次へ"):
        st.session_state.step += 1

# --- ステップ 4: 髪型・髪色 ---
if st.session_state.step == 4:
    st.subheader("髪型・髪色")
    hair_options = [f"髪型{i+1}" for i in range(50)]  # 50パターン
    hair_color_options = ["黒", "茶", "金", "赤", "青", "紫", "ピンク"]
    selected_hair = st.selectbox("髪型を選択", hair_options)
    selected_color = st.selectbox("髪色を選択", hair_color_options)
    if st.button("次へ"):
        st.session_state.step += 1

# --- ステップ 5: 表情 ---
if st.session_state.step == 5:
    st.subheader("表情")
    expression_options = ["自然体", "笑顔", "微笑み", "クール", "自信", "アンニュイ"]
    selected_expression = st.selectbox("表情を選択", expression_options)
    if st.button("次へ"):
        st.session_state.step += 1

# --- ステップ 6: ブランド・季節 ---
if st.session_state.step == 6:
    st.subheader("ブランド・季節")
    brand_options = [f"ブランド{i+1}" for i in range(100)]
    selected_brand = st.selectbox("ブランドを選択", brand_options)
    season_options = ["春", "夏", "秋", "冬"]
    selected_season = st.selectbox("季節を選択", season_options)
    if st.button("次へ"):
        st.session_state.step += 1

# --- ステップ 7: 服の色・デザイン ---
if st.session_state.step == 7:
    st.subheader("服の色・デザイン")
    clothing_colors = ["赤", "青", "黒", "白", "ピンク", "黄色", "緑", "オリジナル"]
    selected_clothing = st.selectbox("服の色を選択", clothing_colors)
    if st.button("生成する"):
        st.success("ここでAI生成処理を呼び出します。")

# --- Magic Request（自由入力） ---
st.text_area("Magic Request（自由リクエスト）", placeholder="例：背景を明るく、顔はそのまま...")

# --- 戻る機能 ---
if st.session_state.step > 2:
    if st.button("一つ戻る"):
        st.session_state.step -= 1
        if st.session_state.history:
            st.session_state.history.pop()


