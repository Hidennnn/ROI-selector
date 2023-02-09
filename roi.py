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


def save_roi(output_folder: str, file: str, index: int, roi_values: List[int]) -> None:
    with open(f"{output_folder}\\{file[:-3]+'txt'}", "a") as fp:
        fp.write(f"{index} {roi_values[0]},{roi_values[1]},{roi_values[0] + roi_values[2]},"
                 f"{roi_values[1] + roi_values[3]}\n")


def manage_image(source: str, output_folder: str, labels: List[str]) -> NoReturn | bool:
    image_raw = cv2.imread(source)
    flag = 0

    while True:
        roi_values = choose_size(image_raw)
        cv2.imshow("ROI", image_raw[int(roi_values[1]):int(roi_values[1] + roi_values[3]),
                          int(roi_values[0]):int(roi_values[0] + roi_values[2])])

        cv2.waitKey(0)
        cv2.destroyWindow("ROI")

        choice = input("\nq - end session without save\n"
                       "a - correct ROI to this photo\n"
                       "o - quit with save\n"
                       "s - select ROI for the same label\n"
                       "r - select ROI for another label\n")

        if flag == 0:
            index = labels.index(source.split("\\")[-1].split("_")[0])

        if choice == 'q':
            return True
        elif choice == 'o':
            save_roi(output_folder, source.split("\\")[-1], index, roi_values)
            return True
        elif choice == 'r':
            save_roi(output_folder, source.split("\\")[-1], index, roi_values)
            flag = 1
            index = int(input("Index of the new label: "))
        elif choice == 's':
            save_roi(output_folder, source.split("\\")[-1], index, roi_values)
        elif choice != 'a':
            save_roi(output_folder, source.split("\\")[-1], index, roi_values)
            break


def roi(source: str | List[str], labels: List[str], output_folder: str, many_sources: int = 0) -> None:
    """ Function allows to mark ROI thanks to easy GUI from cv2. Function automatically rescales images for fitting on
    the screen, but marked ROI is respondent for original size.

    !!! Names of images have to be in format "label_number.format". !!!

    Parameters:
        source (str | List[str]): Directory to folder with images, directory to folder with others folders which contain
                                  images or list of directories to folders with images.

        labels (List[str]): List of labels names. In output file label of image will be saved as number. That number
                            is index of label name in given list.

        output_folder (str): Folder where txt files with ROI values will be saved.

        many_sources (int, default: 0): Flag which allow to determine source type.
                                        0 - directory to folder with images,
                                        1 - directory to folder with others folders which contain images,
                                        2 - list of directories to folders with images.
    """

    if (many_sources == 0 or many_sources == 1) and isinstance(source, list):
        raise TypeError("many_sources is 0 or 1 but list isn't given in parameters.")

    elif many_sources == 2 and isinstance(source, str):
        raise TypeError("many_sources is 2 but string isn't given in parameters.")

    elif many_sources and not source:
        raise ValueError("source is empty!")

    elif not labels:
        raise ValueError("labels is empty!")

    if many_sources == 0:
        for file in os.listdir(source):
            if manage_image(f"{source}\\{file}", output_folder, labels):
                return

    elif many_sources == 1:
        for folder in os.listdir(source):
            for file in os.listdir(f"{source}\\{folder}"):
                if manage_image(f"{source}\\{folder}\\{file}", output_folder, labels):
                    return

    elif many_sources == 2:
        for directory in source:
            for file in os.listdir(directory):
                if manage_image(f"{directory}\\{file}", output_folder, labels):
                    return
