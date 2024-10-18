import fitz
from PIL import Image
import pytesseract
import io
from http import HTTPStatus
from dashscope import Application
import json
from tqdm import tqdm

def read_pdf(pdf_path,output_lang='chi_sim'):


    document = fitz.open(pdf_path)
    total_pages = len(document)
    # print(f"Total pages in the PDF: {total_pages}")

    txt = ''

    for page_num in tqdm(range(total_pages), desc="识别页面中：", unit="page"):
        page = document.load_page(page_num)
        image_list = page.get_images(full=True)

        if not image_list:
            print(f"No images found on page {page_num + 1}.")
            continue

        # 遍历当前页的所有图片
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = document.extract_image(xref)
            image_bytes = base_image["image"]

            # 将图片数据转换成Image对象
            image = Image.open(io.BytesIO(image_bytes))

            # 使用Tesseract进行OCR
            text = pytesseract.image_to_string(image, lang=output_lang)

            txt += text
    # read_pdf("undefine.pdf")
    with open(f"shibie.txt", "w") as text_file:
        text_file.write(txt)
    print("读取完成！")

def jubenfx(text, filename):
    response = Application.call(app_id='2cc924edb328445097a71513c734dfad',
                                prompt=text,
                                api_key='sk-eef092f5235b4c698918df87ac0a6b26', )

    if response.status_code != HTTPStatus.OK:
        print(
            'request_id=%s, code=%s, message=%s\n' % (response.request_id, response.status_code, response.message))
    else:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(response.output.text, file, ensure_ascii=False, indent=4)
        print('分析已完成！')

