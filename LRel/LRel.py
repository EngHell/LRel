from __future__ import annotations

import imghdr
import pathlib
import os
from typing import Tuple, Dict

from PIL import Image, ImageMath
import numpy as np
import h5py
from h5py import Group


class LRel:

    def __init__(self, working_dir: str = None):
        self.image_paths_training_0: [pathlib.Path] = []
        self.image_paths_training_1: [pathlib.Path] = []
        self.image_paths_validation_0: [pathlib.Path] = []
        self.image_paths_validation_1: [pathlib.Path] = []
        self.training_dataset_dictionary: Dict = {}

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
        self.open_images_for_array_with_label_and_offset(
            self.training_x, self.training_y, self.image_paths_training_0, 0, pixels
        )
        self.open_images_for_array_with_label_and_offset(
            self.training_x, self.training_y, self.image_paths_training_1, 1, pixels, self.training_0_count
        )
        self.training_dataset_dictionary = {
            "X": self.training_x,
            "Y": self.training_y
        }

        self.save_dictionary("training", self.training_dataset_dictionary)

    def save_dictionary(self, name: str, dictionary: Dict[str, np.ndarray]):
        filename = self.working_dir + "/datasets.hdf5"
        with h5py.File(filename, "a") as f:
            if name in f:
                del f[name]
            group = f.create_group(name)
            for key, value in dictionary.items():
                group.create_dataset(key, data=value)

        print(f"saved: {name}")
        print(f"shape: {group.visititems()}")

    def open_dictionary(self, name: str) -> Dict[str, np.ndarray]:
        dictionary: Dict[str, np.ndarray] = {}
        with h5py.File(self.working_dir + "/datasets.hdf5", "r") as f:
            group: Group = f[name]
            group.visititems(LRel.populate_dictionary(dictionary))
        return dictionary

    @staticmethod
    def populate_dictionary(dictionary):
        def inner(name, group):
            dictionary[name] = np.array(group)
            return None
        return inner

    def open_images_for_array_with_label_and_offset(self, array_x, array_y, paths, label, pixels, offset=0):
        for index, path in enumerate(paths):
            print(f"processing: {path}")
            array_x[offset + index] = self.open_and_normalize_image(pixels, path)
            array_y[offset + index] = label

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
