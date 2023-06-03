from PIL import Image, ImageDraw, ImageFont
import textwrap
import datetime
import numpy as np
import os


def edit_image(imageArr, logoArr, title="", image_for="", directory=""):
    if image_for == "story":
        new_image_width, new_image_height = 1080, 1920
        text_margin_bottom = 350
        text_margin_left = 60
        required_logo_size = 360
        line_width = 18
    elif image_for == "post":
        new_image_width, new_image_height = 1080, 1080
        required_logo_size = 300
        text_margin_bottom = 150
        text_margin_left = 80
        line_width = 16

    if not os.path.isdir(directory):
        os.makedirs(directory)

    # Load image
    img = Image.fromarray(imageArr)

    # Crop image
    width, height = img.size
    new_width = new_image_width
    new_height = new_image_height
    # Calculate new size
    aspect_ratio = width / height
    if aspect_ratio > new_width / new_height:
        new_width = int(new_height * aspect_ratio)
    else:
        new_height = int(new_width / aspect_ratio)
    # Resize image to new size
    im_resized = img.resize((new_width, new_height))
    # Crop image to desired size
    left = (new_width - new_image_width) // 2
    top = (new_height - new_image_height) // 2
    right = left + new_image_width
    bottom = top + new_image_height
    cropped_img = im_resized.crop((left, top, right, bottom))
    new_width, new_height = cropped_img.size
    print(cropped_img.size)

    # Add text
    draw = ImageDraw.Draw(cropped_img)
    text = title
    font = ImageFont.truetype("NotoSansJP-Black.otf", 55)
    # Wrap text within image width
    wrapper = textwrap.TextWrapper(
        width=line_width, fix_sentence_endings=True, break_long_words=True
    )
    text_lines = wrapper.wrap(text)
    # print(text_lines)
    line_bbox = font.getbbox(text_lines[0])
    line_height = line_bbox[3] - line_bbox[1]
    y = new_height - (((line_height + 10) * (len(text_lines))) + text_margin_bottom)
    for line in text_lines:
        # print(line)
        draw.text((text_margin_left, y), line, font=font, fill=(255, 255, 255))
        y += line_height + 15  # Add margin between lines
    # draw.text((20, (new_height - new_height * 0.3)), text, fill=(255, 255, 255), font=font)

    # Add logo
    logo = Image.fromarray(logoArr)
    logo_width, logo_height = logo.size
    new_logo_size = required_logo_size
    logo_ratio = new_logo_size / logo_width
    new_logo_width = int(logo_width * logo_ratio)
    new_logo_height = int(logo_height * logo_ratio)
    logo = logo.resize((new_logo_width, new_logo_height))
    cropped_img.paste(logo, (new_width - (new_logo_width + 40), 60), mask=logo)

    # Save image
    cropped_img.save(f"./{directory}/{image_for}.jpg")


if __name__ == "__main__":
    im_arr = np.array(Image.open("./test/input1.webp").convert("RGB"))
    logo_arr = np.array(Image.open("./test/logo.png").convert("RGBA"))
    edit_image(
        im_arr,
        logo_arr,
        title="NTT QONOQが秋葉原にXRショールームをオープン。XR技術を無料で体験可能に。",
        image_for="story",
        directory="./test",
    )
    edit_image(
        im_arr,
        logo_arr,
        title="NTT QONOQが秋葉原にXRショールームをオープン。XR技術を無料で体験可能に。",
        image_for="post",
        directory="./test",
    )
