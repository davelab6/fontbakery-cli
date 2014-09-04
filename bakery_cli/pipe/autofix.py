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
import json
import os.path as op
import yaml

from bakery_cli.system import shutil

from bakery_cli.scripts.vmet import metricview, metricfix
from bakery_cli.scripts.ascii import fix_name_table
from bakery_cli.scripts.fstype import reset_fstype
from bakery_cli.scripts.nbsp import checkAndFix
from bakery_cli.scripts import opentype
from bakery_cli.scripts import gasp
from bakery_cli.scripts import dsig


PYPATH = ''


def replace_origfont(testcase):
    command = "$ mv {0}.fix {0}".format(testcase.path)
    if hasattr(testcase, 'logging'):
        testcase.logging.write(command)
    shutil.move(testcase.path + '.fix', testcase.path)


def dsig_signature(testcase):
    """ Create "DSIG" table with default signaturerecord """
    SCRIPTPATH = 'bakery-dsig.py'

    command = "$ {0} {1}".format(SCRIPTPATH, testcase.path)
    if hasattr(testcase, 'logging'):
        testcase.logging.write(command)

    dsig.create(testcase.path)

    replace_origfont(testcase)


def gaspfix(testcase):
    """ Set in "gasp" table value of key "65535" to "15" """
    SCRIPTPATH = 'bakery-gasp.py'

    command = "$ {0} --set={1} {2}".format(SCRIPTPATH, 15, testcase.path)
    if hasattr(testcase, 'logging'):
        testcase.logging.write(command)

    gasp.set(testcase.path, 15)

    replace_origfont(testcase)


def fix_opentype_specific_fields(testcase):
    """ Fix Opentype-specific fields in "name" table """
    SCRIPTPATH = 'bakery-opentype-fix.py'

    command = "$ {0} {1} {2}".format(PYPATH, SCRIPTPATH, testcase.path)
    if hasattr(testcase, 'logging'):
        testcase.logging.write(command)

    opentype.fix(testcase.path)

    replace_origfont(testcase)


def fix_nbsp(testcase):
    """ Fix width for space and nbsp """
    SCRIPTPATH = 'bakery-nbsp-fix.py'

    command = "$ {0} {1} {2}".format(PYPATH, SCRIPTPATH, testcase.path)
    if hasattr(testcase, 'logging'):
        testcase.logging.write(command)
    checkAndFix(testcase.path)

    replace_origfont(testcase)


def fix_metrics(testcase):
    """ Fix vmet table with actual min and max values """
    SCRIPTPATH = 'bakery-vmet-fix.py'

    from bakery_lint.metadata import FamilyMetadata
    family_metadata = FamilyMetadata(json.load(open(testcase.path)))

    paths = []
    for f in family_metadata.fonts:
        path = op.join(op.dirname(testcase.path), f.filename)
        paths.append(path)

    command = "$ {0} {1} --autofix {2}"
    command = command.format(PYPATH, SCRIPTPATH, ' '.join(paths))
    if hasattr(testcase, 'logging'):
        testcase.logging.write(command)

    metricfix(paths)

    for path in paths:
        shutil.move(path + '.fix', path, log=testcase.logging)

    command = "$ {0} {1} {2}".format(PYPATH, SCRIPTPATH, ' '.join(paths))
    testcase.logging.write(command)
    testcase.logging.write(metricview(paths))


def fix_name_ascii(testcase):
    """ Replacing non ascii names in copyright """
    SCRIPTPATH = 'bakery-ascii-fix.py'
    command = "$ {0} {1} {2}".format(PYPATH, SCRIPTPATH, testcase.path)
    if hasattr(testcase, 'logging'):
        testcase.logging.write(command)
    fix_name_table(testcase.path)
    shutil.move(testcase.path + '.fix', testcase.path, log=testcase.logging)


def fix_fstype_to_zero(testcase):
    """ Fix fsType to zero """
    SCRIPTPATH = 'bakery-fstype-fix.py'
    command = "$ {0} {1} --autofix {2}".format(PYPATH, SCRIPTPATH, testcase.path)
    if hasattr(testcase, 'logging'):
        testcase.logging.write(command)
    reset_fstype(testcase.path)
    shutil.move(testcase.path + '.fix', testcase.path, log=testcase.logging)
