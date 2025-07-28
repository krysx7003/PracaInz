from OCR import Ocr, Ocr_name

image_name = "page1.jpg"

ocrs = {
        Ocr(Ocr_name.TESSERACT),
        Ocr(Ocr_name.EASY),
        Ocr(Ocr_name.DOCTR)
}

for ocr in ocrs:
    ocr.recognize_image(image_name)
    ocr.get_text()

