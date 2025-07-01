# from IPython.display import display
# from transformers import TrOCRProcessor, VisionEncoderDecoderModel
#
# processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
# model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
#
# def show_image(pathStr):
#   img = Image.open(pathStr).convert("RGB")
#   display(img)
#   return img
#
# def ocr_image(src_img):
#   pixel_values = processor(images=src_img, return_tensors="pt").pixel_values
#   generated_ids = model.generate(pixel_values)
#   return processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
#   
#
# image = show_image("/home/napnap/Downloads/page1-1.png")
# print(ocr_image(image))
import pytesseract
from PIL import Image

print(pytesseract.image_to_string(Image.open("/home/napnap/Downloads/page1-1.png")))
