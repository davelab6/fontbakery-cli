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
import importlib
import unittest

from itertools import chain


class TestRegistry(object):
    """ Singleton class to collect all available tests """
    tests = []

    @classmethod
    def register(cls, test):
        if not test in TestRegistry.tests:
            TestRegistry.tests.append(test)

    @classmethod
    def list(cls):
        return TestRegistry.tests


class MetaTest(type):
    """
    Class for all tests
    """
    def __new__(mcs, name, bases, attrs):
        abstract = attrs.pop('__abstract__', None)
        for x in attrs.keys():
            if x.startswith('test_'):
                if not hasattr(attrs[x], 'tags'):
                    attrs[x].tags = ['note', ]
        newbornclass = super(MetaTest, mcs).__new__(mcs, name, bases, attrs)
        if not abstract:
            TestRegistry.register(newbornclass)
        return newbornclass


class BakeryTestCase(unittest.TestCase):
    __metaclass__ = MetaTest
    # because we don't want to register this base class as test case
    __abstract__ = True


class BakeryTestResult(unittest.TestResult):

    def __init__(self, stream=None, descriptions=None, verbosity=None,
                 success_list=None, error_list=None, failure_list=None):
        self.sl = success_list
        self.el = error_list
        self.fl = failure_list
        super(BakeryTestResult, self).__init__(self)

    def callmethod(self, methodname, test):
        pkg = '.'.join(methodname.split('.')[:-1])
        mod = importlib.import_module(pkg)
        getattr(mod, methodname.split('.')[-1])(test)

    def startTest(self, test):
        super(BakeryTestResult, self).startTest(test)

    def addSuccess(self, test):
        super(BakeryTestResult, self).addSuccess(test)
        if hasattr(self.sl, 'append'):
            self.sl.append(test)

        if hasattr(test, 'logging'):
            test.logging.write('... {} .. OK'.format(test.id()))

        test_method = getattr(test, test._testMethodName)
        if hasattr(test_method, 'autofix'):
            if getattr(test_method, 'autofix_always_run', False):
                self.callmethod(test_method.autofix_method, test)

    def addError(self, test, err):
        super(BakeryTestResult, self).addError(test, err)
        _, _err_exception, _ = err
        test._err = err
        test._err_msg = _err_exception.message
        if hasattr(self.el, 'append'):
            self.el.append(test)

        if hasattr(test, 'logging'):
            test.logging.write('... {} .. ERROR'.format(test.id()))

    def addFailure(self, test, err):
        super(BakeryTestResult, self).addFailure(test, err)
        _, _err_exception, _ = err
        test._err = err
        test._err_msg = _err_exception.message
        if hasattr(self.fl, 'append'):
            self.fl.append(test)

        if hasattr(test, 'logging'):
            test.logging.write('... {} .. FAIL'.format(test.id()))

        test_method = getattr(test, test._testMethodName)
        if hasattr(test_method, 'autofix'):
            self.callmethod(test_method.autofix_method, test)


class BakeryTestRunner(unittest.TextTestRunner):
    def __init__(self, descriptions=True, verbosity=1, resultclass=None,
                 success_list=None, error_list=None, failure_list=None):

        self.sl = success_list
        self.el = error_list
        self.fl = failure_list

        self.results = []
        self.descriptions = descriptions
        self.verbosity = verbosity
        if resultclass is not None:
            self.resultclass = resultclass
        super(BakeryTestRunner, self).__init__(self)

    def _makeResult(self):
        return self.resultclass(self.stream, self.descriptions,
                                self.verbosity, self.sl, self.el, self.fl)

    def run(self, test):
        "Run the given test case or test suite."
        result = self._makeResult()
        test(result)
        self.results.append(result)
        return result


class tags(object):
    """ Decorator that allow to add .tags property to function. Usefull
    to tag tests. `MetaTest` already implement support for functions with names
    starting with 'test_'. Tags can be used in UI or other ways.

    Example:

    class SimpleTest(BakeryTestCase):
        @tags('important', 'latin-set')
        def test_subset_latin_chars(self):
            ''' Important test that check latin subset char set '''
            self.assertTrue(True) # your test code here

    """

    def __init__(self, *args):
        self.tags = args

    def __call__(self, f):
        f.tags = self.tags
        return f


class autofix(object):

    def __init__(self, methodname, always_run=False):
        self.methodname = methodname
        self.always_run = always_run

    def __call__(self, f):
        f.autofix = True
        f.autofix_method = self.methodname
        f.autofix_always_run = self.always_run
        return f


def make_suite(path, definedTarget, test_method=None, log=None):
    """ path - is full path to file,
        definedTarget is filter to only select small subset of tests
    """
    suite = unittest.TestSuite()
    for TestCase in TestRegistry.list():
        if definedTarget in TestCase.targets:
            TestCase.path = path
            TestCase.logging = log
            if getattr(TestCase, '__generateTests__', None):
                TestCase.__generateTests__()

            for test in unittest.defaultTestLoader.loadTestsFromTestCase(TestCase):
                if test_method and test_method != test._testMethodName:
                    continue
                suite.addTest(test)

    return suite


def run_suite(suite):
    result = {
        'success': [],
        'error': [],
        'failure': []
    }
    runner = BakeryTestRunner(resultclass=BakeryTestResult,
                              success_list=result['success'],
                              error_list=result['error'],
                              failure_list=result['failure'])
    runner.run(suite)
    result['sum'] = sum([len(result[x]) for x in result.keys()])

    check = lambda x: 'required' in getattr(x, x._testMethodName).tags
    # assume that `error` test are important even if they are broken
    if not any([check(i) for i in chain(result.get('failure', []), result.get('error', []))]):
        result['passed'] = True
    else:
        result['passed'] = False

    # on next step here will be runner object
    return result


def tests_report():
    """ Small helper to make test report """
    f = lambda x: True if x.startswith('test') else False
    m = []
    for x in TestRegistry.list():
        m.extend([getattr(x, i) for i in filter(f, dir(x))])

    for i in m:
        print("%s,\"%s\",\"%s\"" % (
            str(i).replace('<unbound method ', '').replace('>', ''),
            ", ".join(i.tags),
            " ".join(unicode(i.__doc__).replace("\n", '').replace('"', "'").split())))
