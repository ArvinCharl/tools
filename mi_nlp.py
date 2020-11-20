#!/user/bin/env python3
# -*- coding: utf-8 -*-
from minlptokenizer.tokenizer import MiNLPTokenizer

tokenizer = MiNLPTokenizer(granularity='fine')  # fine：细粒度，coarse：粗粒度，默认为细粒度
print(tokenizer.cut('今天天气怎么样？'))
