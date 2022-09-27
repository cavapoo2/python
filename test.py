#import ffmpeg
import os
import sys
from PIL import Image,ImageDraw,ImageFont


'''
Another way of creating images using ffmpeg
(
    ffmpeg
    .input('*.jpeg', pattern_type='glob', framerate=24)
    .output('movie.mp4')
    .run()
)
'''
def create_images(name,number):
    fnt = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf",
                             36, encoding="unic")
    for i in range(int(number)):
        img = Image.new('RGB',(1920,1080),color='black')
        d = ImageDraw.Draw(img)
        d.text((960,540), str(i),font=fnt,fill=(255,255,0))
        img.save(name + str(i) + ".jpg", "JPEG", quality=80, optimize=True, progressive=True)



def create_video_from_images(name, duration_in_secs):
    create_images(name,duration_in_secs)
    ffmpeg_command = ("ffmpeg -f image2 -r 1/1 -i " + name + "%01d.jpg -vcodec mpeg4 -y out_" + str(duration_in_secs) + ".mp4")
    os.system(ffmpeg_command)
    rm_files_command = "rm " + name + "*.jpg"

    os.system(rm_files_command)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("need to supply base name, and duration of video in seconds, e.g vid 10")
        sys.exit(0)
    if sys.argv[2].lower() == "range60":
        for i in range(1,61):
            create_video_from_images(sys.argv[1], i)
    else:
        create_video_from_images(sys.argv[1], sys.argv[2])

