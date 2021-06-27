from __future__ import annotations

import imghdr
import pathlib
import os
from typing import Tuple

from PIL import Image, ImageMath
import numpy as np



class LRel:

    def __init__(self, working_dir: str = None):
        self.image_paths_training_0: [pathlib.Path] = []
        self.image_paths_training_1: [pathlib.Path] = []
        self.image_paths_validation_0: [pathlib.Path] = []
        self.image_paths_validation_1: [pathlib.Path] = []

        self.training_x: np.ndarray = np.empty(0)
        self.training_y: np.ndarray = np.empty(0)
        self.validation_x: np.ndarray = np.empty(0)
        self.validation_y: np.ndarray = np.empty(0)

        self.working_dir = None
        self.training_dir = None
        self.training_dir_0 = None
        self.training_dir_1 = None
        self.validation_dir = None
        self.validation_dir_0 = None
        self.validation_dir_1 = None

        self.training_0_count = 0
        self.training_1_count = 0
        self.validation_0_count = 0
        self.validation_1_count = 0

        self.open_directories(working_dir)

    def open_directories(self, working_dir: str = None):

        if working_dir:
            self.working_dir = working_dir

            self.training_dir = working_dir + "/training"
            self.training_dir_0 = self.training_dir + "/0"
            self.training_dir_1 = self.training_dir + "/1"

            self.validation_dir = working_dir + "/validation"
            self.validation_dir_0 = self.validation_dir + "/0"
            self.validation_dir_1 = self.validation_dir + "/1"
        else:
            self.working_dir = self.validation_dir = self.validation_dir = None
            self.validation_dir_1 = self.validation_dir_0 = self.training_dir_1 = self.training_dir_0 = None

    # todo later lets return numeric values for the error? or something different than txt
    def process_directories(self, signal) -> str:
        # initializaiton of values.
        msg = "sucess"
        self.training_0_count = self.training_1_count = 0
        self.validation_0_count = self.validation_1_count = 0

        self.image_paths_training_0 = []
        self.image_paths_training_1 = []
        self.image_paths_validation_0 = []
        self.image_paths_validation_1 = []

        if not os.path.exists(self.working_dir):
            msg = f"working dir does not exist: {self.working_dir}"

        if not os.path.exists(self.training_dir):
            msg = f"training dir does not exist: {self.training_dir}"

        if not os.path.exists(self.training_dir_0):
            msg = f"training_0 dir does not exist: {self.training_dir_0}"

        if not os.path.exists(self.training_dir_1):
            msg = f"training_1 dir does not exist: {self.training_dir_1}"

        if not os.path.exists(self.validation_dir):
            msg = f"validation dir does not exist: {self.validation_dir}"

        if not os.path.exists(self.validation_dir_0):
            msg = f"validation dir does not exist: {self.validation_dir_0}"

        if not os.path.exists(self.validation_dir_1):
            msg = f"validation dir does not exist: {self.validation_dir_1}"

        for path in pathlib.Path(self.training_dir_0).iterdir():
            if path.is_file() and imghdr.what(path) == "jpeg":
                LRel.send_signal_image_found(signal, path)
                self.image_paths_training_0.append(path)
                self.training_0_count += 1

        for path in pathlib.Path(self.training_dir_1).iterdir():
            if path.is_file() and imghdr.what(path) == "jpeg":
                self.image_paths_training_1.append(path)
                LRel.send_signal_image_found(signal, path)
                self.training_1_count += 1

        for path in pathlib.Path(self.validation_dir_0).iterdir():
            if path.is_file() and imghdr.what(path) == "jpeg":
                self.image_paths_validation_0.append(path)
                LRel.send_signal_image_found(signal, path)
                self.validation_0_count += 1

        for path in pathlib.Path(self.validation_dir_1).iterdir():
            if path.is_file() and imghdr.what(path) == "jpeg":
                self.image_paths_validation_1.append(path)
                LRel.send_signal_image_found(signal, path)
                self.validation_1_count += 1

        return msg

    def initialize_image_arrays(self, pixels):
        self.training_x = np.empty(LRel.calculate_image_array_shape(self.training_count, pixels))
        self.training_y = np.empty((self.training_count, 1))

    def preprocess_images(self, pixels):
        self.initialize_image_arrays(pixels)
        for index, path in enumerate(self.image_paths_training_0):
            print(f"processing: {path}")
            self.training_x[index] = self.open_and_normalize_image(pixels, path)

        for index, path in enumerate(self.image_paths_training_1):
            print(f"processing: {path}")
            self.training_x[index + len(self.image_paths_training_0)] = self.open_and_normalize_image(pixels, path)

        for i in range(self.training_0_count):
            self.training_y[i] = 0
        for i in range(self.training_1_count):
            self.training_y[i+self.training_0_count] = 1



    @staticmethod
    def open_and_normalize_image(pixels, path) -> np.ndarray:
        img = Image.open(path).resize((pixels, pixels))
        np_img = np.array(img)

        if len(np_img.shape) < 3:
            rgb_img = Image.new("RGB", img.size)
            rgb_img.paste(img)
            np_img = np.array(rgb_img)

        return np_img/255


    @staticmethod
    def calculate_image_array_shape(n_images: int, pixels: int) -> Tuple[int, int, int, int]:
        # since were only using jpeg images their dimensions will be (pixels, pixels, 3)
        return n_images, pixels, pixels, 3

    @staticmethod
    def send_signal_message(signal, msg):
        signal.emit(msg)

    @staticmethod
    def send_signal_image_found(signal, path):
        LRel.send_signal_message(signal, f"found img:{path}")

    @property
    def training_count(self) -> int:
        return self.training_0_count + self.training_1_count

    @property
    def validation_count(self) -> int:
        return self.validation_0_count + self.validation_1_count
