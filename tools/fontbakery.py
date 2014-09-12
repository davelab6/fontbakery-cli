#!/usr/bin/env python
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
import argparse
import multiprocessing
import multiprocessing.pool
import os
import os.path as op
import sys
import yaml

from bakery_cli import pipe
from bakery_cli.bakery import Bakery, BAKERY_CONFIGURATION_DEFAULTS
from bakery_cli.utils import UpstreamDirectory


class DualLog(object):

    def write(self, msg, prefix=u''):
        if prefix:
            msg = prefix + msg
        print(msg.encode('utf8'))


def create_bakery_config(bakery_config_dir, data):
    if not op.exists(bakery_config_dir):
        os.makedirs(bakery_config_dir)

    bakeryyaml = op.abspath(op.join(bakery_config_dir, 'bakery.yaml'))

    l = open(bakeryyaml, 'w')
    l.write(yaml.safe_dump(data))
    l.close()


def find_bakery_config(sourcedir):
    for bakeryfile in ['bakery.yaml', 'bakery.yml']:
        try:
            bakeryyaml = open(op.join(sourcedir, bakeryfile), 'r')
            return yaml.safe_load(bakeryyaml)
        except IOError:
            pass
    return None


def run_bakery(sourcedir):
    sourcedir = op.realpath(sourcedir)
    try:

        config = find_bakery_config(sourcedir)
        if not config:
            config = yaml.safe_load(open(BAKERY_CONFIGURATION_DEFAULTS))

        build_project_dir = op.join(sourcedir, 'builds', 'build')

        if 'process_files' not in config:
            directory = UpstreamDirectory(sourcedir)
            # normalize process_files path
            config['process_files'] = directory.get_fonts()

        create_bakery_config(build_project_dir, config)

        b = Bakery('', sourcedir, 'builds', 'build')
        config = op.join(build_project_dir, 'bakery.yaml')
        b.load_config(config)
        b.run()
    except Exception as ex:
        raise
        print('FAILED: %s' % sourcedir, file=sys.stderr)
        print(ex, file=sys.stderr)
        sys.exit(1)


class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)


# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class Pool(multiprocessing.pool.Pool):

    Process = NoDaemonProcess


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('projectpath', nargs='+',
                        help=("Path to directory with UFO, SFD, TTX, TTF or OTF files"))
    args = parser.parse_args()

    for p in args.projectpath:
        run_bakery(p)

    # pool = Pool(4)

    # pool.map(run_bakery, args.projectpath)
    # pool.close()

    # pool.join()
