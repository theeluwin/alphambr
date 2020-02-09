# -*- coding: utf-8 -*-

import cv2
import numpy as np


class Alphambr(object):
    """
        Args:
            cut_margin: cut image margin
            add_padding: add paddings for bounding rectangle
            alpha_threshold: threshold for alpha channel (1 ~ 255)
            max_component_count: max component count, use all if None
            min_component_size: min component size, use all if None
    """
    def __init__(self, cut_margin=6, add_padding=10, alpha_threshold=127, max_component_count=None, min_component_size=None):
        self.cut_margin = cut_margin
        self.add_padding = add_padding
        self.alpha_threshold = alpha_threshold
        self.max_component_count = max_component_count
        self.min_component_size = min_component_size

    def __call__(self, image):

        # cut margin
        if self.cut_margin > 0:
            cm = self.cut_margin
            image = image[cm: -cm, cm: -cm, ...]

        # apply alpha threshold: it's like, x = 255 if x >= threshold else 0
        gated_alpha = cv2.threshold(image[..., -1], self.alpha_threshold, 255, cv2.THRESH_BINARY)[1]

        # get connected components
        num_components, labels = cv2.connectedComponents(gated_alpha)
        ci2counts = {}
        for ci in range(num_components):
            ci2counts[ci] = (labels == ci).sum()
        sorted_cis = sorted(ci2counts, key=ci2counts.get, reverse=True)

        # limit component count
        if self.max_component_count is not None:
            cc = self.max_component_count + 1
            doomed_cis = sorted_cis[cc:]
            for ci in doomed_cis:
                gated_alpha[labels == ci] = 0
            sorted_cis = sorted_cis[:cc]

        # limit component size
        if self.min_component_size is not None:
            cs = self.min_component_size
            survived_cis = []
            for ci in sorted_cis:
                if ci2counts[ci] < cs:
                    gated_alpha[labels == ci] = 0
                else:
                    survived_cis.append(ci)
            sorted_cis = survived_cis

        # get MBR
        gate = (gated_alpha >= self.alpha_threshold)
        wh = np.where(gate)
        H, W, C = image.shape
        y1, y2 = np.min(wh[0]), np.max(wh[0])
        x1, x2 = np.min(wh[1]), np.max(wh[1])
        H = y2 - y1
        W = x2 - x1

        # draw on canvas
        p = self.add_padding
        canvas = np.zeros((H + 2 * p, W + 2 * p, C), dtype=np.uint8)
        canvas[p: -p, p: -p, :] = image[y1: y2, x1: x2, ...]
        canvas[p: -p, p: -p, -1] *= gate[y1: y2, x1: x2]
        return canvas
