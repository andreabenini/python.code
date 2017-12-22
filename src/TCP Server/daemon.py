#
# Ben's daemon class, python 3.x. - Simple but effective Python Daemon
#
# @author   Andrea Benini (andreabenini  gmail)
#           https://github.com/andreabenini/python.code
#
# @license  GPLv3
#           Copyright (C) 2017  Andrea Benini
#
#           This program is free software; you can redistribute it and/or modify
#           it under the terms of the GNU General Public License as published by
#           the Free Software Foundation; either version 3 of the License, or
#           (at your option) any later version.
#
#           This program is distributed in the hope that it will be useful,
#           but WITHOUT ANY WARRANTY; without even the implied warranty of
#           MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#           GNU General Public License for more details.
#
#           You should have received a copy of the GNU General Public License
#           along with this program; if not, write to the Free Software Foundation,
#           Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
#           or see <http://www.gnu.org/licenses/>.
#
# @see      Drop me a note if you want, comments welcomed, slightly modified and improved version, credits to:
#           http://web.archive.org/web/20170313055313/http://www.jejik.com:80/files/examples/daemon3x.py
#
import os
import sys
import time
import atexit
import signal


#
# common daemon class. Subclassed below
#
class simpleDaemon:

    # Constructor
    def __init__(self, name='', pidfile='', stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin   = stdin
        self.stdout  = stdout
        self.stderr  = stderr
        self.name    = name
        self.pid     = None
        self.pidfile = pidfile
        self.running = True
        self.signal  = signal.SIGQUIT


    # PID GET - Get pid of the running process
    def pidGet(self):
        if self.pid is None:
            try:
                with open(self.pidfile, 'r') as pf:
                    pid = int(pf.read().strip())
                pf.close()
                self.pid = pid if self.__pidDetect(pid) else None

            except (IOError, TypeError):
                self.pid = None
        return self.pid

    # PID DETECT - Detect if there's a running process on that pid
    # @see Used on pidGet(self)
    def __pidDetect(self, pid):
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True

    # PID CREATE - Create and write the pid file
    def pidCreate(self):
        self.pid = os.getpid()
        with open(self.pidfile, 'w+') as f:
            f.write(str(self.pid) + '\n')

    # PID DELETE - Delete pid file
    def pidDelete(self):
        os.remove(self.pidfile)


    # START - Start the daemon
    def start(self):
        if self.pidGet():
            sys.stderr.write("{0} is already running [PID:{1}]. Cannot continue\n".format(self.name, self.pid))
            sys.exit(1)
        # Start the daemon
        print("demonize now !")
        self.__daemonize()
        print("defined ?")
        IsMethodDefined = getattr(self, "daemonSignal", None)
        print("callable")
        if callable(IsMethodDefined):
            print("party hard")
            signal.signal(self.signal, self.daemonSignal)
        print("Yeah me !")
        self.daemonStart()              # Endless loop must be placed here


    # STOP - Stop the daemon
    def stop(self, silent=False):
        try:
            # Get daemon PID
            self.pidGet()
            if not self.pid:
                if silent: return       # Daemon not running ? It's not a problem
                sys.stderr.write("{0} is not running\n".format(self.name))
                sys.exit(1)
            # Run user function hook
            self.daemonStop()
            # Try killing the daemon process
            while True:
                os.kill(self.pid, self.signal)
                time.sleep(0.1)

        except OSError as err:
            e = str(err)
            if e.find("No such process") <= 0:
                print(str(err))
                sys.exit(1)
        finally:
            if os.path.exists(self.pidfile):
                os.remove(self.pidfile)
            self.pid = None


    # Restart the daemon
    def restart(self):
        self.stop(silent=True)
        self.start()


    # DAEMON START (virtual) This method must be overridden in your own subclass
    def daemonStart(self):
        raise NotImplementedError

    # DAEMON STOP  (virtual) This method must be overridden in your own subclass
    def daemonStop(self):
        raise NotImplementedError


    # Forking from parent process
    # @see Private method, called from __daemonize() method only
    def __fork(self, attempt):
        try:
            pid = os.fork()
            if pid > 0:             # PID>0  [I am your father]
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('{0} daemon fork({1}) failed: {2}\n'.format(self.name, attempt, err))
            sys.exit(1)

    # Deamonize method with UNIX double fork black magic ["Advanced Programming in the UNIX Environment" (ISBN 0201563177)]
    def __daemonize(self):
        self.__fork(1)                          # First Fork
        # decouple from parent environment
        try: os.chdir('/')
        except OSError as err:
            sys.stderr.write('change path failed: {0}', err)
            sys.exit(1)
        os.setsid()
        os.umask(0)
        self.__fork(2)                          # Second Fork

        # redirect standard file descriptors (stdin,stdout,stderr)
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.pidDelete)
        self.pidCreate()
