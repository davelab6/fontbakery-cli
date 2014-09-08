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
import fnmatch
import os

import quadopt
from fontcrunch import fontcrunch

from bakery_cli.system import shutil


class FontCrunch(object):

    def __init__(self, bakery):
        self.project_root = bakery.project_root
        self.builddir = bakery.build_dir
        self.bakery = bakery

    def _quadopt_optimize(self, bez_dir):
        pattern = '*.bez'
        for root, dirs, files in os.walk(bez_dir):
            for filename in fnmatch.filter(files, pattern):
                fn = os.path.join(root, filename)
                print('Optimize: {}'.format(fn))
                quadopt.optimize_run(fn, fn + 'opt')

    def run(self, filename, pipedata):
        if not pipedata.get('fontcrunch'):
            return  # run fontcrunch only if user set flag in config
        filename = os.path.join(self.builddir, filename)
        self.bakery.logging_raw('### Foncrunch {}\n'.format(filename))
        bez_dir = os.path.join(self.builddir, 'bez')
        os.chdir(self.builddir)
        fontcrunch.generate(filename)
        self._quadopt_optimize(bez_dir)
        fontcrunch.repack(filename, '{}.crunched'.format(filename))
        shutil.move('{}.crunched'.format(filename), filename)
        return 1

    def execute(self, pipedata):
        if not pipedata.get('fontcrunch'):
            return  # run fontcrunch only if user set flag in config
        task = self.bakery.logging_task('Foncrunching TTF')
        if self.bakery.forcerun:
            return

        bez_dir = os.path.join(self.builddir, 'bez')
        try:
            for filename in [os.path.join(self.builddir, x) \
                             for x in pipedata['bin_files']]:
                self.run(filename, pipedata)
            self.bakery.logging_task_done(task)
        except:
            self.bakery.logging_task_done(task, failed=True)
            raise
        finally:
            shutil.rmtree(bez_dir)
