# -*- coding: utf-8 -*-

import os
import argparse

from tqdm import tqdm
from skimage.io import imread
from skimage.io import imsave

from alphambr import Alphambr


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', type=str, default='./images')
    parser.add_argument('--result_dir', type=str, default='./results')
    args = parser.parse_args()
    return args


def example(args):

    # init
    ambr = Alphambr(
        cut_margin=1,
        add_padding=12,
        alpha_threshold=1,
        max_component_count=2,
        min_component_size=50 * 50
    )

    # prepare result
    os.makedirs(args.result_dir, exist_ok=True)

    # for each samples
    fnames = os.listdir(args.image_dir)
    for fname in tqdm(fnames):

        # get name
        splitted = fname.split('.')
        ext = splitted[-1]
        name = '.'.join(splitted[:-1])

        # read image
        ipath = os.path.join(args.image_dir, fname)
        try:
            image = imread(ipath)
        except ValueError:  # if not image
            continue

        # run (functor)
        mbred = ambr(image)

        # save image
        fname = f'{name}_ambred.{ext}'
        ipath = os.path.join(args.result_dir, fname)
        imsave(ipath, mbred)


if __name__ == '__main__':
    args = parse_args()
    example(args)
