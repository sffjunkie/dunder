# Copyright 2009-2014, Simon Kennedy, sffjunkie+code@gmail.com

import io
import re
import sys
import os.path
from setuptools import setup
from setuptools.command.test import test as TestCommand

this_dir = os.path.dirname(__file__)
src_dir = os.path.join(this_dir, 'src')
sys.path.append(src_dir)

import dunder
data = dunder.parse(os.path.join(src_dir, 'dunder.py'))

author_email = data.get('__email__', None)
if not author_email:
    m = re.match(r'(?P<name>[\w\s]+)(?:<(?P<email>[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})>)?',
                 data['__author__'],
                 flags=re.IGNORECASE)
    g = m.groups()
    author_name = g[0].strip()
    if g[1]:
        author_email = g[1].strip()
    else:
        author_email = ''
else:
    author_name = data['__author__']


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


setup(name='dunder',
      version=data['__version__'],
      description='Extract dunder variables from a Python source file.',
      long_description=read('README'),
      author=author_name,
      author_email=author_email,
      url="https://launchpad.net/dunder.py",
      license='Apache-2.0',
      package_dir={'': 'src'},
      py_modules=['dunder'],
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
      ],

      tests_require=['tox'],
      cmdclass={'test': Tox},
)
