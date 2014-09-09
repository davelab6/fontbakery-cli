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
from bakery_cli.scripts import encode_glyphs


PYPATH = ''


def replace_origfont(testcase):
    targetpath = testcase.operator.path
    command = "$ mv {0}.fix {0}".format(targetpath)
    if hasattr(testcase, 'operator'):
        testcase.operator.debug(command)
    fixed_font_path = '{}.fix'.format(targetpath)
    if op.exists(fixed_font_path):
        shutil.move(fixed_font_path, targetpath)


def dsig_signature(testcase):
    """ Create "DSIG" table with default signaturerecord """
    targetpath = testcase.operator.path

    SCRIPTPATH = 'bakery-dsig.py'

    command = "$ {0} {1}".format(SCRIPTPATH, targetpath)
    if hasattr(testcase, 'operator'):
        testcase.operator.debug(command)

    dsig.create(targetpath)

    replace_origfont(testcase)


def gaspfix(testcase):
    """ Set in "gasp" table value of key "65535" to "15" """
    targetpath = testcase.operator.path

    SCRIPTPATH = 'bakery-gasp.py'

    command = "$ {0} --set={1} {2}".format(SCRIPTPATH, 15, targetpath)
    if hasattr(testcase, 'operator'):
        testcase.operator.debug(command)

    gasp.set(targetpath, 15)

    replace_origfont(testcase)


def fix_opentype_specific_fields(testcase):
    """ Fix Opentype-specific fields in "name" table """
    targetpath = testcase.operator.path
    SCRIPTPATH = 'bakery-opentype-fix.py'

    command = "$ {0} {1} {2}".format(PYPATH, SCRIPTPATH, targetpath)
    if hasattr(testcase, 'operator'):
        testcase.operator.debug(command)

    opentype.fix(targetpath)

    replace_origfont(testcase)


def fix_nbsp(testcase):
    """ Fix width for space and nbsp """
    targetpath = testcase.operator.path

    SCRIPTPATH = 'bakery-nbsp-fix.py'

    command = "$ {0} {1} {2}".format(PYPATH, SCRIPTPATH, targetpath)
    if hasattr(testcase, 'operator'):
        testcase.operator.debug(command)
    checkAndFix(targetpath)

    replace_origfont(testcase)


def fix_metrics(testcase):
    """ Fix vmet table with actual min and max values """
    targetpath = testcase.operator.path
    SCRIPTPATH = 'bakery-vmet-fix.py'

    from bakery_lint.metadata import FamilyMetadata
    family_metadata = FamilyMetadata(json.load(open(targetpath)))

    paths = []
    for f in family_metadata.fonts:
        path = op.join(op.dirname(targetpath), f.filename)
        paths.append(path)

    command = "$ {0} {1} --autofix {2}"
    command = command.format(PYPATH, SCRIPTPATH, ' '.join(paths))
    if hasattr(testcase, 'operator'):
        testcase.operator.debug(command)

    metricfix(paths)

    for path in paths:
        shutil.move(path + '.fix', path, log=testcase.operator.logger)

    command = "$ {0} {1} {2}".format(PYPATH, SCRIPTPATH, ' '.join(paths))
    if hasattr(testcase, 'operator'):
        testcase.operator.debug(command)
        testcase.operator.debug(metricview(paths))


def fix_name_ascii(testcase):
    """ Replacing non ascii names in copyright """
    targetpath = testcase.operator.path

    SCRIPTPATH = 'bakery-ascii-fix.py'
    command = "$ {0} {1} {2}".format(PYPATH, SCRIPTPATH, targetpath)
    if hasattr(testcase, 'operator'):
        testcase.operator.debug(command)

    fix_name_table(targetpath)
    shutil.move(targetpath + '.fix', targetpath,
                log=testcase.operator.logger)


def fix_fstype_to_zero(testcase):
    """ Fix fsType to zero """
    targetpath = testcase.operator.path

    SCRIPTPATH = 'bakery-fstype-fix.py'
    command = "$ {0} {1} --autofix {2}".format(PYPATH, SCRIPTPATH, targetpath)
    if hasattr(testcase, 'operator'):
        testcase.operator.debug(command)

    reset_fstype(targetpath)
    shutil.move(targetpath + '.fix', targetpath,
                log=testcase.operator.logger)


def fix_encode_glyphs(testcase):
    targetpath = testcase.operator.path
    SCRIPTPATH = 'bakery-encode-glyphs-fix.py'
    command = "$ {0} {1} --autofix {2}".format(PYPATH, SCRIPTPATH, targetpath)
    if hasattr(testcase, 'operator'):
        testcase.operator.debug(command)

    encode_glyphs.add_spua_by_glyph_id_mapping_to_cmap(
        testcase.ttx, targetpath, testcase.unencoded_glyphs)
    if testcase.unencoded_glyphs:
        shutil.move(targetpath + '.fix', targetpath,
                    log=testcase.operator.logger)


def rename(testcase):
    targetpath = testcase.operator.path

    new_targetpath = op.join(op.dirname(targetpath),
                             testcase.expectedfilename)
    shutil.move(targetpath, new_targetpath, log=testcase.operator.logger)

    testcase.operator.path = new_targetpath
