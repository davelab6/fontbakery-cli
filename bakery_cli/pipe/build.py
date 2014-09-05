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
import os
import os.path as op

from fontTools import ttx

from bakery_cli.scripts.font2ttf import convert
from bakery_cli.system import prun, shutil as shellutil
from bakery_cli.utils import UpstreamDirectory


class Build(object):

    def __init__(self, bakery):
        self.project_root = bakery.project_root
        self.builddir = bakery.build_dir
        self.bakery = bakery

    def otf2ttf(self, filepath):
        fontname = filepath[:-4]

        _ = 'font2ttf.py {0}.otf {0}.ttf\n'
        self.bakery.logging_cmd(_.format(fontname))

        path = '{}.otf'.format(fontname)
        if op.exists(op.join(self.builddir, path)):
            try:
                ttfpath = '{}.ttf'.format(fontname)
                convert(op.join(self.builddir, path),
                        op.join(self.builddir, ttfpath), log=self.bakery.log)
                os.remove(op.join(self.builddir, path))
            except Exception, ex:
                self.bakery.logging_err(ex.message)
                raise

    def movebin_to_builddir(self, files):
        result = []
        for a in files:
            d = op.join(self.builddir, op.basename(a)[:-4] + '.ttf')
            s = op.join(self.builddir, a[:-4] + '.ttf')

            try:
                shellutil.move(s, d, log=self.bakery.log)
                result.append(op.basename(a)[:-4] + '.ttf')
            except:
                pass
        return result

    def print_vertical_metrics(self, binfiles):
        SCRIPTPATH = 'bakery-vmet-fix.py'
        command = ' '.join([op.join(self.builddir, x) for x in binfiles])
        prun('%s %s' % (SCRIPTPATH, command), cwd=op.dirname(__file__),
             log=self.bakery.log)

    def execute(self, pipedata, prefix=""):
        task = self.bakery.logging_task('Convert sources to TTF')
        if self.bakery.forcerun:
            return

        directory = UpstreamDirectory(op.join(self.builddir, 'sources'))
        self.bakery.logging_task('{}'.format(directory.get_ttx()))
        try:
            if directory.get_ttx():
                self.execute_ttx([op.join('sources', x) for x in directory.get_ttx()])
            if directory.UFO:
                self.execute_ufo_sfd([op.join('sources', x) for x in directory.UFO])
            if directory.SFD:
                self.execute_ufo_sfd([op.join('sources', x) for x in directory.SFD])
            if directory.BIN:
                self.execute_bin([op.join('sources', x) for x in directory.BIN])

            binfiles = self.movebin_to_builddir([op.join('sources', x) for x in directory.ALL_FONTS])

            self.print_vertical_metrics(binfiles)

            pipedata['bin_files'] = binfiles
        except:
            self.bakery.logging_task_done(task, failed=True)
            raise

        self.bakery.logging_task_done(task)
        return pipedata

    def execute_ttx(self, files):
        paths = []
        for f in files:
            f = op.join(self.builddir, f)
            paths.append(f)

        self.bakery.logging_cmd('ttx %s' % ' '.join(paths))
        ttx.main(paths)

        for p in files:
            self.otf2ttf(p)

    def execute_ufo_sfd(self, files):
        for f in files:
            filepath = op.join(self.builddir, f)
            _ = 'font2ttf.py %s %s'
            self.bakery.logging_cmd(_ % (filepath,
                                         filepath[:-4] + '.ttf'))
            ttfpath = filepath[:-4] + '.ttf'

            try:
                convert(op.join(self.builddir, filepath),
                        op.join(self.builddir, ttfpath), log=self.bakery.log)
            except Exception, ex:
                self.bakery.logging_err(ex.message)
                raise

    def execute_bin(self, files):
        for p in files:
            if p.endswith('.otf'):
                self.otf2ttf(p)
