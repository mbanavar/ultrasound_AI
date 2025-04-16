# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 20:07:41 2025
Last edited on Tue Apr 16 21:21:00 2025
@author: Daniel Wilson & Gabe Adamson
"""
def process_uploaded_image(image, kernel, thresh, coefficient, t_lower, t_upper, bS):
    #Import Libraries
    import numpy as np
    import cv2
    import pywt
    import pywt.data

    #method definitions
    def wavelet_filtering(image,thresh):
        coeffs = pywt.dwt2(image, 'haar')
        LL, (LH, HL, HH) = coeffs
         #Threshold for coeff needs to be adjusted per image currently
        #Keeps only within threshold times maximum value for each coefficient
        filtered_LL = np.where(LL >= thresh*LL.max(), LL, 0)
        filtered_LH = np.where(LH >= thresh*LH.max(), LH, 0)
        filtered_HL = np.where(HL >= thresh*HL.max(), HL, 0)
        filtered_HH = np.where(HH >= thresh*HH.max(), HH, 0)
        filtered_coeffs = (filtered_LL, (filtered_LH, filtered_HL, filtered_HH))
        image_out = pywt.idwt2(filtered_coeffs,'haar')
        return image_out

    def resize_if_needed_cv2(img, max_width=800, max_height=800):
        height, width = img.shape[:2]

        if width > max_width or height > max_height:
            # Calculate scale factor while maintaining aspect ratio
            scale_w = max_width / width
            scale_h = max_height / height
            scale = min(scale_w, scale_h)

            new_width = int(width * scale)
            new_height = int(height * scale)

            resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
            print(f"Image resized from ({width}, {height}) to ({new_width}, {new_height})")
            return resized_img
        else:
            return img

    def gauss_blur(image, kernel, coefficient):

        gaussBlurIm = cv2.GaussianBlur(image, (kernel, kernel), coefficient)

        return gaussBlurIm


    def filter_inside_lines(edges):

        height, width = edges.shape
        filteredLines = np.empty((height, width), dtype=np.uint8)

        for i in range(0, len(edges)-1):
            for j in range(0, len(edges[0])-2):
                y1 = -((j**2)/512)+(153*j/64)-(21361/32)
                y2 = -((9040*(j**2))/13737241)+(11114837*j/13737241)+(5210544027/13737241)
                x1 = -(321*i/460)+(106207/230)
                x2 = (317*i/466)+(177657/233)
                if (i > y1) and (i < y2) and (j > x1) and (j < x2):
                    filteredLines[i][j] = edges[i][j]
                else:
                    filteredLines[i][j] = 0

        return filteredLines


    def canny_detection(image, t_lower, t_upper):

        edges = cv2.Canny(image, t_lower, t_upper)

        return edges


    def polarize(img):
        height, width = img.shape
        polarizedImage = np.empty((height, width), dtype=np.uint8)


        for i in range(0, len(img)-1):
            for j in range(0, len(img[i])-1):
                if img[i][j]*255 >= 255:
                    polarizedImage[i][j] = 255
                else:
                    polarizedImage[i][j] = 0

        return polarizedImage


    def draw_lines(original_image, edges, bS):
        # Ensure the original image is in color (RGB)
        color_image = cv2.cvtColor(original_image, cv2.COLOR_GRAY2RGB)

        height, width, _ = edges.shape  # Adjust for 3D array (height, width, channels)

        for i in range(1, height - 1):
            for j in range(1, width - 1):
                # Check if any channel in the edge pixel is non-zero (indicating an edge)
                if np.any(edges[i, j] != 0):  # Use np.any() to check all channels
                    # Draw a red line on the original image where the edge is detected
                    # Use a small box around the edge pixel to bolden the line (with bS as bold strength)
                    for dx in range(-bS, bS + 1):
                        for dy in range(-bS, bS + 1):
                            xi = min(max(i + dx, 0), height - 1)
                            yi = min(max(j + dy, 0), width - 1)
                            color_image[xi, yi] = [0, 0, 255]  # Red color

        return color_image

    originalImage = image
    resizedOriginalImage = resize_if_needed_cv2(originalImage)
    gaussBlurIm = gauss_blur(resizedOriginalImage, kernel, coefficient)          # First Blur
    waveletImage = wavelet_filtering(gaussBlurIm, thresh)                        # Wavelet Filtering
    waveGaussImage = gauss_blur(waveletImage, kernel, coefficient)               # Blur after wavelet filtering
    polarizedImage = polarize(waveGaussImage)                                    # Polarize pixels to white or black
    edges = canny_detection(polarizedImage, t_lower, t_upper)                    # Canny Edge Detection
    edges_resized = cv2.resize(edges, (resizedOriginalImage.shape[1], resizedOriginalImage.shape[0]))
    filteredLines = filter_inside_lines(edges_resized)                           # Sort out lines insides of boundaries
    tempColorLines = cv2.cvtColor(filteredLines, cv2.COLOR_GRAY2RGB)             # Bolden edge detection lines and turn them red
    finalImage = draw_lines(resizedOriginalImage, tempColorLines, bS)

    return finalImage
