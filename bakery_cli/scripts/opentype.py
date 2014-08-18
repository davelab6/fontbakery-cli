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
from bakery_cli.ttfont import Font
from fontTools.ttLib.tables._n_a_m_e import NameRecord


def findOTFamilyName(ttfont):
    for namerec in ttfont['name'].names:
        if (namerec.nameID == 16 and namerec.platformID == 3
                and namerec.langID == 0x409):
            return namerec


def findOTStyleName(ttfont):
    for namerec in ttfont['name'].names:
        if (namerec.nameID == 17 and namerec.platformID == 3
                and namerec.langID == 0x409):
            return namerec


def findOTFullName(ttfont):
    for namerec in ttfont['name'].names:
        if (namerec.nameID == 18 and namerec.platformID == 3
                and namerec.langID == 0x409):
            return namerec


mapping = {
    'Thin': 'Regular',
    'Extra Light': 'Regular',
    'Light': 'Regular',
    'Regular': 'Regular',
    'Medium': 'Regular',
    'SemiBold': 'Regular',
    'Extra Bold': 'Regular',
    'Black': 'Regular',

    'Thin Italic': 'Italic',
    'Extra Italic Light': 'Italic',
    'Light Italic': 'Italic',
    'Italic Italic': 'Italic',
    'Medium Italic': 'Italic',
    'SemiBold Italic': 'Italic',
    'Extra Bold Italic': 'Italic',
    'Black Italic': 'Italic',

    'Bold': 'Bold',
    'Bold Italic': 'Bold Italic'
}


def fix(fontpath):
    ttfont = Font.get_ttfont(fontpath)

    ot_namerecord = findOTFamilyName(ttfont)
    if not ot_namerecord:
        ot_namerecord = NameRecord()
        ot_namerecord.nameID = 16
        ot_namerecord.platformID = 3
        ot_namerecord.langID = 0x409

        # When building a Unicode font for Windows, the platform ID
        # should be 3 and the encoding ID should be 1
        ot_namerecord.platEncID = 1

        ttfont['name'].names.append(ot_namerecord)

    ot_namerecord.string = ttfont.familyname.encode("utf_16_be")

    ot_namerecord = findOTStyleName(ttfont)
    if not ot_namerecord:
        ot_namerecord = NameRecord()
        ot_namerecord.nameID = 17
        ot_namerecord.platformID = 3
        ot_namerecord.langID = 0x409
        # When building a Unicode font for Windows, the platform ID
        # should be 3 and the encoding ID should be 1
        ot_namerecord.platEncID = 1

        ttfont['name'].names.append(ot_namerecord)

    ot_namerecord.string = mapping.get(ttfont.stylename, 'Regular').encode("utf_16_be")

    ot_namerecord = findOTFullName(ttfont)
    if not ot_namerecord:
        ot_namerecord = NameRecord()
        ot_namerecord.nameID = 18
        ot_namerecord.platformID = 3
        ot_namerecord.langID = 0x409
        # When building a Unicode font for Windows, the platform ID
        # should be 3 and the encoding ID should be 1
        ot_namerecord.platEncID = 1

        ttfont['name'].names.append(ot_namerecord)

    ot_namerecord.string = ttfont.fullname.encode("utf_16_be")

    ttfont.save(fontpath + '.fix')
