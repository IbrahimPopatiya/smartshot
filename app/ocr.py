import pytesseract
from PIL import Image
import os
from PIL import Image, ImageOps, ImageFilter

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def upscale_if_needed(image: Image.Image) -> Image.Image:
    width, height = image.size
    if width < 1000 or height < 300:
        image = image.resize(
            (width * 2, height * 2),
            Image.BICUBIC
        )
    return image

def preprocess_image(image: Image.Image) -> Image.Image:
    # 1. Convert to grayscale
    image = image.convert("L")

    # 2. Increase contrast aggressively
    image = ImageOps.autocontrast(image, cutoff=2)

    # 3. Apply median filter (reduces noise)
    image = image.filter(ImageFilter.MedianFilter(size=3))

    # 4. Sharpen text edges
    image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    return image

def extract_text_from_image(image_path: str) -> str:
    if not os.path.exists(image_path):
        return ""
    
    

    try:
        image = Image.open(image_path)
        image = upscale_if_needed(image)
        image = preprocess_image(image)
        custom_config = (
            "--oem 3 "          # Best OCR engine (LSTM)
            "--psm 6 "          # Block of text (best for screenshots)
            "-c preserve_interword_spaces=1"
        )
        text = pytesseract.image_to_string(image,lang="eng",config=custom_config)
        return text.strip()
    
    except Exception as e:
        print("OCR error:", e)
        return ""
