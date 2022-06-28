"""Methods that are too wordy
"""
from typing import Iterable
from PIL import Image


TOL = 75


def open_file(file: str) -> str:
    """Return file contents of any plain text file in the directory file.
    """
    with open(file) as f:
        file_text = f.read()
    return file_text


def check_allowed_suffix(filename: str, allowed_suffix: Iterable) -> bool:
    """Return true if filename is one of the formats in allowed_suffix.
    """
    for suffix in allowed_suffix:
        if filename[-len(suffix):] == suffix:
            return True
    else:
        return False


class NotRGBA(Exception):
    pass


def import_image(directory: str) -> Image:
    """Import image given directory.
    The image should be a png file.
    """
    image = Image.open(directory)
    if image.mode == 'RGBA' or image.mode == 'RGB':
        # image.load()  # required for png.split()
        return image
    else:
        raise NotRGBA


def process_image(img: Image, size_to: tuple[int, int] = (250, 250)) -> \
        tuple[list[tuple[int, int, int | int, int, int, int]],
        tuple[int, int]]:
    """Return two tuples:
        - The first one is the list of the pixel data of the image
        from left to right first, then top down.
        - The second one is the (width, height) of the image."""
    img: Image = img.resize(size_to)
    width, height = img.size
    # img.show()
    pix_data = img.load()
    pixels = [pix_data[x, y] for y in range(height) for x in range(width)]
    # pix_data = [img[x, y] for x in range(width) for y in range(height)]
    # return pix_data
    return pixels, (width, height)


def extract_black_parts(pixels: list[tuple[int, int, int | int, int, int, int]], size_to: tuple[int, int],
                        tol: int) -> \
        list[tuple[int, int]]:
    """Extract the black parts of an image. All in a list of black locations."""
    wi, he = size_to
    px_list = [(i % wi, i // wi) for i, x in enumerate(pixels) if close_to_color(x, tol)]
    return px_list


def close_to_color(pixel: tuple[int, int, int | int, int, int, int], tol) -> bool:
    """Return True if the pixel is close to the color black,
    and its transparency is above 200/255."""
    conds = [
        pixel[0] < tol, pixel[1] < tol, pixel[2] < tol,
        len(pixel) < 4 or pixel[3] > 240
    ]
    tmp = all(conds)
    # print(f'the color {pixel} is {"black" if tmp else "not black"}')
    return tmp


def black_part_process(img: Image, size: tuple[int, int], tol: int = 75) -> list[tuple[int, int]]:
    """Entire black part controller"""
    px_data, size_ = process_image(img, size)
    return extract_black_parts(px_data, size_, tol)


if __name__ == '__main__':
    a1 = import_image('../frr.png')
    a2 = black_part_process(a1, (125, 125))
    print(a2)
