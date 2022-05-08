import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import math

def main():
    image_path = sys.argv[1]
    asciify(image_path)
    
def random_char():
    """ Returns a random ASCII draw char """
    chars = "~/#@0$!&*"
    return chars[math.floor(np.random.rand() * len(chars))]

def asciify(image_path):
    """ Takes an image path and draws it with ASCII characters """
    background_color = (255, 255, 255)

    with Image.open(image_path) as image_in:
        np_image = np.array(image_in)
        image_width, image_height = image_in.size
        image_out = Image.new("RGB", image_in.size, background_color)
        
        font_size = 25
        font_x_factor = 3200
        font_y_factor = 1720
        font = ImageFont.truetype("./fonts/Courier.ttf", font_size)
        
        draw_context = ImageDraw.Draw(image_out)

        dx = round(image_width * font_size / font_x_factor)
        dy = round(image_height * font_size / font_y_factor)

        count = 0
        for y in range(0, image_height, dy):
            for x in range(0, image_width, dx):
                tile = np_image[y:y+dy,x:x+dx,:]
                average_rgb = np.mean(tile, axis=(0, 1))
                color = np.asarray(np.round(average_rgb), dtype="int")
                
                count += 1
                # if (np.average(color) > 100): 
                #     print(color, np.average(color))
                #     quit()
                # text_bg_color = np.where(color * 2 < 255, color * 2, 255)
                text_bg_color = color // 3
                draw_context.rectangle((x, y, x+dx, y+dy), fill=tuple(text_bg_color))
                draw_context.text((x, y), random_char(), font=font, fill=tuple(color))


        # print(countx)
        image_out.show()

    

if __name__ == "__main__":
    main()