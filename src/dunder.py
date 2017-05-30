"""Extract 'dunder' variables e.g. __version__ from a source file"""

import io
import re
import ast

__version__ = '0.1.1'
__author__ = 'Simon Kennedy <sffjunkie+code@gmail.com>'

__all__ = ['parse']


class Dunders(dict, ast.NodeVisitor):
    """A dictionary which is filled using an ast NodeVisitor to extract
    dunder variables e.g. __version__

    Only the following types of dunder values are parsed correctly

        * Strings
        * Numbers
        * Non nested tuples and lists of Strings or Numbers
          e.g. (1, 2), [1, 3] and (1, 'd') are
          parsed correctly but (1, (2, 3)) is not.
    """

    def __init__(self):
        dict.__init__(self)
        self._mode = None
        self._name = ''
        self._elems = None

    def parse(self, filename, **kwargs):
        """Parse filename"""

        stream = io.open(
            filename,
            encoding=kwargs.get("encoding", "utf8")
        )

        self.clear()
        data = stream.read()
        data = self._remove_codings(data)
        root = ast.parse(data, filename)
        self.visit(root)

    def generic_visit(self, anode):
        ast.NodeVisitor.generic_visit(self, anode)

    def visit_Assign(self, anode):
        """Visit an assignment node"""

        self._mode = 'assign'
        ast.NodeVisitor.generic_visit(self, anode)
        self._mode = None

    def visit_Name(self, anode):
        """Visit a name node"""

        if self._mode == 'assign' and re.match(r'__[\w_]+__', anode.id):
            self._name = anode.id

    def visit_Str(self, anode):
        """Visit a string node"""

        if self._mode == 'assign' and self._name != '':
            self[self._name] = anode.s
            self._name = ''
        elif self._mode in ['tuple', 'list']:
            self._elems.append(anode.s)

    def visit_Num(self, anode):
        """Visit a number node"""

        if self._mode == 'assign' and self._name != '':
            self[self._name] = anode.n
            self._name = ''
        elif self._mode in ['tuple', 'list']:
            self._elems.append(anode.n)

    def visit_Tuple(self, anode):
        """Visit a tuple node.
        
        Only single level tuples are parsed correctly
        """
        if self._mode == 'assign' and self._name != '':
            self._mode = 'tuple'
            self._elems = []
            self.generic_visit(anode)
            self[self._name] = tuple(self._elems)
            self._mode = 'assign'
            self._name = ''

    def visit_List(self, anode):
        """Visit a list node.
        
        Only single level lists are parsed correctly
        """
        if self._mode == 'assign' and self._name != '':
            self._mode = 'list'
            self._elems = []
            self.generic_visit(anode)
            self[self._name] = list(self._elems)
            self._mode = 'assign'
            self._name = ''

    def _remove_codings(self, data):
        """Remove any 'coding' lines as the Python 2 compile function
        chokes on them.
        """
        remove = []
        lines = data.split('\n')
        for idx, line in enumerate(lines):
            if self._is_coding(line):
                remove.append(idx)

        for idx, idx_to_remove in enumerate(remove):
            idx_to_remove = idx_to_remove - idx
            del lines[idx_to_remove]

        return '\n'.join(lines)


    def _is_coding(self, s):
        """Return True if string defines an encoding for the file"""
        
        if not s or s[0] != '#':
            return False

        matches = re.findall(r'coding[:=]\s*([-\w.]+)', s)
        if matches:
            return True
        else:
            return False


def parse(filename, **kwargs):
    """Parse a file and return the dunder variables as a dictionary"""

    d = Dunders()
    d.parse(filename, **kwargs)
    return d
