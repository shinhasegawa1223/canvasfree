import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# 画面全体に広げるためのCSS
st.markdown("""
    <style>
    /* メインカラムのmax-widthをほぼ解除する */
    .block-container {
        max-width: 100vw !important;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }
    /* canvasラッパーも全域使う */
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

uploaded_image = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])
if uploaded_image is not None:
    img = Image.open(uploaded_image)
    width, height = img.size

    # ラッパーでcanvasを囲い、原寸サイズでcanvasを作る
    st.markdown('<div class="canvas-scroll-xy">', unsafe_allow_html=True)

    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=3,
        stroke_color="red",
        background_image=img,
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode="polygon",
        point_display_radius=5,
        key="canvas",
    )

    st.markdown('</div>', unsafe_allow_html=True)

    if canvas_result.json_data is not None:
        st.write(canvas_result.json_data)
