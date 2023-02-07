from __future__ import annotations
import cv2
import numpy as np
from typing import List, NoReturn
import os


def rescale_image(image: np.ndarray, rescale_ratio: int = 100) -> np.ndarray:
    width = int(image.shape[1] * rescale_ratio / 100)
    height = int(image.shape[0] * rescale_ratio / 100)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


def select_roi(image: np.ndarray, rescale_ratio: int = 100) -> List[int | any]:
    if rescale_ratio != 100:
        image = rescale_image(image, rescale_ratio)
    roi_of_image = cv2.selectROI(image)
    roi_of_image = list(roi_of_image)
    for x in range(len(roi_of_image)):
        roi_of_image[x] = int((roi_of_image[x] * 100) / rescale_ratio)

    cv2.destroyWindow("ROI selector")
    return roi_of_image


def choose_size(image_raw: np.ndarray) -> List[int | any]:
    if image_raw.shape[0] > 3000:
        roi_values = select_roi(image_raw, 30)

    elif image_raw.shape[0] > 2000:
        roi_values = select_roi(image_raw, 35)

    elif image_raw.shape[0] > 1500:
        roi_values = select_roi(image_raw, 45)

    elif image_raw.shape[0] > 1000:
        roi_values = select_roi(image_raw, 80)

    else:
        roi_values = select_roi(image_raw, 100)

    return roi_values


def manage_image(source: str, output_file_name: str, labels: List[str]) -> NoReturn | bool:
    image_raw = cv2.imread(source)

    while True:
        roi_values = choose_size(image_raw)
        cv2.imshow("ROI", image_raw[int(roi_values[1]):int(roi_values[1] + roi_values[3]),
                          int(roi_values[0]):int(roi_values[0] + roi_values[2])])

        cv2.waitKey(0)
        cv2.destroyWindow("ROI")

        choice = input("q - end session without save\n"
                       "a - select ROI to this photo again")

        if choice == 'q':
            return True
        elif choice != 'a':
            break

    with open(output_file_name, "a") as fp:
        file = source.split("\\")[-1]
        which_label = file.split("_")[0]
        fp.write(f"{file} {roi_values[0]},{roi_values[1]},{roi_values[0] + roi_values[2]},\
                {roi_values[1] + roi_values[3]},{labels.index(which_label)}\n")


def roi(source: str | List[str], output_file_name: str, labels: List[str], many_sources: int = 0,
        append_mode: bool = False) -> None:
    """ Function allows to mark ROI thanks to easy GUI from cv2. Function automatically rescales images for fitting on
    the screen, but marked ROI is respondent for original size.

    !!! Names of images have to be in format "label_number.format". !!!

    Parameters:
        source (str | List[str]): Directory to folder with images, directory to folder with others folders which contain
                                  images or list of directories to folders with images.

        output_file_name (str): Name of file where ROI parameters will be saved. If output_file_name does not end
                                with ".txt", function will add that suffix.

        labels (List[str]): List of labels names. In output file label of image will be saved as number. That number
                            is index of label name in given list.

        many_sources (int, default: 0): Flag which allow to determine source type.
                                        0 - directory to folder with images,
                                        1 - directory to folder with others folders which contain images,
                                        2 - list of directories to folders with images.

        append_mode (bool, default: False): Flag which determine if new file (output_file_name) will be created
                                            or data will be appended to earlier made file.
                                            If append_mode is False but file exists, ValueError is raised.
    """

    if (many_sources == 0 or many_sources == 1) and isinstance(source, list):
        raise TypeError("many_sources is 0 or 1 but list isn't given in parameters.")

    elif many_sources == 2 and isinstance(source, str):
        raise TypeError("many_sources is 2 but string isn't given in parameters.")

    elif many_sources and not source:
        raise ValueError("source is empty!")

    elif not labels:
        raise ValueError("labels is empty!")

    if output_file_name.split('.')[-1] != "txt":
        output_file_name += ".txt"

    if not append_mode and os.path.exists(output_file_name):
        raise ValueError("File with this name already exist.")

    if many_sources == 0:
        for file in os.listdir(source):
            if manage_image(f"{source}\\{file}", output_file_name, labels):
                return

    elif many_sources == 1:
        for folder in os.listdir(source):
            for file in os.listdir(f"{source}\\{folder}"):
                if manage_image(f"{source}\\{folder}\\{file}", output_file_name, labels):
                    return

    elif many_sources == 2:
        for directory in source:
            for file in os.listdir(directory):
                if manage_image(f"{directory}\\{file}", output_file_name, labels):
                    return
