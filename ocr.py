import cv2
import pytesseract
from PIL import Image
import argparse
import re
import subprocess
import universal

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
    
def extract_invoice_data(text):
    top_headings = text.splitlines()[:5] 
    top_headings = [line.strip() for line in top_headings if line.strip()]  

    company_name = top_headings[0] if top_headings else "Not found"  

    total_amount = re.search(r'(?:grand\s*total|total\s*amount|amount\s*due)[^\d]*(\d+[.,]?\d*)', text, re.IGNORECASE)

    tax_a = re.search(
        r'(?:total\s*gst)[^\d]*(\d+[.,]?\d*)', 
        text, 
        re.IGNORECASE
    )

    gst = re.search(
        r'(?:gst|id)[^\d]*(\d+[.,]?\d*)', 
        text, 
        re.IGNORECASE
    )
    
    date = re.search(r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b|\b(\d{4}[/-]\d{1,2}[/-]\d{1,2})\b', text)

    return {
        'company_name': company_name.strip(),
        'date': date.group(0) if date else "Not found",
        'total_amount': total_amount.group(1) if total_amount else "Not found",
        'tax_a': tax_a.group(1) if tax_a else "Not found",
        'gst': gst.group(1) if gst else "Not found"
    }
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Full Pipeline')
    parser.add_argument('--image', type=str, help='Path to the input image')
    parser.add_argument('--name_image',type=str,help='Name of file')
    args = parser.parse_args()
    result = extract_text(args)
    print(result)
    if result == "":
        print("Nothing found")
    else:
        extracted_data = extract_invoice_data(result)
        
        data_list = [
            extracted_data['company_name'],
            extracted_data['date'],
            extracted_data['total_amount'],
            extracted_data['tax_a'],
            extracted_data['gst']
        ]
        if data_list[2]=="Not Found":
            filename="a.txt"
            value=-1
            with open(filename, 'w') as file:
                file.write(str(value))
            print(f"Value '{value}' written to {filename}")
            
        else:
            filename="a.txt"
            value=data_list[2]
            with open(filename, 'w') as file:
                file.write(str(value))
            print(f"Value '{value}' written to {filename}")
        command = ["python","data.py",f"{data_list[0]}",f"{data_list[1]}",f"{data_list[2]}",f"{data_list[3]}",f"{data_list[4]}"]
        subprocess.run(command)
