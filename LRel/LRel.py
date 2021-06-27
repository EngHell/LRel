from __future__ import annotations

import imghdr
import pathlib
import os


class LRel:

    def __init__(self, working_dir: str = None):
        self.training_0_images: [pathlib.Path] = []
        self.training_1_images: [pathlib.Path] = []
        self.validation_0_images: [pathlib.Path] = []
        self.validation_1_images: [pathlib.Path] = []

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

        self.training_0_images = []
        self.training_1_images = []
        self.validation_0_images = []
        self.validation_1_images = []

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
                self.training_0_images.append(path)
                self.training_0_count += 1

        for path in pathlib.Path(self.training_dir_1).iterdir():
            if path.is_file() and imghdr.what(path) == "jpeg":
                self.training_1_images.append(path)
                LRel.send_signal_image_found(signal, path)
                self.training_1_count += 1

        for path in pathlib.Path(self.validation_dir_0).iterdir():
            if path.is_file() and imghdr.what(path) == "jpeg":
                self.validation_0_images.append(path)
                LRel.send_signal_image_found(signal, path)
                self.validation_0_count += 1

        for path in pathlib.Path(self.validation_dir_1).iterdir():
            if path.is_file() and imghdr.what(path) == "jpeg":
                self.validation_1_images.append(path)
                LRel.send_signal_image_found(signal, path)
                self.validation_1_count += 1

        return msg

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
