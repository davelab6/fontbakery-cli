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
from bakery_cli.report.utils import render_template


TAB = 'METADATA.json'


def generate(config, outfile='metadata.html'):
    if not op.exists(op.join(config['path'], 'METADATA.json')):
        return

    destfile = open(op.join(config['path'], outfile), 'w')

    metadata = open(op.join(config['path'], 'METADATA.json')).read()

    try:
        metadata_new = open(op.join(config['path'], 'METADATA.json.new')).read()
    except (IOError, OSError):
        metadata_new = ''
    print(render_template(outfile, metadata=metadata,
                          metadata_new=metadata_new, markdown=markdown),
          file=destfile)
