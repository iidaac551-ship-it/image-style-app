import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import base64

# -------------------------------
# 設定
# -------------------------------
API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
API_TOKEN = "YOUR_HUGGING_FACE_API_KEY"  # 自分のキーに置き換えてください

headers = {"Authorization": f"Bearer {API_TOKEN}"}

# -------------------------------
# サイドバー
# -------------------------------
st.sidebar.title("Fashion Studio AI")
st.sidebar.write("ステップごとに画像を生成できます")

# -------------------------------
# セッションステート
# -------------------------------
if "step" not in st.session_state:
    st.session_state.step = 1
if "source_image" not in st.session_state:
    st.session_state.source_image = None
if "target_image" not in st.session_state:
    st.session_state.target_image = None
if "current_image" not in st.session_state:
    st.session_state.current_image = None
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# ステップごと画面
# -------------------------------
def generate_image(prompt, init_image=None):
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True},
    }
    if init_image:
        buffered = BytesIO()
        init_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        payload["inputs"] = {"prompt": prompt, "init_image": img_str, "strength":0.7}
    
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        # 結果の画像を取得
        img_data = base64.b64decode(result["data"][0]["image_base64"])
        return Image.open(BytesIO(img_data))
    else:
        st.error(f"生成失敗: {response.status_code}")
        return None

st.title("🌸 Fashion Studio AI 🌸")

# ステップ1: 画像アップロード
if st.session_state.step == 1:
    st.subheader("Step 1: モデル画像をアップロード")
    uploaded = st.file_uploader("人物画像を選択", type=["png","jpg","jpeg"])
    if uploaded:
        img = Image.open(uploaded)
        st.session_state.source_image = img
        st.session_state.current_image = img
        st.session_state.step += 1

# ステップ2: 服装画像アップロード
elif st.session_state.step == 2:
    st.subheader("Step 2: 服装画像をアップロード")
    uploaded = st.file_uploader("服装画像を選択", type=["png","jpg","jpeg"])
    if uploaded:
        img = Image.open(uploaded)
        st.session_state.target_image = img
        st.session_state.step += 1

# ステップ3: 画角・ポーズ選択
elif st.session_state.step == 3:
    st.subheader("Step 3: 画角・ポーズ選択")
    angles = [f"{i}°アングル" for i in range(1,81)]
    selected_angle = st.selectbox("画角を選択", angles)
    pose_options = ["正面","斜め上","斜め下","アップ","自撮り風"]  # 必要なら拡張
    selected_pose = st.selectbox("ポーズを選択", pose_options)
    prompt_text = st.text_area("リクエスト（任意）","")
    if st.button("生成"):
        prompt = f"{selected_pose}, {selected_angle}, {prompt_text}"
        result = generate_image(prompt, init_image=st.session_state.source_image)
        if result:
            st.session_state.history.append(st.session_state.current_image)
            st.session_state.current_image = result
            st.image(result, caption="生成結果")
            if st.button("次のステップ"):
                st.session_state.step += 1

# ステップ4以降も同様に追加可能
# 髪型・髪色、表情、ブランド・季節、服の色など
