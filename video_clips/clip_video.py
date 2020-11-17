# -*- coding: utf-8 -*-
import os

from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
# import cv2

input_video_file = 'FIRE1.mp4'
out_video = 'out_FIRE1.mp4'

clip1 = VideoFileClip(input_video_file).subclip(14, 60)
# clip2 = VideoFileClip(input_video_file).subclip(0, 11)
# clip3 = VideoFileClip(input_video_file).subclip(150, 166)
# clip4 = VideoFileClip(input_video_file).subclip(276, 285)
# clip5 = VideoFileClip(input_video_file).subclip(286, 296)

final_clip = concatenate_videoclips([clip1])
final_clip.write_videofile(out_video)
