"""First, test out the mouse."""
import json
import time
from dataclasses import dataclass
# from typing import Iterable
from pynput import keyboard

import mouse

from extras import extras as ext

TEST_LIST = [(100 + x, x) for x in range(300, 700)]
P_TOL = 2


@dataclass
class GlobalClass:
    gv: bool


gv = GlobalClass(False)


@dataclass
class SingleClick:
    x: int
    y: int
    mc: bool = False


@dataclass
class MoveClick:
    x1: int  # start
    y1: int
    x2: int  # end
    y2: int
    mc: bool = True


def open_and_compress_images():
    """Open and compress an image to a 250x250 matrix
    which contains RGB values."""


def run_mouse(locations: list[tuple[int, int]], start_pos: tuple[int, int] = (0, 0), scale: int = 1) -> None:
    """Click the mouse in all applicable locations.
    start_pos: the starting position (x, y).
    scale: does not affect the starting position.
    """
    # mouse.click('left')
    # time.sleep(1)
    # mouse.drag(300, 300, 600, 600, absolute=True, duration=1)
    locations_transformed = [(x[0] * scale + start_pos[0], x[1] * scale + start_pos[1]) for x in locations]

    for cur_pos in locations_transformed:
        mouse.move(cur_pos[0], cur_pos[1], True,
                   duration=0.00001)
        mouse.click()  # left click


def run_mouse_better(locations: list[tuple[int, int]],
                     start_pos: tuple[int, int] = (0, 0), scale: int = 1,
                     p_tol: int = 1, interlacing: int = 0) -> None:
    """It works way better this time"""
    p_tol = abs(p_tol)
    if p_tol == 0:
        p_tol = 1
    # Everything should be sorted. Look for runs.
    new_locations: list[SingleClick | MoveClick] = []
    p_location = [-88, -88]
    run_start = [0, 0]
    run_mode = False
    for loc in locations:
        # if the previous position is one left than the current position
        if loc[0] - p_tol <= p_location[0] <= loc[0] - 1 and p_location[1] == loc[1]:
            if not run_mode:  # starting a new run mode
                run_mode = True
                run_start[0] = loc[0]
                run_start[1] = loc[1]

        else:  # otherwise - end the run mode
            if run_mode:
                run_mode = False
                if check_interlacing(p_location[1], interlacing):
                    new_locations.append(MoveClick(scale * run_start[0] + start_pos[0],
                                                   scale * run_start[1] + start_pos[1],
                                                   scale * p_location[0] + start_pos[0],
                                                   scale * p_location[1] + start_pos[1]))
            if check_interlacing(p_location[1], interlacing):
                new_locations.append(SingleClick(scale * loc[0] +
                                                 start_pos[0],
                                                 scale * loc[1] +
                                                 start_pos[1]))
        p_location[0] = loc[0]
        p_location[1] = loc[1]

    for new_loc in new_locations:
        if gv.gv:
            raise KeyboardInterrupt
        if new_loc.mc:
            mouse.drag(new_loc.x1, new_loc.y1, new_loc.x2, new_loc.y2, absolute=True, duration=0)
        else:
            mouse.move(new_loc.x, new_loc.y, True)
            time.sleep(0.00001)
            mouse.click()


def check_interlacing(row_num: int, interlace: int) -> bool:
    """If interlacing is on, check if the
    row passes."""
    if interlace <= 0:
        return True
    elif row_num % (interlace + 1) == 0:
        return True
    else:
        return False


def main(tolerance: int, p_tolerance: int, path_to_img: str,
         img_scale: tuple[int, int], img_start_position: tuple[int, int],
         finish_scale: int, interlacing: int = 0):
    # the lower the number, the more black a color has to be.
    # you want to do to the image. This number is always positive
    # (it will be made positive if not) and the greater it is, the
    # more compressed the image seems. Set to 1 for the most
    # optimal image.
    # mouse.hook(lambda: raise KeyboardInterrupt)
    a1 = ext.import_image(path_to_img)
    a2 = ext.black_part_process(a1, img_scale, tolerance)
    run_mouse_better(a2, img_start_position, finish_scale, p_tolerance,
                     interlacing)
    # print(a2)


def img_center_to_top_left(pos: tuple[int, int], img_size: tuple[int, int]) -> tuple[int, int]:
    """I haven't and will not be testing this out."""
    px, py = pos
    sx, sy = img_size
    return (px - sx) // 2, (py - sy) // 2


def main_from_json() -> None:
    with open('variables.json') as jf:
        data = json.load(jf)
    main(data["tolerance"], data["p_tolerance"], data["path_to_img"], tuple(data["img_scale"]),
         tuple(data["img_start_position"]), data["finish_scale"],
         data["interlacing"])


def on_press(key):
    print('you pressed something')
    gv.gv = True
    print(gv.gv)
    # exit(42069)
    # raise KeyboardInterrupt
    #
    # try:
    #     print('alphanumeric key {0} pressed'.format(
    #         key.char))
    # except AttributeError:
    #     print('special key {0} pressed'.format(
    #         key))


def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


if __name__ == '__main__':
    # Collect events until released
    # https://pynput.readthedocs.io/en/latest/keyboard.html
    # ...or, in a non-blocking fashion:
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()
    main_from_json()

    # t_tolerance = 30  # lower, the less black
    # t_p_tolerance = 4  # lower, the less compressed
    # t_path_to_img = 'nya.png'  # path to img
    # t_img_scale = (500, 500)  # canvas scale
    # t_img_start_position = (200, 200)  # start pos
    # t_finish_scale = 1  # scalar-vector product of img scale
    # t_interlacing = 1  # the amount of interlacing
    #
    # time.sleep(2)  # prevent anything from happening for 4 seconds in case you change your mind
    # main(t_tolerance,
    #      t_p_tolerance,
    #      t_path_to_img,
    #      t_img_scale,
    #      t_img_start_position,
    #      t_finish_scale,
    #      t_interlacing)
    # # print(a2)
