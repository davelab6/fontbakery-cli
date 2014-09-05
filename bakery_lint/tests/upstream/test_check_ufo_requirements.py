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

from bakery_lint.base import BakeryTestCase as TestCase

import robofab.world
import robofab.objects


class UfoOpenTest(TestCase):
    targets = ['upstream']
    tool = 'Robofab'
    name = __name__

    def setUp(self):
        self.font = robofab.world.OpenFont(self.operator.path)
        # You can use ipdb here to interactively develop tests!
        # Uncommand the next line, then at the iPython prompt: print(self.operator.path)
        # import ipdb; ipdb.set_trace()

    def test_it_exists(self):
        """ Does this UFO path exist? """
        self.assertEqual(os.path.exists(self.operator.path), True)

    def test_is_folder(self):
        """ Is this UFO really a folder?"""
        self.assertEqual(os.path.isdir(self.operator.path), True)

    def test_is_ended_ufo(self):
        """ Does this font file's name end with '.ufo'?"""
        self.assertEqual(self.operator.path.lower().endswith('.ufo'), True)

    # @tags('required')
    def test_is_A(self):
        """ Does this font have a glyph named 'A'?"""
        self.assertTrue('A' in self.font)

    def test_is_A_a_glyph_instance(self):
        """ Is this font's property A an instance of an RGlyph object? """
        if 'A' in self.font:
            a = self.font['A']
        else:
            a = None
        self.assertIsInstance(a, robofab.objects.objectsRF.RGlyph)

    def test_is_fsType_eq_1(self):
        """Is the OS/2 table fsType set to 0?"""
        desiredFsType = [0]
        self.assertEqual(self.font.info.openTypeOS2Type, desiredFsType)

    # TODO check if this is a good form of test
    def has_character(self, unicodeString):
        """Does this font include a glyph for the given unicode character?"""
        # TODO check the glyph has at least 1 contour
        character = unicodeString[0]
        glyph = None
        if character in self.font:
            glyph = self.font[character]
        self.assertIsInstance(glyph, robofab.objects.objectsRF.RGlyph)

    def test_has_rupee(self):
        u""" Does this font include a glyph for ₹, the Indian Rupee Sign
             codepoint?"""
        self.has_character(self, u'₹')
