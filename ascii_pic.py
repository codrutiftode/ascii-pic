import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageCms
import matplotlib.pyplot as plt
import math
import cv2

alphabet = "~/#@0$!&*"


def main():
    print("Rendering...")
    image_path = sys.argv[1]
    alphabet_path = "./alphabet/alphabet.png"
    asciify(image_path, alphabet_path)
    print("Finished render.")


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
                tile = np_image[y:y+dy, x:x+dx, :]
                average_rgb = np.mean(tile, axis=(0, 1))
                color = np.asarray(np.round(average_rgb), dtype="int")
                text_bg_color = color // 3

                draw_context.rectangle(
                    (x, y, x+dx, y+dy), fill=tuple(text_bg_color))
                draw_context.text((x, y), random_char(),
                                  font=font, fill=tuple(color))

        image_out.show()


def asciify(image_path, alphabet_path):
    """ Takes an image path and draws it with ASCII characters """
    background_color = (255, 255, 255)

    with Image.open(alphabet_path) as image_alphabet:
        with Image.open(image_path) as image_in:
            np_image = np.array(image_in)
            image_width, image_height = image_in.size

            # Create output image
            image_out = Image.new("RGB", image_in.size, background_color)
            draw_context = ImageDraw.Draw(image_out)

            # Init font
            font_size = 25
            font = ImageFont.truetype("./fonts/Courier.ttf", font_size)
            dx, dy = font.getsize("#")

            # Draw pixelated output background
            for y in range(0, image_height, dy):
                for x in range(0, image_width, dx):
                    tile = np_image[y:y+dy, x:x+dx, :]
                    average_rgb = np.mean(tile, axis=(0, 1))
                    color = np.asarray(np.round(average_rgb), dtype="int")

                    draw_context.rectangle(
                        (x, y, x+dx, y+dy), fill=tuple(color))

            # Use alphabet to create luminance mask
            np_alphabet = np.array(image_alphabet.convert("L"))
            split_alphabet = np.array(
                np.split(np_alphabet, np_alphabet.shape[1] // dx, axis=1))
            countx = image_width // dx + 1
            county = image_height // dy + 1
            indices_mat = np.floor(np.random.rand(
                county, countx) * len(alphabet))
            L_alphabet_blocks = split_alphabet[np.array(
                indices_mat, dtype="int")]
            L_alphabet = np.block([[col for col in row]
                                  for row in L_alphabet_blocks])

            # Add characters by weight-averaging the luminance channel with the luminance mask
            hls_image_out = cv2.cvtColor(
                np.array(image_out), cv2.COLOR_RGB2LAB)
            weight_original = 1
            weight_mask = 2
            hls_image_out[:, :, 0] = (hls_image_out[:, :, 0] * weight_original +
                                      L_alphabet[0:image_height, 0:image_width] / 255 * 100 * weight_mask) // (weight_original + weight_mask)

            # Create final image
            final_image = Image.fromarray(cv2.cvtColor(
                hls_image_out, cv2.COLOR_LAB2RGB), mode="RGB")
            final_image.show()


if __name__ == "__main__":
    main()
