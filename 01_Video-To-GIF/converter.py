from moviepy import VideoFileClip

def full(video, output):
    VideoFileClip(video).write_gif(output)

def first_ten_seconds(video, output):
    VideoFileClip(video).subclipped(0, 10).write_gif(output)

def resize(video, output):
    VideoFileClip(video).resized(width=480).write_gif(output)

def low_fps(video, output):
    VideoFileClip(video).write_gif(output, fps=10)