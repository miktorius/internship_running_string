from PIL import Image, ImageFont, ImageDraw
import cv2
import numpy as np


def generate_image(string: str):
    # string constants
    string_font = ImageFont.truetype('../utils/couriernew.ttf', 75)
    string_color = (255, 255, 255)
    string_offset = (10, 15)
    # image constants
    image_size = (15 + 50 * len(string), 100)
    background_color = (0, 0, 0)
    # image generator
    image = Image.new(mode="RGB", size=image_size, color=background_color)
    # making image editable and adding text
    image_edit = ImageDraw.Draw(image)
    image_edit.text(string_offset, string, string_color, font=string_font)
    return image, image_size


def generate_video(string: str):
    image, image_size = generate_image(string)
    fps = 60
    total_frames = fps * 3  # for 3 second length
    # constants to cut 100x100 images out of original image
    frame_box = [0, 0, 100, 100]
    # step to generate frame
    frame_step = (image_size[0] - 100) / total_frames
    # video settings
    video_name = 'video.mp4'
    video_codec = cv2.VideoWriter_fourcc(*'mp4v')
    video_size = (100, 100)
    video = cv2.VideoWriter(video_name, video_codec, fps, video_size)  # video initialisation
    # building video out of small crops
    for _ in range(total_frames):
        frame = image.crop(tuple(frame_box))  # cropping
        frame_box[0] += frame_step
        frame_box[2] += frame_step
        opencv_frame = np.array(frame)  # formatting pillow to opencv image
        video.write(opencv_frame)  # adding single frame to a video
    video.release()
