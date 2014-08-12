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
import os.path as op

from bakery_cli.system import run, shutil as shellutil


class TTFAutoHint(object):

    def __init__(self, bakery):
        self.project_root = bakery.project_root
        self.builddir = bakery.build_dir
        self.bakery = bakery

    def execute(self, pipedata, prefix=""):
        """ Run ttfautohint with project command line settings

        For each ttf file in result src folder, outputting them in
        the _out root, or just copy the ttfs there.
        """
        # $ ttfautohint -l 7 -r 28 -G 0 -x 13 -w "" \
        #               -W -c original_font.ttf final_font.ttf
        params = pipedata.get('ttfautohint', '')
        if not params:
            return pipedata

        task = self.bakery.logging_task('Autohint TTFs (ttfautohint)')

        if self.bakery.forcerun:
            return

        if 'autohinting_sizes' not in pipedata:
            pipedata['autohinting_sizes'] = []

        is_failed = False
        for filepath in pipedata['bin_files']:
            filepath = op.join(self.project_root,
                               self.builddir, filepath)
            cmd = ("ttfautohint {params} {source}"
                   " '{name}.autohint.ttf'").format(params=params.strip(),
                                                    name=filepath[:-4],
                                                    source=filepath)
            try:
                run(cmd, cwd=self.builddir, log=self.bakery.log)
            except:
                self.bakery.logging_err('TTFAutoHint is not available')
                self.bakery.logging_task_done(task, failed=True)
                is_failed = True
                break
            pipedata['autohinting_sizes'].append({
                'fontname': op.basename(filepath),
                'origin': op.getsize(filepath),
                'processed': op.getsize(filepath[:-4] + '.autohint.ttf')
            })
            # compare filesizes TODO print analysis of this :)
            comment = "# look at the size savings of that subset process"
            cmd = "ls -l %s.*ttf %s" % (filepath[:-4], comment)
            run(cmd, cwd=self.builddir, log=self.bakery.log)
            shellutil.move(filepath[:-4] + '.autohint.ttf', filepath,
                           log=self.bakery.log)

        if not is_failed:
            self.bakery.logging_task_done(task)
        return pipedata
