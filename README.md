# ROI-selector

Version 1.0.1 - 07.02.2023

Function allows to mark ROI thanks to easy GUI from cv2. Function automatically rescales images for fitting on the screen, but marked ROI is respondent for original size.

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

TODO:
- improve documentation.
- better cleaning of code.
- allow to save files in .csv
- better place of showing control image.
