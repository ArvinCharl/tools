#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os
import traceback

from caj2pdf.cajparser import CAJParser

cajs_path = 'Downloads'
for caj in os.listdir(cajs_path):
    caj_path = os.path.join(cajs_path, caj)
    pdf_path = caj_path.replace(".caj", ".pdf")
    try:
        print(f'处理{caj}中...')
        do_caj = CAJParser(caj_path)
        do_caj.convert(pdf_path)
        print(f'处理{caj}完毕.', '\n')
    except:
        traceback.print_exc()
        print(f'处理{caj}失败...', '\n')

