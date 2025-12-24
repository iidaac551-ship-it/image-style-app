import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="Fashion Image Studio", layout="wide")

# --------------------
# 初期化
# --------------------
if "step" not in st.session_state:
    st.session_state.step = 1
if "history" not in st.session_state:
    st.session_state.history = []
if "image" not in st.session_state:
    st.session_state.image = None

# --------------------
# ユーティリティ
# --------------------
def save_history():
    if st.session_state.image:
        st.session_state.history.append(st.session_state.image.copy())

def undo():
    if st.session_state.history:
        st.session_state.image = st.session_state.history.pop()

# --------------------
# UI
# --------------------
st.title("🧥 Fashion Image Studio（簡易版）")

col_main, col_ctrl = st.columns([3, 2])

with col_main:
    st.subheader("🖼 プレビュー")

    if st.session_state.image:
        st.image(st.session_state.image, use_column_width=True)
    else:
        st.info("画像をアップロードしてください")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("⬅ 画像を1つ戻す"):
            undo()
    with col_b:
        if st.button("⬅ ステップを戻す"):
            if st.session_state.step > 1:
                st.session_state.step -= 1

with col_ctrl:
    st.subheader(f"STEP {st.session_state.step}")

    # --------------------
    # STEP 1：画像アップロード
    # --------------------
    if st.session_state.step == 1:
        img1 = st.file_uploader("① モデル画像（顔を維持・服は消去想定）", type=["png", "jpg", "jpeg"])
        img2 = st.file_uploader("② 服装画像（服のみ使用）", type=["png", "jpg", "jpeg"])

        if img1:
            image = Image.open(img1).convert("RGB")
            st.session_state.image = image
            save_history()

        if st.button("次へ ➡"):
            st.session_state.step = 2

    # --------------------
    # STEP 2：ポーズ・画角
    # --------------------
    if st.session_state.step == 2:
        pose = st.selectbox(
            "ポーズ・画角",
            [
                "正面", "自撮り風", "上から", "下から", "アップ",
                "斜め45度", "真横", "振り向き",
                "バストアップ", "ウエストアップ", "全身"
            ]
        )
        free_pose = st.text_area("自由入力（ポーズ・画角）")

        if st.button("次へ ➡"):
            save_history()
            st.session_state.step = 3

    # --------------------
    # STEP 3：髪型・髪色
    # --------------------
    if st.session_state.step == 3:
        hair = st.selectbox(
            "髪型",
            [
                "そのまま", "ショート", "ボブ", "ロング",
                "ウェーブ", "ポニーテール", "お団子",
                "ハーフアップ", "前髪あり", "前髪なし"
            ]
        )
        hair_color = st.selectbox(
            "髪色",
            ["そのまま", "ブラック", "ブラウン", "ベージュ", "アッシュ", "ピンク", "シルバー"]
        )
        free_hair = st.text_area("自由入力（髪型・髪色）")

        if st.button("次へ ➡"):
            save_history()
            st.session_state.step = 4

    # --------------------
    # STEP 4：ブランド・季節
    # --------------------
    if st.session_state.step == 4:
        season = st.selectbox("季節", ["春", "夏", "秋", "冬"])

        brand = st.selectbox(
            "ブランド（女性向け）",
            [
                "CHANEL", "DIOR", "GUCCI", "PRADA", "CELINE",
                "LOEWE", "SAINT LAURENT", "FENDI", "MIU MIU",
                "SNIDEL", "FRAY I.D", "Mila Owen", "ZARA",
                "Ameri", "CLANE", "Mame Kurogouchi"
            ]
        )

        free_brand = st.text_area("自由入力（ブランド・世界観）")

        if st.button("次へ ➡"):
            save_history()
            st.session_state.step = 5

    # --------------------
    # STEP 5：最終指示
    # --------------------
    if st.session_state.step == 5:
        final_request = st.text_area(
            "最終リクエスト（顔は維持・服のみ反映など自由に）",
            height=120
        )

        st.success("この画面構成で Gemini / API に渡す想定です")

        if st.button("完了 🎉"):
            st.balloons()

st.caption("※ このUIは『選択 → 自由入力』を前提にしたベース構成です")
