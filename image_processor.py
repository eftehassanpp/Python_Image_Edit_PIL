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
        line_size = 18
    elif image_for == "post":
        new_image_width, new_image_height = 1080, 1080
        required_logo_size = 300
        text_margin_bottom = 150
        text_margin_left = 80
        line_size = 16

    if not os.path.isdir(directory):
        os.makedirs(directory)

    # Load image
    img = Image.fromarray(imageArr).convert("RGB")

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

    # Add text
    draw = ImageDraw.Draw(cropped_img)
    text = title
    font = ImageFont.truetype("NotoSansJP-Bold.otf", 55)
    # Wrap text within image width
    wrapper = textwrap.TextWrapper(
        width=line_size, fix_sentence_endings=True, break_long_words=True
    )
    text_lines = wrapper.wrap(text)
    line_bbox = font.getbbox(text_lines[0])
    line_height = line_bbox[3] - line_bbox[1]
    # textbox start position defined using line height and margin bottom
    textbox_position_y = ((line_height + 10) * (len(text_lines))) + text_margin_bottom
    y = new_height - textbox_position_y

    # draw.rectangle((rec_start, rec_end), fill=(0, 0, 0))
    for line in text_lines:
        bbox = font.getbbox(line)
        line_height = bbox[3] - bbox[1]
        line_width = bbox[2] - bbox[0]
        rec_start = (text_margin_left - 10, y + 5)
        rec_end = ((text_margin_left + line_width + 15), (y + line_height + 27))
        # print(line)
        draw.rounded_rectangle(
            (rec_start, rec_end),
            fill=(255, 255, 255),
            outline=(0, 0, 0),
            radius=5,
            width=2,
        )
        draw.text((text_margin_left, y), line, spacing=20, font=font, fill=(0, 0, 0))
        y += line_height + 26  # Add margin between lines

    # Add logo
    logo = Image.fromarray(logoArr)
    logo_width, logo_height = logo.size
    new_logo_size = required_logo_size
    # logo size reduced according to the image type and required size defined on top of the file
    logo_ratio = new_logo_size / logo_width
    new_logo_width = int(logo_width * logo_ratio)
    new_logo_height = int(logo_height * logo_ratio)
    logo = logo.resize((new_logo_width, new_logo_height))
    # logo start position will be on top of the text start position so we will place is logo height size upper tan the text
    logo_start_y = new_height - textbox_position_y - int(new_logo_height + 5)
    # a background rectangle for logo on the starting to end of logo position counted by left margin and logo heigh and width
    draw.rounded_rectangle(
        (
            (text_margin_left - 10, logo_start_y - 10),
            (
                (text_margin_left + new_logo_width + 10),
                (logo_start_y + new_logo_height + 5),
            ),
        ),
        fill=(255, 255, 255),
        outline=(0, 0, 0),
        radius=5,
        width=2,
    )
    # now finally the logo is paged over the original image on the same place the background drawn
    cropped_img.paste(logo, (text_margin_left, logo_start_y), mask=logo)
    final_image = cropped_img
    # Save image
    final_image.save(f"./{directory}/{image_for}.jpg")


if __name__ == "__main__":
    im_arr = np.array(Image.open("./test/input1.webp").convert("RGBA"))
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
