# -*- coding: utf-8 -*-
import os

from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *
# import cv2

input_video_file = r'E:\DownloadsFromChrome\【合集】赵本山，宋丹丹合作小品系列_P5_2008 央视春节联欢晚会 小品 《火炬手》.flv'
out_video = r'out_baiyunheitu.mp4'

video = VideoFileClip(input_video_file)

# 截取视频
clip1 = video.subclip(0, 376)
# # clip2 = video.subclip(0, 11)
# # clip3 = video.subclip(150, 166)
# # clip4 = video.subclip(276, 285)
# # clip5 = video.subclip(286, 296)
final_clip = concatenate_videoclips([clip1])
final_clip.write_videofile(out_video)


# 获取视频的音频
audio = clip1.audio
audio.write_audiofile('baiyunheitu.mp3')
