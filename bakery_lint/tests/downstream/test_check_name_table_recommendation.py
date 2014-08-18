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
from bakery_lint.base import BakeryTestCase as TestCase
from bakery_cli.ttfont import Font


class CheckStyleNameRecommendation(TestCase):

    targets = ['result']
    tool = 'lint'
    name = __name__
    path = '.'

    def test_check_stylename_is_under_recommendations(self):
        """ Style name must be equal to one of the following four
            values: “Regular”, “Italic”, “Bold” or “Bold Italic” """
        font = Font.get_ttfont(self.path)
        self.assertIn(font.stylename, ['Regular', 'Italic',
                                       'Bold', 'Bold Italic'])


class CheckOTFamilyNameRecommendation(TestCase):

    targets = ['result']
    tool = 'lint'
    name = __name__
    path = '.'

    def test_check_opentype_familyname(self):
        """ OT Family Name for Windows should be equal to Family Name """
        font = Font.get_ttfont(self.path)
        self.assertEqual(font.ot_family_name, font.familyname)


class CheckOTStyleNameRecommendation(TestCase):

    targets = ['result']
    tool = 'lint'
    name = __name__
    path = '.'

    def test_check_opentype_stylename(self):
        """ Style name matches Windows-only Opentype-specific StyleName """
        stylename_mapping = {
            'Regular': ['Thin', 'Light', 'Extra Light', 'Regular',
                        'Medium', 'SemiBold', 'Extra Bold', 'Black'],
            'Italic': ['Thin Italic', 'Extra Light Italic', 'Italic',
                       'Medium Italic', 'SemiBold Italic', 'Extra Bold Italic',
                       'Black Italic'],
            'Bold': ['Bold'],
            'Bold Italic': ['Bold Italic']
        }

        font = Font.get_ttfont(self.path)
        self.assertIn(font.stylename, stylename_mapping)
        self.assertIn(font.ot_style_name, stylename_mapping[font.stylename])
