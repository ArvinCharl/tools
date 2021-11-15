#!/user/bin/env python3
# -*- coding: utf-8 -*-
from pydub import AudioSegment

input_sound_file = r'out_jdft_dangkekaijiang.wav'
out_sound = r'out_out_jdft_dangkekaijiang.wav'

sound = AudioSegment.from_wav(input_sound_file)
# sound = AudioSegment.from_mp3(input_sound_file)
# sound = AudioSegment.from_ogg(input_sound_file)
# sound = AudioSegment.from_flv(input_sound_file)

# clip = sound[1 * 1000: 66 * 1000]
clip = sound[39 * 1000:287 * 1000]
clip.export(out_sound, format='wav')
