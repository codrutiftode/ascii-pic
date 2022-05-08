import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import math

alphabet = "~/#@0$!&*"

def main():
    image_path = sys.argv[1]
    alphabet_path = "./alphabet/alphabet.png"
    asciify(image_path, alphabet_path)
    
def random_char():
    """ Returns a random ASCII draw char """
    return alphabet[math.floor(np.random.rand() * len(alphabet))]

def asciify_legacy(image_path):
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

        for y in range(0, image_height, dy):
            for x in range(0, image_width, dx):
                tile = np_image[y:y+dy,x:x+dx,:]
                average_rgb = np.mean(tile, axis=(0, 1))
                color = np.asarray(np.round(average_rgb), dtype="int")
                text_bg_color = color // 3

                draw_context.rectangle((x, y, x+dx, y+dy), fill=tuple(text_bg_color))
                draw_context.text((x, y), random_char(), font=font, fill=tuple(color))

        image_out.show()


def asciify(image_path, alphabet_path):
    """ Takes an image path and draws it with ASCII characters """
    background_color = (255, 255, 255)

    with Image.open(alphabet_path) as image_alphabet:
        with Image.open(image_path) as image_in:
            np_image = np.array(image_in)
            image_width, image_height = image_in.size
            image_out = Image.new("RGB", image_in.size, background_color)
            draw_context = ImageDraw.Draw(image_out)
            
            font_size = 25
            font = ImageFont.truetype("./fonts/Courier.ttf", font_size)
            dx, dy = font.getsize("#")

            for y in range(0, image_height, dy):
                for x in range(0, image_width, dx):
                    tile = np_image[y:y+dy,x:x+dx,:]
                    average_rgb = np.mean(tile, axis=(0, 1))
                    color = np.asarray(np.round(average_rgb), dtype="int")
                    
                    draw_context.rectangle((x, y, x+dx, y+dy), fill=tuple(color))
                    # draw_context.text((x, y), random_char(), font=font, fill=tuple(color))

            # Use alphabet to create luminance mask
            np_alphabet = np.array(image_alphabet.convert("L"))
            print(np_alphabet.shape, dx)
            split_alphabet = np.array(np.split(np_alphabet, np_alphabet.shape[1] // dx, axis=1))
            countx = image_width // dx
            county = image_height // dy
            indices_mat = np.floor(np.random.rand(county, countx) * len(alphabet))
            print (split_alphabet.shape, indices_mat.shape)
            L_alphabet_blocks = split_alphabet[np.array(indices_mat, dtype="int")]
            L_alphabet = np.block([[col for col in row] for row in L_alphabet_blocks])
            print(L_alphabet.shape)

            # Add characters
            hsv_image_out = np.array(image_out.convert("HSV"))
            # print(hsv_image_out[:,:,2].shape)
            hsv_image_out[0:1064,:,2] = L_alphabet
            final_image = Image.fromarray(hsv_image_out, mode="HSV")
            final_image.convert("RGB").show()

    

if __name__ == "__main__":
    main()