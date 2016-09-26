from __future__ import print_function, unicode_literals

import os
import json

from glob import glob
from bs4 import BeautifulSoup

from general_tools.file_utils import load_json_object
from obs_data import obs_data


class OBSStatus(object):
    def __init__(self, content_dir=None):
        """
        Class constructor. Takes a path to a directory
        :param object content_dir: Path to the directory of OBS manifest file
        """
        self.content_dir = content_dir

        self. manifest_file = os.path.join(self.content_dir, 'manifest.json')
        if os.path.isfile(self. manifest_file):
            self.__dict__ = load_json_object(self.manifest_file)
        else:
            raise IOError('The file {0} was not found.'.format(self.manifest_file))

    def __contains__(self, item):
        return item in self.__dict__


class OBSInspection(object):
    def __init__(self, content_dir=None):
        """
        Class constructor. Takes a path to a directory
        :param object content_dir: Path to the directory of OBS chapter files and manifest
        """
        self.content_dir = content_dir
        self.files = sorted(glob(os.path.join(self.content_dir, '*.html')))
        self.manifest = {}

    def run(self):
        # get manifest.json
        with open(os.path.join(self.content_dir, 'manifest.json')) as manifest_file:
            self.manifest = json.load(manifest_file)
        return self.get_errors()

    def get_errors(self):
        """
        Checks this chapter for errors
        :returns list<str>
        """
        errors = []

        for i in range(1, 51):
            chapter = str(i).zfill(2)
            filename = os.path.join(self.content_dir, chapter + '.html')

            if not os.path.isfile(filename):
                errors.append('Chapter {0} does not exist!'.format(chapter))
                continue

            with open(filename) as chapter_file:
                chapter_html = chapter_file.read()

            soup = BeautifulSoup(chapter_html, 'html.parser')

            content = soup.body.find(id='content')

            if not content:
                errors.append('Chapter {0} has not content!'.format(chapter))
                continue

            if not content.h1:
                errors.append('Chapter {0} does not have a title!'.format(chapter))

            frame_count = len(content.find_all('img'))
            expected_frame_count = obs_data['chapters'][chapter]['frames']
            if frame_count != expected_frame_count:
                errors.append('Chapter {0} has only {0} frames.There should be {0}!'.format(chapter, frame_count, expected_frame_count))

            if len(soup.content.p) != (frame_count * 2 + 1):
                errors.append('Bible reference not found at end of chapter {0}!'.format(chapter))

        return errors

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

    def __str__(self):
        return self.__class__.__name__ + ' ' + self.number
