from fileinput import filename

from PDF_Loader import  *

if __name__ == '__main__':
    # read_pdf('毛泽东经济年谱 (顾龙生（中共中央党校出版社1993年）) (Z-Library).pdf')
    with open('shibie.txt', 'r') as file:
        text = file.read()
    output = './output/fenxi.json'
    jubenfx(text,output)
