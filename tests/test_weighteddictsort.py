import unittest

from bakery_cli.utils import weighted_dict_sort


input_array = [
    {
        'name': 'Catcher',
        'tests': [
            {'status': 'OK'},
            {'status': 'OK'},
            {'status': 'FAIL'},
            {'status': 'FIXED'}
        ]
    },
    {
        'name': 'Printer',
        'tests': [
            {'status': 'ERROR'},
            {'status': 'FAIL'},
            {'status': 'FAIL'}
        ]
    },
    {
        'name': 'Mock',
        'tests': [
            {'status': 'OK'},
            {'status': 'FAIL'},
            {'status': 'FAIL'},
            {'status': 'FIXED'}
        ]
    },
    {
        'name': 'Look',
        'tests': [
            {'status': 'OK'},
            {'status': 'OK'}
        ]
    },
    {
        'name': 'Flood',
        'tests': [
            {'status': 'OK'},
            {'status': 'OK'},
            {'status': 'FIXED'},
            {'status': 'FIXED'}
        ]
    },
    {
        'name': 'Click',
        'tests': [
            {'status': 'OK'},
            {'status': 'FAIL'},
            {'status': 'FIXED'},
            {'status': 'FIXED'}
        ]
    }
]


result_array = [
    {
        'name': 'Printer',
        'tests': [
            {'status': 'ERROR'},
            {'status': 'FAIL'},
            {'status': 'FAIL'}
        ]
    },
    {
        'name': 'Mock',
        'tests': [
            {'status': 'OK'},
            {'status': 'FAIL'},
            {'status': 'FAIL'},
            {'status': 'FIXED'}
        ]
    },
    {
        'name': 'Click',
        'tests': [
            {'status': 'OK'},
            {'status': 'FAIL'},
            {'status': 'FIXED'},
            {'status': 'FIXED'}
        ]
    },
    {
        'name': 'Catcher',
        'tests': [
            {'status': 'OK'},
            {'status': 'OK'},
            {'status': 'FAIL'},
            {'status': 'FIXED'}
        ]
    },
    {
        'name': 'Flood',
        'tests': [
            {'status': 'OK'},
            {'status': 'OK'},
            {'status': 'FIXED'},
            {'status': 'FIXED'}
        ]
    },
    {
        'name': 'Look',
        'tests': [
            {'status': 'OK'},
            {'status': 'OK'}
        ]
    }
]


class TestWeightedDictSort(unittest.TestCase):

    def test_weighted_dict_sort(self):
        self.assertEqual(weighted_dict_sort(input_array), result_array)
