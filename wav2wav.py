#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os
from pathlib import Path

wavs_path = "tes_data"
out_wavs_path = 'out_tes_data'
wav_list = os.listdir(wavs_path)

for wav in wav_list:
    if wav.endswith('wav'):
        input_wav_path = os.path.join(wavs_path, wav)
        print(f'正在处理: {input_wav_path}')
        out_wav = f'out_{os.path.basename(input_wav_path)}'
        out_wav_path = os.path.join(out_wavs_path, wav)
        wav_cmd = f'sox {input_wav_path} -r 16000 -c 1 {out_wav_path}'
        x = os.popen(wav_cmd)
        print(x)

out_cmd = f'file {out_wavs_path}/*'
y = os.popen(out_cmd).read()
print(y)
