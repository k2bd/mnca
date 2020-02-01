import os

import numpy as np


def load_masks(dir_name):
    """
    Loads masks from a target directory and returns a dict of name: mask
    """
    # TODO: trim masks

    masks = {}
    for mask_name in os.listdir(dir_name):
        with open(os.path.join(dir_name, mask_name), "r") as f:
            mask = [[int(n) for n in line.split()] for line in f.readlines()]
            masks[mask_name] = np.array(mask, ndmin=2)

    return masks
