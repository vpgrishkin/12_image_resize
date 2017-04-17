from os.path import exists, join, splitext, sys
from os import makedirs
import argparse

from PIL import Image


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='A path to the images')
    parser.add_argument('-W', '--width', type=int)
    parser.add_argument('-H', '--height', type=int)
    parser.add_argument('-s', '--scale', type=float)
    parser.add_argument('-o', '--output', help='A output folder')
    return parser.parse_args()


def has_valid_arguments_or_print_msg(arguments):
    if not exists(arguments.path):
        print('No any image')
        return False
    if arguments.scale and (arguments.width or arguments.height):
        print('You can input only scale and width or height at once')
        return False
    if not (arguments.scale or arguments.width or arguments.height):
        print('You have to input scale or height or width of the result image')
        return False
    return True



def get_new_image_size(width, height, new_width, new_height, scale):
    if scale is not None:
        return int(width * scale), int(height * scale)
    if new_height is None:
        scale = new_width / width
        return new_width, int(height * scale)
    if new_width is None:
        scale = new_height / height
        return int(width * scale), new_height
    return new_width, new_height


def resize_image(image, width, height, scale):
    original_width, original_height = image.size
    new_width, new_height = get_new_image_size(original_width, original_height, width, height, scale)
    new_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    print(original_width, original_height, width, height)
    if (original_width / original_height != new_width / new_height):
        print('The image proportion was changed!')
    return new_image


def save_image(output_path, path_to_image, image):
    width, height = image.size
    base, ext = splitext(path_to_image)
    image_file_name = '{}__{}x{}{}'.format(base, width, height, ext)
    if output_path is None:
        image.save(image_file_name)
    else:
        try:
            makedirs(output_path)
        except OSError:
            pass
        image.save(join(output_path, image_file_name))


if __name__ == '__main__':
    arguments = get_arguments()

    if not has_valid_arguments_or_print_msg(arguments):
        print('Exit. The arguments isn\'t valid')
        sys.exit(1)

    image = Image.open(arguments.path)
    new_image = resize_image(image, arguments.width, arguments.height, arguments.scale)
    save_image(arguments.output, arguments.path, new_image)
    print('Completed')