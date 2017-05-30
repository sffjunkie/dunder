import sys
import ast
import os.path

this_dir = os.path.dirname(__file__)
mod_dir = os.path.abspath(os.path.join(this_dir, '..'))
sys.path.append(mod_dir)

import dunder

def filename(leaf):
    return os.path.join(os.path.dirname(__file__), leaf)

def test_dunder_nodeparser():
    node = ast.parse("""a = 1 + 2\n
__version__ = '1.2.2'\n
__author__='Simon'""")

    d = dunder.Dunders()
    d.visit(node)
    assert '__version__' in d

def test_dunder_file():
    d = dunder.Dunders()
    d.parse(filename('python.file'))
    assert d['__version__'] == '0.1'
    assert d['__brian__'] == (1, 2, 3)
    assert d['__wally__'] == 1
    assert d['__dave__'] == 1.1

def test_dunder_2files():
    d = dunder.Dunders()
    d.parse(filename('python.file'))
    d.parse(filename('python.file2'))
    assert '__version__' not in d
    assert d['__hector__'] == '0.2'
    assert d['__nobby__'] == (1, '4')
    assert d['__styles__'] == [56, 57]


def test_parse():
    d = dunder.parse(filename('python.file'))
    assert d['__version__'] == '0.1'
    assert d['__dave__'] == 1.1
