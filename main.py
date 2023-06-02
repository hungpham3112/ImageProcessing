from PIL import Image
from lib import count, coordinates, equalize_intensity, mean_filter, median_filter, gaussian_smoothing
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def adjust_color_balance(gain_red, gain_green, gain_blue, bias_red, bias_green, bias_blue, image):
    # Apply color balance adjustment to the image
    adjusted_image = image.astype(float)

    adjusted_image[..., 0] = gain_red * adjusted_image[..., 0] + bias_red
    adjusted_image[..., 1] = gain_green * adjusted_image[..., 1] + bias_blue
    adjusted_image[..., 2] = gain_blue * adjusted_image[..., 2] + bias_green

    return np.clip(adjusted_image, 0, 255).astype(np.uint8)

def main(): # Set the page title
    st.set_page_config(page_title="Frame with Components")

    # Create a sidebar with an upload image button
    uploaded_file = st.sidebar.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Read the uploaded image using OpenCV
        image = np.array(Image.open(uploaded_file))

        # Resize the image using OpenCV for faster resizing
        #  image = np.array(image.resize((300, 300)))

        # Create sliders for color balance adjustments
        gain_red = st.sidebar.slider("Red Gain", 0.0, 5.0, 1.0, step=0.1)
        gain_green = st.sidebar.slider("Green Gain", 0.0, 5.0, 1.0, step=0.1)
        gain_blue = st.sidebar.slider("Blue Gain", 0.0, 5.0, 1.0, step=0.1)
        bias_red = st.sidebar.slider("Red Bias", 0, 255, 0)
        bias_green = st.sidebar.slider("Green Bias", 0, 255, 0)
        bias_blue = st.sidebar.slider("Blue Bias", 0, 255, 0)

        # Adjust color balance based on slider values
        adjusted_image = adjust_color_balance(gain_red, gain_green, gain_blue, bias_red, bias_green, bias_blue, image)
        original_image = adjusted_image

        fig, ax = plt.subplots()
        # Create 2 frame as 2 columns
        col1, col2 = st.columns(2)
        with col2:
            if st.button("Equalization"):
                equalized_image = equalize_intensity(adjusted_image)
                for color, index in zip(("red", "green", "blue"), range(0, 3)):        
                    vec_x, vec_y = coordinates(count(equalized_image[:, :, index]))
                    ax.plot(vec_x, vec_y,color=color)
                adjusted_image = equalized_image
            if st.button("Median filter"):
                filtered_image = median_filter(adjusted_image, 3)
                adjusted_image = filtered_image


            if st.button("Mean filter"):
                filtered_image = mean_filter(adjusted_image, 3)
                adjusted_image = filtered_image

            if st.button("Gaussian Blur"):
                filtered_image = gaussian_smoothing(adjusted_image, 3, 1.5)
                adjusted_image = filtered_image
            if st.button("Reset"):
                adjusted_image = original_image
        with col:
            st.image(adjusted_image, channels="RGB")
            for color, index in zip(("red", "green", "blue"), range(0, 3)):        
                vec_x, vec_y = coordinates(count(adjusted_image[:, :, index]))
                ax.plot(vec_x, vec_y,color=color)
            st.pyplot(fig)

if __name__ == "__main__":
    main()
