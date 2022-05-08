from PIL import ImageDraw, Image, ImageFont
import os

alphabet = "~/#@0$!&*"
output_dir = "./alphabet/"
font_size = 25

# Create output dir
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

# Font config
font = ImageFont.truetype("./fonts/Courier.ttf", font_size)
image_width, image_height = font.getsize("#")
print(image_width, image_height)
image_size = (image_width * len(alphabet), image_height)

# Render alphabet
image_out = Image.new("RGB", image_size, (150, 150, 150))
draw_context = ImageDraw.Draw(image_out)
for (i, char) in enumerate(alphabet):
    draw_context.text((i * image_width, 0), text=char, font=font, fill=(255, 255, 255))

image_out.save(output_dir + "alphabet.png")