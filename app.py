import streamlit as st
import pandas as pd
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# ─── CSS：画面全体＆スクロール可能なキャンバス領域 ─────────────────────────
st.markdown("""
    <style>
    .block-container {
        max-width: 100vw !important;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }
    .canvas-scroll-xy {
        overflow-x: auto;
        overflow-y: auto;
        border: 1px solid #888;
        background: #eee;
        margin-bottom: 1rem;
        width: fit-content;
        height: fit-content;
        max-width: 100vw;
        max-height: 90vh;
    }
    </style>
""", unsafe_allow_html=True)

# ─── モード選択 ───────────────────────────────────────────────────────────
mode = st.radio("モードを選択", ("ポリゴンを描く", "ポリゴンを編集"), index=0)
drawing_mode = "polygon" if mode == "ポリゴンを描く" else "transform"

# ─── 画像アップロード ───────────────────────────────────────────────────────
uploaded_image = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])
if not uploaded_image:
    st.info("画像をアップロードしてください。上部の“Browse files”をクリックしてください。")
    st.stop()

img = Image.open(uploaded_image)
width, height = img.size

# ─── 最初のキャンバス描画 ───────────────────────────────────────────────────
st.markdown('<div class="canvas-scroll-xy">', unsafe_allow_html=True)
canvas_initial = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # 頂点内塗り色
    stroke_width=3,
    stroke_color="red",
    background_image=img,
    update_streamlit=True,
    height=height,
    width=width,
    drawing_mode=drawing_mode,
    point_display_radius=5,
    key="canvas_initial",
)
st.markdown('</div>', unsafe_allow_html=True)

# ─── JSON データ表示 & 頂点編集 ───────────────────────────────────────────────
if canvas_initial.json_data:
    st.subheader("キャンバス JSON データ")
    st.json(canvas_initial.json_data)

    # ポリゴンオブジェクトを抽出
    objs = canvas_initial.json_data.get("objects", [])
    polygon_obj = next((o for o in objs if o.get("type") == "polygon"), None)

    if polygon_obj:
        st.subheader("ポリゴンの頂点編集")
        df = pd.DataFrame(polygon_obj["points"])
        edited = st.experimental_data_editor(
            df,
            num_rows="fixed",
            columns=[
                {"field": "x", "headerName": "X 座標", "type": "numeric"},
                {"field": "y", "headerName": "Y 座標", "type": "numeric"}
            ],
            key="vertex_editor"
        )
        # 編集結果を反映
        polygon_obj["points"] = edited.to_dict("records")

        # 再描画
        st.subheader("編集後の再描画")
        st.markdown('<div class="canvas-scroll-xy">', unsafe_allow_html=True)
        st_canvas(
            initial_drawing={"objects": objs},
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=3,
            stroke_color="red",
            background_image=img,
            update_streamlit=True,
            height=height,
            width=width,
            drawing_mode="transform",
            point_display_radius=5,
            key="canvas_edited",
        )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("キャンバス上にポリゴンオブジェクトが見つかりません。描画モードで多角形を描いてください。")
