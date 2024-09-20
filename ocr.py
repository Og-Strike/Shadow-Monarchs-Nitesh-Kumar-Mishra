import cv2
import pytesseract
from PIL import Image
import sys
import argparse

def extract_text(args):
    try:
        image = cv2.imread(args.image)
        TEXT_THRESHOLD = 5
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, TEXT_THRESHOLD, 255, cv2.THRESH_BINARY_INV)
        
        mask = cv2.bitwise_not(thresh)
        occlusion_mask = cv2.dilate(mask, None, iterations=2)
        occluded_image = cv2.bitwise_and(gray, gray, mask=occlusion_mask)
        text = pytesseract.image_to_string(Image.fromarray(occluded_image))
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Full Pipeline')
    parser.add_argument('--image', type=str, help='Path to the input image')
    parser.add_argument('--name_image',type=str,help='Name of file')
    args = parser.parse_args()
    result = extract_text(args)
    if result == "":
        print("nothing")
    else:
        print(result)
