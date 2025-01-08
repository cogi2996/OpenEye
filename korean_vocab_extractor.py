import cv2
import numpy as np
from PIL import Image
import pytesseract
import os
import re

class KoreanVocabExtractor:
    def __init__(self):
        # Specify path to Tesseract executable
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    def cleanup_text(self, text):
        # Remove all whitespace first
        text = ''.join(text.split())
        
        # Remove any non-Hangul characters
        hangul_text = ''
        for char in text:
            # Check if character is Hangul (Unicode range for Hangul: 0xAC00-0xD7A3)
            if '\uac00' <= char <= '\ud7a3' or char == ' ':
                hangul_text += char
        
        # Remove any remaining whitespace
        hangul_text = hangul_text.strip()
        
        return hangul_text

    def preprocess_image(self, image):
        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to get a binary image (black and white)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

        return thresh

    def extract_red_boxes(self, image_path):
        if not os.path.exists(image_path):
            print(f"Error: Image file not found at {image_path}")
            return []

        # Read image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not read image at {image_path}")
            return []

        # Preprocess image to enhance text visibility (binary image)
        processed_image = self.preprocess_image(image)

        # Convert to HSV to find red areas (red border for the text)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = mask1 + mask2

        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        extracted_texts = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            if w < 20 or h < 20:  # Filter small contours
                continue

            # Get the region inside the red rectangle (ROI)
            roi = image[y:y+h, x:x+w]
            roi_pil = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))

            # Apply OCR with custom config for better Korean text recognition
            custom_config = r'--oem 3 --psm 6 -l kor'
            text = pytesseract.image_to_string(roi_pil, config=custom_config)
            cleaned_text = self.cleanup_text(text)

            if cleaned_text:
                extracted_texts.append(cleaned_text)

            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imwrite('detected_boxes.jpg', image)

        return extracted_texts

    def save_to_file(self, extracted_words, file_name="extracted_words.txt"):
        # Save the extracted words to a text file
        with open(file_name, 'w', encoding='utf-8') as file:
            for word in extracted_words:
                file.write(word + "\n")
        print(f"Extracted words have been saved to {file_name}")


def main():
    extractor = KoreanVocabExtractor()
    image_path = r"D:\OpenEye\input_image.jpg"  # Thay đổi đường dẫn ảnh tại đây

    print(f"\nProcessing image: {image_path}")
    
    # Extract text from red boxes
    extracted_words = extractor.extract_red_boxes(image_path)
    
    if extracted_words:
        print("\nExtracted words:")
        for i, word in enumerate(extracted_words, 1):
            print(f"{i}. {word}")
        
        # Save extracted words to file
        extractor.save_to_file(extracted_words)
        print("\nVisualization saved as 'detected_boxes.jpg'")
    else:
        print("\nNo words were extracted. Please check if:")
        print("1. The image file exists and is readable")
        print("2. There are red boxes in the image")
        print("3. The red boxes contain Korean text")


if __name__ == "__main__":
    main()
