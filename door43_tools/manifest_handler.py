# -*- coding: utf-8 -*-

# Transforms old versions of manifest.json files to the latest

from __future__ import print_function, unicode_literals

import os
import json

from six import iteritems
from door43_tools import bible_books
from door43_tools.language_handler import Language


class Manifest(object):
    LATEST_VERSION = 6

    def __init__(self, manifest_path=None):
        # Set Defaults
        self.package_version = Manifest.LATEST_VERSION
        self.format = "markdown"
        self.generator = {
            "name": "",
            "build": ""
        }
        self.target_language = {
            "id": None,
            "name": None,
            "direction": "ltr"
        }
        self.project = {
            "id": None,
            "name": None
        }
        self.type = {
            "id": "text",
            "name": "Text"
        }
        self.resource = {
            "id": None,
            "name": None
        }
        self.source_translations = []
        self.parent_draft = {}
        self.translators = []
        self.finished_chunks = []

        if manifest_path:
            self.load_from_file(manifest_path)

    def load_from_file(self, path):
        with open(path, 'r') as f:
            manifest = json.load(f)
        manifest = Manifest.standardize_manifest_json(manifest)
        self.populate(manifest)

    def populate(self, manifest):
        for key, value in iteritems(manifest):
            setattr(self, key, value)

    @staticmethod
    def standardize_manifest_json(manifest):
        new_manifest = manifest

        translators = []
        if 'translators' in new_manifest:
            for translator in new_manifest['translators']:
                if isinstance(translator, dict) and 'name' in translator:
                    translators.append(translator['name'])
                elif isinstance(translator, basestring):
                    translators.append(translator)
        new_manifest['translators'] = translators

        source_translations = []
        if 'source_translations' in manifest:
            if isinstance(manifest['source_translations'], dict):
                for key in manifest['source_translations'].keys():
                    source = manifest['source_translations'][key]
                    prod, lang, resource = key.split('-')
                    source['language_id'] = lang
                    source['resource_id'] = resource
                    source_translations.append(source)
                    if 'resource' not in new_manifest:
                        new_manifest['resource'] = {'id': resource, 'name': 'UNKNOWN'}
                        if resource == 'ulb':
                            new_manifest['resource']['name'] = 'Unlocked Literal Bible'
                        if resource == 'udb':
                            new_manifest['resource']['name'] = 'Unlocked Dynamic Bible'
                        if resource == 'obs':
                            new_manifest['resource']['name'] = 'Open Bible Stories'
                        if resource == 'tn':
                            new_manifest['resource']['name'] = 'translationNotes'
                        if resource == 'tw':
                            new_manifest['resource']['name'] = 'translationWords'
                        if resource == 'tq':
                            new_manifest['resource']['name'] = 'translationQuestions'
                        if resource == 'ta':
                            new_manifest['resource']['name'] = 'translationAcademy'
                    if 'format' not in manifest:
                        if resource == 'ulb' or resource == 'udb':
                            new_manifest['format'] = 'usfm'
                        else:
                            new_manifest['format'] = 'markdown'

        new_manifest['source_translations'] = source_translations

        if 'project' not in manifest:
            new_manifest['project'] = {}
            if 'project_id' in manifest:
                del new_manifest['project_id']
                new_manifest['project'] = {'id': manifest['project_id'], 'name': 'UNKNOWN'}
                if new_manifest['resource']['id'] == 'ulb' or new_manifest['resource']['id'] == 'udb':
                    new_manifest['project']['name'] = bible_books.BOOK_NAMES[new_manifest['project']['id']]

        if 'parent_drafts' not in manifest:
            new_manifest['parent_drafts'] = {}

        if 'finished_frames' in manifest:
            del new_manifest['finished_frames']
            new_manifest['finished_chunks'] = manifest['finished_frames']

        if 'type' not in manifest:
            new_manifest['type'] = {'id': 'text', 'name': 'Text'}

        manifest['package_version'] = Manifest.LATEST_VERSION

        return new_manifest

    @staticmethod
    def create_manifest_from_repo_name_and_files(repo_name, files):
        manifest = Manifest()
        if '_' in repo_name:
            parts = repo_name.split('_')
        else:
            parts = repo_name.split('-')

        for i, part in iteritems(parts):
            languages = Language.load_languages()
            langs = [x for x in languages if x.lc == part]
            if len(langs):
                lang = langs[0]
                manifest.target_language['id'] = lang.lc
                manifest.target_language['name'] = lang.ln
                manifest.target_language['direction'] = lang.ld
            del parts[i]
            break

        for part in parts:
            if part.lower() == 'obs':
                manifest.resource['id'] = 'obs'
                manifest.resource['name'] = 'Open Bible Stories'
                manifest.format = 'markdown'
                break
            if part.lower() == 'ulb':
                manifest.resource['id'] = 'ulb'
                manifest.resource['name'] = 'Unlocked Literal Bible'
                manifest.format = 'usfm'
                break
            if part.lower() == 'udb':
                manifest.resource['id'] = 'udb'
                manifest.resource['name'] = 'Unlocked Dynamic Bible'
                manifest.format = 'usfm'
                break
            if part.lower() in bible_books.BOOK_NAMES:
                manifest.project['id'] = part.lower()
                manifest.project['name'] = bible_books.BOOK_NAMES[part.lower()]
                manifest.format = 'usfm'
                if not manifest.resource['id']:
                    manifest.resource['id'] = 'bible'
                    manifest.resource['name'] = 'Bible'
        if manifest.format != 'usfm':
            for path in files:
                _, extension = os.path.splitext(path)
                if extension == '.usfm':
                    manifest.format = 'usfm'
                break
