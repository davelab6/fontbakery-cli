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
import magic
import os

from bakery_lint.base import BakeryTestCase as TestCase, tags, autofix
from bakery_cli.ttfont import Font


class CheckFsTypeIsNotSet(TestCase):

    name = __name__
    targets = ['result']
    tool = 'lint'

    @tags('required')
    @autofix('bakery_cli.pipe.autofix.fix_fstype_to_zero', always_run=True)
    def test_is_fstype_not_set(self):
        """ Is the OS/2 table fsType set to 0? """
        font = Font.get_ttfont(self.operator.path)
        self.assertEqual(font.OS2_fsType, 0)


class CheckFontAgreements(TestCase):

    name = __name__
    targets = ['result']
    tool = 'lint'

    def setUp(self):
        self.font = Font.get_ttfont(self.operator.path)

    @tags('required')
    def test_em_is_1000(self):
        """ Font em should be equal 1000 """
        self.assertEqual(self.font.get_upm_height(), 1000)

    @tags('required')
    def test_latin_file_exists(self):
        """ Check latin subset font file exists """
        path = os.path.dirname(self.operator.path)
        path = os.path.join(path, self.operator.path[:-3] + "latin")
        self.assertTrue(os.path.exists(path))

    @tags('required')
    def test_file_is_font(self):
        """ Menu file have font-name-style.menu format """
        self.assertTrue(magic.from_file(self.operator.path), 'TrueType font data')

    @tags('required')
    def test_font_is_font(self):
        """ File provided as parameter is TTF font file """
        self.assertTrue(magic.from_file(self.operator.path, mime=True),
                        'application/x-font-ttf')
