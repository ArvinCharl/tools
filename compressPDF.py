#!/user/bin/env python3
# -*- coding: utf-8 -*-
import fitz
import os
from PIL import Image
from glob import glob
from time import time


class PdfEdit:
    def __init__(self, f_type='jpg'):
        self.f_type = f_type
        self.f_path = os.path.join(os.path.abspath('.'), f'PdfEdit{int(time())}')
        if not os.path.exists(self.f_path):
            os.mkdir(self.f_path)

    def pdf2img(self, f_path=None, f_file=None, pn=[0, 0], zoom=[2.0, 2.0]):
        """ 把pdf分割成图片
        f_path: pdf文件路径
        f_file: pdf文件流
        pn: 列表或元组，如果为元组，则为需要转换压缩的元组内页码， 如果是列表，则为需要转换的pdf起止页码，默认为全部
        zoom: 每个尺寸的缩放系数， 默认为分辨率的2倍
        """
        if f_path and f_path.endswith('pdf'):
            doc = fitz.open(f_path)
        elif f_file:
            doc = fitz.open('pdf', stream=f_file)
        else:
            print('无效的文件')
            return 0
        if isinstance(pn, tuple):
            p_list = pn
        elif isinstance(pn, list):
            if not pn[1]:
                pn[1] = doc.pageCount
            p_list = range(*pn)
        else:
            print('页码类型应该为列表或元组')
            return 0
        for pg in p_list:
            page = doc[pg]
            trans = fitz.Matrix(*zoom).preRotate(0)
            p_img = page.getPixmap(matrix=trans, alpha=False)
            p_img.writeImage(f'{self.f_path}/{pg + 1}.{self.f_type}')
        doc.close()
        return 1

    def img2pdf(self, f_size=150, quality=75):
        """把图片转换成pdf
        f_size: int, 压缩目标，KB
        quality: int, 初始压缩比率
        """
        doc = fitz.open()
        for img in glob(f'{self.f_path}//*.{self.f_type}'):
            for _ in range(3):
                if os.path.getsize(img) / 1024 <= f_size:
                    break
                im = Image.open(img).save(img, quality=quality)
            imgpdf = fitz.open('pdf', fitz.open(img).convertToPDF())
            doc.insertPDF(imgpdf)  # 将当前页插入pdf文档
        path = os.path.join(self.f_path, f'{int(time())}.pdf')
        print(path)
        doc.save(path)  # 保存pdf文件
        doc.close()
        return path


if __name__ == '__main__':
    pe = PdfEdit()
    pe.pdf2img(r'D:\Desktop\20201221电信-海科-技术开发合同（媒体画像智能分析系统）.pdf')
    pe.img2pdf()
