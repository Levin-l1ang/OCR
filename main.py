import fitz
from PIL import Image
import pytesseract
import os


def extract_images_from_pdf(pdf_path, output_folder):
    # 打开PDF文件
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_name = f"page_{page_num + 1}_img_{img_index + 1}.{image_ext}"
            image_path = os.path.join(output_folder, image_name)
            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)
            print(f"Saved image: {image_path}")


def ocr_image_to_text(image_path):
    # 使用Tesseract进行OCR处理
    text = pytesseract.image_to_string(Image.open(image_path))
    return text


def main():
    pdf_path = "example.pdf"  # 替换为你的PDF文件路径
    output_folder = "extracted_images"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 提取PDF中的所有图像
    extract_images_from_pdf(pdf_path, output_folder)

    # 对每个图像进行OCR处理
    for image_file in os.listdir(output_folder):
        image_path = os.path.join(output_folder, image_file)
        text = ocr_image_to_text(image_path)
        print(f"Text from {image_file}:\n{text}\n")


if __name__ == "__main__":
    main()