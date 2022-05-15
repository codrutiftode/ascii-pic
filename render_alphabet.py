import json
from PIL import ImageDraw, Image, ImageFont
import os
import json

ALPHABET_DIR = "./alphabet/"
ALPHABET_PNG = "alphabet.png"
ALPHABET_META = "alphabet.json"

def render_alphabet():
    alphabet = "~/#@0$!&*"
    font_size = 25

    # Create output dir
    if not os.path.isdir(ALPHABET_DIR):
        os.mkdir(ALPHABET_DIR)

    # Font config
    font = ImageFont.truetype("./fonts/Courier.ttf", font_size)
    image_width, image_height = font.getsize("#")
    image_size = (image_width * len(alphabet), image_height)

    # Render alphabet
    print("Rendering alphabet...")
    image_out = Image.new("RGB", image_size, (90, 90, 90))
    draw_context = ImageDraw.Draw(image_out)
    for (i, char) in enumerate(alphabet):
        draw_context.text((i * image_width, 0), text=char,
                        font=font, fill=(255, 255, 255))

    image_out.save(ALPHABET_DIR + ALPHABET_PNG)

    # Write alphabet metadata
    with open(ALPHABET_DIR + ALPHABET_META, "w") as alphabet_meta:
        alphabet_meta.write(json.dumps({
            "char_width": image_width,
            "char_height": image_height,
            "chars": alphabet
        }))

    print("Render done.")


class Alphabet():
    """ Loads and unloads an alphabet and its metadata """
    def __init__(self, alphabet_dir):
        self.image_path = alphabet_dir + ALPHABET_PNG
        self.meta_path = alphabet_dir + ALPHABET_META

    def __enter__(self):
        self.image = Image.open(self.image_path)
        with open(self.meta_path) as meta_file:
            self.meta = json.loads(meta_file.read())
        return self

    def __exit__(self, type, value, traceback):
        self.image.close()


# Main function behaviour
if __name__ == "__main__":
    render_alphabet()