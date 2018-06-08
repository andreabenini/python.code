# uWSGI Environment Printer - Print uWSGI environment variables
#                           Copyright (C) 2018/06  Andrea (Ben) Benini
# LICENSE:
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the  Free Software Foundation, either version  3 of  the License, or
# (at your option) any later version.
#
# This  program is  distributed  in the hope  that it will be  useful,
# but  WITHOUT  ANY  WARRANTY;  without even the  implied warranty  of
# MERCHANTABILITY  or  FITNESS  FOR  A  PARTICULAR  PURPOSE.   See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import io

# Print uwsgi environment
def application(Environment, Output):
    Output('200 OK', [('Content-Type', 'text/html')])
    yield(b'\n')
    for Variable in Environment:
        TypeValue = str(type( Environment[Variable] ))
        if   type(Environment[Variable]) is bytes:
            Value = Environment[Variable].decode('UTF-8')
        elif type(Environment[Variable]) is str:
            Value = Environment[Variable]
        elif type(Environment[Variable]) is int:
            Value = str(Environment[Variable])
        elif type(Environment[Variable]) is bool:
            Value = str(Environment[Variable])
        elif type(Environment[Variable]) is tuple:
            Value = '('+','.join(map(str, Environment[Variable]))+')'
        elif isinstance(Environment[Variable], io.TextIOBase):
            Value = '[[[TextIOBase file stream]]]'
        elif TypeValue == "<class 'uwsgi._Input'>":
            Value = '[[[uwsgi._Input file stream]]]'
        elif TypeValue == "<class 'builtin_function_or_method'>":
            Value = '[[[builtin_function_or_method]]]'
        elif TypeValue == "<class 'uwsgi._Input'>":
            Value = '[[[uWSGI Input]]]'
        else:
            Value = '[[[ UNKNOWN ]]]'
        yield('{type:25} {var:20} = {value}\n'.format(
                type  = TypeValue,
                var   = Variable,
                value = Value
              ).encode('UTF-8'))
    yield(b'++++++++++++++++++++++++++\n')
