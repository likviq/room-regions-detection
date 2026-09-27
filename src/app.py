import asyncio

import cv2
import numpy as np
import streamlit as st

from src.constants.image_constants import ImageConstants
from src.container import Container
from src.enums.background_removal_state import BackgroundRemovalState
from src.view_models.process_image.process_image_request import ProcessImageRequest


@st.cache_resource
def get_container():
    container = Container()
    return container


def load_uploaded_image(uploaded_file):
    image_bytes = uploaded_file.getvalue()
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image


def main():
    st.set_page_config(page_title="Floor Plan Analyzer", layout="wide")
    st.title("Floor Plan Analyzer")

    uploaded_file = st.file_uploader("Upload floor plan", type=["png", "jpg", "jpeg", "webp"])

    if uploaded_file is None:
        return

    background_removal_enabled = st.checkbox("Remove background", value=True)
    target_height = st.number_input("Target height", min_value=1, value=ImageConstants.DEFAULT_TARGET_HEIGHT)
    background_tolerance = st.number_input("Background tolerance", min_value=0, value=ImageConstants.DEFAULT_BACKGROUND_TOLERANCE)
    region_threshold = st.number_input("Region threshold", min_value=0, value=ImageConstants.DEFAULT_REGION_THRESHOLD)
    seed_offset = st.number_input("Seed offset", min_value=0, value=ImageConstants.DEFAULT_SEED_OFFSET)
    minimum_room_area = st.number_input("Minimum room area", min_value=1, value=ImageConstants.DEFAULT_MINIMUM_ROOM_AREA)
    overlay_alpha = st.slider("Overlay alpha", min_value=0.0, max_value=1.0, value=ImageConstants.DEFAULT_OVERLAY_ALPHA)

    if background_removal_enabled:
        background_removal_state = BackgroundRemovalState.ENABLED
    else:
        background_removal_state = BackgroundRemovalState.DISABLED

    image = load_uploaded_image(uploaded_file)

    if image is None:
        st.error("The uploaded file could not be decoded.")
        return

    request = ProcessImageRequest(
        image,
        None,
        target_height,
        background_removal_state,
        background_tolerance,
        region_threshold,
        seed_offset,
        minimum_room_area,
        overlay_alpha,
    )

    container = get_container()
    process_image_service = container.create_process_image_service()

    try:
        response = asyncio.run(process_image_service.process_image(request))
    except ValueError as error:
        st.error(str(error))
        return

    original_column, processed_column = st.columns(2)

    with original_column:
        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Original")

    with processed_column:
        st.image(cv2.cvtColor(response.preprocessed_image, cv2.COLOR_BGR2RGB), caption="Preprocessed")

    st.image(cv2.cvtColor(response.labeled_image, cv2.COLOR_BGR2RGB), caption="Rooms")
    st.write(f"Detected lines: {0 if response.detected_lines is None else len(response.detected_lines)}")
    st.write(f"Detected rooms: {len(response.room_labels)}")

    st.download_button(
        label="Download rooms.json",
        data=response.rooms_json,
        file_name="rooms.json",
        mime="application/json",
    )


if __name__ == "__main__":
    main()
