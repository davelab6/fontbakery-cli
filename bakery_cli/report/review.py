# coding: utf-8
# Copyright 2013 The Font Bakery Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# See AUTHORS.txt for the list of Authors and LICENSE.txt for the License.
from __future__ import print_function

import os.path as op
from markdown import markdown

from bakery_cli.report import utils as report_utils
from bakery_cli.utils import UpstreamDirectory

from bakery_lint.metadata import Metadata

from fontaine.cmap import Library
from fontaine.font import FontFactory


TAB = 'Review'
TEMPLATE_DIR = op.join(op.dirname(__file__), 'templates')

t = lambda templatefile: op.join(TEMPLATE_DIR, templatefile)


def get_orthography(fontaineFonts):
    library = Library(collections=['subsets'])
    result = []
    for font, fontaine in fontaineFonts:
        for f1, f2, f3, f4 in fontaine.get_orthographies(_library=library):
            result.append([font, f1, f2, f3, f4])
    return sorted(result, key=lambda x: x[3], reverse=True)


def get_weight_name(value):
    return {
        100: 'Thin',
        200: 'ExtraLight',
        300: 'Light',
        400: '',
        500: 'Medium',
        600: 'SemiBold',
        700: 'Bold',
        800: 'ExtraBold',
        900: 'Black'
    }.get(value, '')


def generate(config, outfile='review.html'):
    directory = UpstreamDirectory(config['path'])
    fonts = [(path, FontFactory.openfont(op.join(config['path'], path)))
             for path in directory.BIN]

    metadata_file = open(op.join(config['path'], 'METADATA.json')).read()
    family_metadata = Metadata.get_family_metadata(metadata_file)
    faces = []
    for f in family_metadata.fonts:
        faces.append({'name': f.full_name,
                      'basename': f.post_script_name,
                      'path': f.filename,
                      'meta': f})

    destfile = open(op.join(config['path'], 'review.html'), 'w')
    app_version = report_utils.git_info(config)
    print(report_utils.render_template(
        outfile, fonts=faces, markdown=markdown, current_page=outfile,
        get_weight_name=get_weight_name,
        build_repo_url=report_utils.build_repo_url, app_version=app_version,
        get_orthography=get_orthography, fontaineFonts=fonts), file=destfile)
