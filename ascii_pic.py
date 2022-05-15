import sys
import numpy as np
import matplotlib.pyplot as plt
import math
import cv2
import time
import json
from render_alphabet import ALPHABET_DIR, Alphabet


def main():
    print("Rendering...")
    image_path = sys.argv[1]
    with Alphabet(ALPHABET_DIR) as alphabet:
        start = time.time()
        original_image = cv2.cvtColor(
            cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        ascii_image = asciify(original_image, alphabet)
        end = time.time()
        plt.imshow(ascii_image)
        plt.show()
    print("Finished render.")
    print("Total time: %0.3f" % (end - start))


def asciify(original_image, alphabet):
    """ Takes an image path and draws it with ASCII characters """
    # Unpack alphabet data
    dx = alphabet.meta["char_width"]
    dy = alphabet.meta["char_height"]
    alphabet_chars = alphabet.meta["chars"]

    image_height = original_image.shape[0]
    image_width = original_image.shape[1]

    # Create output image
    image_out = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    # Draw pixelated output background
    for y in range(0, image_height, dy):
        for x in range(0, image_width, dx):
            tile = original_image[y:y+dy, x:x+dx, :]
            average_rgb = np.mean(tile, axis=(0, 1))
            color = np.asarray(np.round(average_rgb), dtype="int")
            image_out[y:y+dy, x:x+dx] = color

    # Use alphabet to create luminance mask
    np_alphabet = np.array(alphabet.image.convert("L"))
    split_alphabet = np.array(
        np.split(np_alphabet, np_alphabet.shape[1] // dx, axis=1))
    countx = image_width // dx + 1
    county = image_height // dy + 1
    indices_mat = np.floor(np.random.rand(
        county, countx) * len(alphabet_chars))
    L_alphabet_blocks = split_alphabet[np.array(
        indices_mat, dtype="int")]
    L_alphabet = np.block([[col for col in row]
                           for row in L_alphabet_blocks])

    # Add characters by weight-averaging the luminance channel with the luminance mask
    hls_image_out = cv2.cvtColor(image_out, cv2.COLOR_RGB2LAB)
    weight_original = 1
    weight_mask = 2
    hls_image_out[:, :, 0] = (hls_image_out[:, :, 0] * weight_original +
                              L_alphabet[0:image_height, 0:image_width] / 255 * 100 * weight_mask) // (weight_original + weight_mask)

    # Create final image
    final_image = cv2.cvtColor(hls_image_out, cv2.COLOR_LAB2RGB)
    return final_image


if __name__ == "__main__":
    main()
