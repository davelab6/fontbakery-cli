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
import codecs
import os.path as op

from fontaine.cmap import Library
from fontaine.builder import Builder, Director


class PyFontaine(object):

    def __init__(self, bakery):
        self.project_root = bakery.project_root
        self.builddir = bakery.build_dir
        self.bakery = bakery

    def execute(self, pipedata):
        task = self.bakery.logging_task('pyFontaine TTFs')
        if self.bakery.forcerun:
            return

        try:
            library = Library(collections=['subsets'])
            director = Director(_library=library)

            fonts = []
            for font in pipedata['bin_files']:
                fonts.append(op.join(self.builddir, font))

            _ = ('fontaine --collections subsets --text %s'
                 ' > fontaine.txt\n') % ' '.join(fonts)
            self.bakery.logging_cmd(_)

            fontaine_log = op.join(self.builddir, 'fontaine.txt')
            fp = codecs.open(fontaine_log, 'w', 'utf-8')

            result = Builder.text_(director.construct_tree(fonts))
            fp.write(result.output)
            self.bakery.logging_task_done(task)
        except:
            self.bakery.logging_task_done(task, failed=True)
            raise
