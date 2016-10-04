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
        self.warnings = []
        self.errors = []

    def run(self):
        self.check_files()

    def check_files(self):
        """
        Checks this chapter for problems
        :returns list<str>
        """
        self.warnings = []

        # get manifest.json
        manifest_filepath = os.path.join(self.content_dir, 'manifest.json')
        if os.path.isfile(manifest_filepath):
            with open(manifest_filepath) as manifest_file:
                self.manifest = json.load(manifest_file)

        for i in range(1, 51):
            try:
                chapter = str(i).zfill(2)
                filename = os.path.join(self.content_dir, chapter + '.html')

                if not os.path.isfile(filename):
                    self.warnings.append('Chapter {0} does not exist!'.format(chapter))
                    continue

                with open(filename) as chapter_file:
                    chapter_html = chapter_file.read()

                soup = BeautifulSoup(chapter_html, 'html.parser')

                if not soup.find('body'):
                    self.warnings.append('Chapter {0} has no content!'.format(chapter))
                    continue

                content = soup.body.find(id='content')

                if not content:
                    self.warnings.append('Chapter {0} has no content!'.format(chapter))
                    continue

                if not content.find('h1'):
                    self.warnings.append('Chapter {0} does not have a title!'.format(chapter))

                frame_count = len(content.find_all('img'))
                expected_frame_count = obs_data['chapters'][chapter]['frames']
                if frame_count != expected_frame_count:
                    self.warnings.append(
                        'Chapter {0} has only {1} frame(s).There should be {2}!'.format(chapter, frame_count,
                                                                                      expected_frame_count))

                if len(content.find_all('p')) != (frame_count * 2 + 1):
                    self.warnings.append('Bible reference not found at end of chapter {0}!'.format(chapter))
            except Exception as e:
                self.errors.append(e.message)
