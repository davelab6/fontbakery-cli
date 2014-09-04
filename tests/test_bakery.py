import unittest

from mock import patch

from bakery_cli.pipe.copy import Copy
from bakery_cli.pipe.build import Build
from bakery_cli.pipe.rename import Rename
from bakery_cli.bakery import Bakery


class TestBakery(unittest.TestCase):

    def test_copy_process(self):
        pipedata = {'process_files': ['1.in/fontname-bold.ttx'],
                    'builddir': 'build',
                    'project_root': ''}

        b = Bakery('/home/user', 'project', 'out', 'build')

        b = Copy(b)
        with patch.object(b, 'copy_to_builddir') as mock_copy2builddir:
            with patch.object(b, 'create_source_dir') as mock_create_src:
                mock_create_src.return_value = 'sources'
                with patch.object(b, 'copy_helper_files') as mock_copyhf:
                    pipedata = b.execute(pipedata)

                    mock_copy2builddir.assert_called_once_with(['1.in/fontname-bold.ttx'], 'sources')
                    self.assertEqual(pipedata['process_files'], ['sources/fontname-bold.ttx'])
                    self.assert_(mock_copyhf.called)
                    self.assert_(mock_create_src.called)

    def test_copy_with_splitted_ttx(self):
        pipedata = {'process_files': ['1.in/fontname-bold.ttx'],
                    'builddir': 'build',
                    'project_root': ''}

        b = Bakery('/home/user', 'project', 'out', 'build')

        b = Copy(b)
        with patch.object(b, 'copy_to_builddir') as copy2builddir:
            with patch.object(b, 'lookup_splitted_ttx') as splitted_ttx:
                with patch.object(b, 'create_source_dir') as mock_create_src:
                    mock_create_src.return_value = 'sources'
                    with patch.object(b, 'copy_helper_files') as mock_copyhf:
                        splitted_ttx.return_value = ['1.in/fontname-bold._g_p_o_s.ttx']

                        pipedata = b.execute(pipedata)

                        copy2builddir.assert_called_once_with(['1.in/fontname-bold.ttx',
                                                               '1.in/fontname-bold._g_p_o_s.ttx'], 'sources')
                        self.assertEqual(pipedata['process_files'], ['sources/fontname-bold.ttx'])
                        self.assert_(mock_create_src.called)
                        self.assert_(mock_copyhf.called)

    def test_convert(self):
        pipedata = {'process_files': ['sources/fontname-bold.ttx',
                                      'sources/fontname-regular.ttx'],
                    'project_root': '',
                    'builddir': 'build'}

        b = Bakery('/home/user', 'project', 'out', 'build')

        b = Build(b)
        with patch.object(b, "execute_ttx") as ttx_call:
            with patch.object(b, "movebin_to_builddir") as move:
                move.return_value = ['fontname-bold.ttf',
                                     'fontname-regular.ttf']
                pipedata = b.execute(pipedata)

                ttx_call.assert_called_once_with(['sources/fontname-bold.ttx',
                                                  'sources/fontname-regular.ttx'])
                self.assertEqual(pipedata['bin_files'],
                                 ['fontname-bold.ttf', 'fontname-regular.ttf'])
                move.assert_called_once_with(['sources/fontname-bold.ttx',
                                              'sources/fontname-regular.ttx'])

    def test_rename(self):
        pipedata = {'bin_files': ['sources/fontname-bold.ttf']}

        b = Bakery('', '', '', '')

        b = Rename(b)

        with patch.object(b, 'get_psname') as getpsname:
            with patch('bakery_cli.system.shutil.move'):
                with patch('fontTools.ttLib.TTFont') as TTFont:
                    TTFont.return_value = ''
                    getpsname.return_value = 'fontname-regular.ttf'
                    b.execute(pipedata)
                    # move.assert_called_once_with('sources/fontname-bold.ttf',
                    #                              'sources/fontname-regular.ttf',
                    #                              log=bakery_cli.system.stdoutlog)
        self.assertEqual(pipedata['bin_files'], ['sources/fontname-regular.ttf'])
