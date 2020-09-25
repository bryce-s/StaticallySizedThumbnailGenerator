import sys
import PIL
from PIL import Image
import os
import shutil
import threading

inputDir: str = "./inputs/"
outputDir: str = "./outputs/"

smallSize = 220, 124
medSize = 700, 394


def reset_output_dir():
    if (os.path.exists(outputDir)):
        shutil.rmtree(outputDir)
    os.mkdir(outputDir)


def save_image(image: Image, filename: str):
    image.save(os.path.join(outputDir, filename))


def generate_filename(imageName: str, sizeTag: str):
    splitImageName: list = imageName.split('.')
    if sizeTag != "-sm" and sizeTag != "-lg":
        print("invalid sizetag")
        exit()
    return f'{splitImageName[0]}{sizeTag}.{splitImageName[1]}'


def open_and_resize_image(imageName: str):
    if not imageName.lower().endswith(".jpg") and not imageName.lower().endswith(".png"):
        print("We only accept png and jpg images")
        sys.exit()
    image: object = Image.open(os.path.join(inputDir, imageName))

    smallImage = image.resize(smallSize)
    medImage = image.resize(medSize)

    save_image(smallImage, generate_filename(imageName, "-s"))
    save_image(medImage, generate_filename(imageName, "-l"))


def absoluteFilePaths(directory):
   for dirpath, _, filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))


def walk_input_files():
    filenames: list = os.listdir(inputDir)
    return filenames


def resize_images():
    reset_output_dir()
    filenames: list = walk_input_files()
    for filename in filenames:
        newThread = threading.Thread(
            target=open_and_resize_image, args=(filename,))
        newThread.start()


resize_images()
