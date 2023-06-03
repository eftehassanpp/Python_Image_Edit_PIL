from image_processor import edit_image
from wp_media import get_logo
from PIL import Image
import urllib.request
import numpy as np
import datetime
import urllib3
import time
import csv
import ssl
import os

# disable warnings
urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context
directory = ""


# define download image function
def dl_image(imageUrl, mode):
    ssl._create_default_https_context = ssl._create_unverified_context
    # Open the image from a URL and convert it to an ndarray
    with urllib.request.urlopen(
        imageUrl, context=ssl._create_unverified_context()
    ) as im_url:
        im_arr = np.array(Image.open(im_url).convert(mode))
        return im_arr


def fileOpener():
    with open("./info.csv", "r", encoding="UTF-8", newline="") as file:
        csvreader = csv.reader(file, delimiter=",")
        datalist = list(csvreader)
        print(len(datalist))
    return datalist


def mainProcess(i, image_url, wp_url, wp_user, wp_pass, title):
    global directory
    try:
        subdomain = wp_url.split("//")[1].split(".")[0]
        current_date = datetime.datetime.now()
        dateString = current_date.strftime("%Y-%m-%d-%H%M")
        serial_number = i + 1
        directory = f"./output/{subdomain}/{dateString}-{serial_number}"

        # get image from url
        imageArr = dl_image(
            image_url,
            "RGB",
        )

        # get logo from wp logo url
        logo_url = get_logo(wp_url, wp_user, wp_pass)
        logoArr = dl_image(logo_url, "RGBA")

        # edit image for "story"
        edit_image(
            imageArr,
            logoArr,
            title=title,
            image_for="story",
            directory=directory,
        )

        # edit image for "post"
        edit_image(
            imageArr,
            logoArr,
            title=title,
            image_for="post",
            directory=directory,
        )
        print("image edit done")
        return "Success"
    except Exception as e:
        print(e)
        return e


def justify_url(base_url):
    if base_url.startswith("http://"):
        base_url = base_url.replace("http://", "https://")
    if base_url.startswith("https://"):
        if base_url.endswith("/"):
            wpUrl = base_url
        else:
            wpUrl = base_url + "/"
    else:
        if base_url.endswith("/"):
            wpUrl = "https://" + base_url
        else:
            wpUrl = "https://" + base_url + "/"
    return wpUrl


if __name__ == "__main__":
    list = fileOpener()
    total = len(list)
    for i in range(1, total):
        print(i)
        imageUrl = list[i][1]
        base_url = list[i][4]
        wpUrl = justify_url(base_url)
        wpUser = list[i][5]
        wpPass = list[i][6]
        article_title = list[i][9]
        if not list[i][10]:
            status = mainProcess(i, imageUrl, wpUrl, wpUser, wpPass, article_title)
            list[i][10] = status
            list[i][11] = directory
            with open("./info.csv", "w", encoding="UTF-8", newline="") as new_datalist:
                csvWriter = csv.writer(new_datalist)
                csvWriter.writerows(list)
            time.sleep(2)
        else:
            print("already image edited")
    print("all done")
