import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt

def adjust_color_balance(gain_red, gain_green, gain_blue, bias_red, bias_green, bias_blue, image):
    # Apply color balance adjustment to the image
    adjusted_image = image.copy()
    adjusted_image[:, :, 0] = cv2.multiply(adjusted_image[:, :, 0], gain_blue)
    adjusted_image[:, :, 1] = cv2.multiply(adjusted_image[:, :, 1], gain_green)
    adjusted_image[:, :, 2] = cv2.multiply(adjusted_image[:, :, 2], gain_red)
    adjusted_image[:, :, 0] = cv2.add(adjusted_image[:, :, 0], bias_blue)
    adjusted_image[:, :, 1] = cv2.add(adjusted_image[:, :, 1], bias_green)
    adjusted_image[:, :, 2] = cv2.add(adjusted_image[:, :, 2], bias_red)

    return adjusted_image

# Create the Streamlit app
def main():
    # Set the page title
    st.set_page_config(page_title="Frame with Components")

    # Create a sidebar with an upload image button
    uploaded_file = st.sidebar.file_uploader("Upload Image", type=["png", "jpg"])

    if uploaded_file is not None:
        # Read the uploaded image using OpenCV
        file_bytes = uploaded_file.getvalue()
        image = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)

        # Resize the image using OpenCV for faster resizing
        image = cv2.resize(image, (300, 300))

        # Create sliders for color balance adjustments
        gain_red = st.sidebar.slider("Red Gain", 0.0, 5.0, 1.0, step=0.1)
        gain_green = st.sidebar.slider("Green Gain", 0.0, 5.0, 1.0, step=0.1)
        gain_blue = st.sidebar.slider("Blue Gain", 0.0, 5.0, 1.0, step=0.1)
        bias_red = st.sidebar.slider("Red Bias", 0, 500, 0)
        bias_green = st.sidebar.slider("Green Bias", 0, 500, 0)
        bias_blue = st.sidebar.slider("Blue Bias", 0, 500, 0)

        # Adjust color balance based on slider values
        adjusted_image = adjust_color_balance(gain_red, gain_green, gain_blue, bias_red, bias_green, bias_blue, image)

        # Display the adjusted image and plot
        col1, col2 = st.columns(2)

        with col1:
            # Display the adjusted image using OpenCV's imshow
            st.image(adjusted_image, channels="BGR")

        with col2:
            # Create a plot
            fig, ax = plt.subplots()
            x = [1, 2, 3, 4, 5]
            y = [2 * gain_blue, 4 * gain_green, 6 * gain_red, 8 * bias_blue, 10 * bias_green]
            ax.plot(x, y)
            st.pyplot(fig)


if __name__ == "__main__":
    main()
