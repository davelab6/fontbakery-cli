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

from bakery_cli.system import run, shutil


class Optimize(object):
    """ Run optimization process for font """

    def __init__(self, bakery):
        self.project_root = bakery.project_root
        self.builddir = bakery.build_dir
        self.bakery = bakery

    def execute(self, pipedata):
        task = self.bakery.logging_task('Optimizing TTF')
        if self.bakery.forcerun:
            return

        try:
            for filename in pipedata['bin_files']:
                self.run(filename, pipedata)
            self.bakery.logging_task_done(task)
        except:
            self.bakery.logging_task_done(task, failed=True)
            raise

    def run(self, filename, pipedata):
        if 'optimize' in pipedata and not pipedata['optimize']:
            return
        self.bakery.logging_raw('### Optimize TTF {}'.format(filename))

        from fontTools import subset

        args = [op.join(self.builddir, filename), '*']
        args += ['--layout-features=*']
        args += ['--notdef-outline', '--name-IDs=*', '--hinting']
        self.bakery.logging_cmd('pyftsubset %s' % ' '.join(args))

        subset.main(args)

        newsize = os.stat(op.join(self.builddir, filename + '.subset')).st_size
        origsize = os.stat(op.join(self.builddir, filename)).st_size

        # compare filesizes TODO print analysis of this :)
        comment = "# look at the size savings of that subset process"
        self.bakery.logging_cmd("ls -l '%s'* %s" % (filename, comment))

        statusmessage = "{0}.subset: {1} bytes\n{0}: {2} bytes\n"
        self.bakery.logging_raw(statusmessage.format(filename, newsize, origsize))

        # move ttx files to src
        shutil.move(op.join(self.builddir, filename + '.subset'),
                    op.join(self.builddir, filename),
                    log=self.bakery.log)
