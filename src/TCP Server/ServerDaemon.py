# Python imports
import os
import time
import socket
import signal
import logging
import datetime
import traceback
import multiprocessing
from   configparser     import ConfigParser
# Program imports
from   logAdapter       import logAdapter
from   daemon           import simpleDaemon


# Daemon
class ServerDaemon(simpleDaemon):

    # Constructor
    def __init__(self, name='', stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', basepath='', logLevel=None):
        # Public properties
        pidfile = basepath + '/' + name + ".pid"
        super().__init__(name, pidfile, stdin, stdout, stderr)
        self.basepath   = basepath
        if basepath == '' or basepath == '/' or basepath is None:
            raise Exception("Path servizio " + name + " non valida")

        # Constructor setup
        self.SERVICE = "System"
        self.__SigLock   = False
        self.__logSetup(logLevel)                                               # Logging facility setup
        self.__LoadConfiguration()                                              # Loading configuration file and properties
        # Configuration file parser
        configParser = ConfigParser()
        configParser.read(self.configfile)
        # Loading needed properties from configParser
        self.systemHost  = self.__LoadConfigurationVar(configParser, 'host')
        self.systemPort  = int(self.__LoadConfigurationVar(configParser, 'port'))
        self.connections = int(self.__LoadConfigurationVar(configParser, 'connections', 5))
        self.SocketList  = []
        self.TIMEOUT     = 60                                                   # TCP Connection, 60s
        self.BUFFERSIZE  = 1024                                                 # TCP BufferSize, 1K
        self.FILEMESSAGE = basepath + '/messages.log'
        self.ProcessPool = []


    # Setup logging facility
    def __logSetup(self, logLevel):
        # Loggging setup, create locale [logger] var and attaching its own handler
        self.loglevel   = logLevel
        logger = logging.getLogger(self.name)                                   # Log service name
        Formatter   = logging.Formatter('%(asctime)-15s %(levelname)-8s %(process)5d %(message)s', '%Y-%m-%d %H:%M:%S')
        if    logLevel == 'critical': logger.setLevel(logging.CRITICAL)         # Log level type
        elif  logLevel == 'error'   : logger.setLevel(logging.ERROR)
        elif  logLevel == 'warning' : logger.setLevel(logging.WARNING)
        elif  logLevel == 'info'    : logger.setLevel(logging.INFO)
        elif  logLevel == 'debug'   : logger.setLevel(logging.DEBUG)
        else: logger.setLevel(logging.INFO)
        FileHandler = logging.FileHandler(self.basepath + '/server.log')
        FileHandler.setFormatter(Formatter)
        logger.addHandler(FileHandler)
        # Setting [self.logger] property with system wide special adapter [logAdapter]
        self.logger = logAdapter(logging.getLogger(self.name), {'class': 'Daemon'})


    # Loading configuration file ./server.conf
    def __LoadConfiguration(self):
        self.configfile = self.basepath + '/server.conf'                     # Configuration file
        if not os.path.isfile(self.configfile):
            raise Exception("Configuration File " + self.configfile + " not found")
        FileContent = open(self.configfile, 'rb').read().decode('UTF-8').replace('\r\n', '\n')  # Dos2Unix/like conversion on configuration file (if needed)
        open(self.configfile, 'wb').write(bytes(FileContent, 'UTF-8'))


    # LOAD CONFIGURATION VAR - Get module setting from configuration file
    # @return (Value) When found
    # @return (None ) When not found
    def __LoadConfigurationVar(self, parser, variable, default=None):
        try:
            return parser[self.SERVICE][variable]
        except Exception:
            Message = "Cannot recover variable '%s' from section [%s] in %s " % (variable, self.SERVICE, self.configfile)
            self.logger.error("LoadConfigurationVar: %s" % Message)
            if default is None:
                raise Exception(Message)
            else:
                return default


    # DAEMON START - User hook function for daemon startup
    def daemonStart(self):
        self.logger.info('')
        self.logger.info('')
        self.logger.info("%s Daemon started   ((( PID:%s )))   [%s:%s] (log:%s)" % (self.name, self.pid, self.systemHost, self.systemPort, self.loglevel))
        signal.signal(signal.SIGUSR1, self.__daemonSignal)                              # SIGUSR1 [shutdown request]
        self.__TCPinit()
        self.__daemonLoop()
        self.stop()


    # DAEMON SIGNAL - Handler for incoming signals to this service
    def __daemonSignal(self, signum, frame):
        self.logger.info("daemonSignal: %s  [%s]" % (str(signum), self.__SigLock))
        if not self.__SigLock:
            self.__SigLock = True
            if signum == signal.SIGUSR1:
                self.running = False
                self.logger.info("Server Daemon shutdown requested")
            self.__SigLock = False


    # Init TCP stream
    def __TCPinit(self):
        self.logger.info("Starting socket server on %s:%d" % (self.systemHost, self.systemPort))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.systemHost, self.systemPort))
        self.sock.listen(self.connections)                                              # Connections that can be queued up waiting to be accepted
        self.SocketList = []
        self.SocketList.append(self.sock)


    # PROCESS POOL JOIN - Waiting for zombie process with safe termination [join()]
    def __ProcessPoolJoin(self):
        self.logger.debug("Pool = %s" % self.ProcessPool)
        for Process in self.ProcessPool:
            self.logger.debug("    alive = %s" % Process.is_alive())
            if not Process.is_alive():
                Process.join()
                self.ProcessPool.remove(Process)


    def __ProcessKiller(self):
        for Process in self.ProcessPool:
            time.sleep(0.1)
            self.logger.info("[SIGQUIT] -> (%5d) %s" % (Process.pid, Process.name))
            try: os.kill(Process.pid, signal.SIGQUIT)
            except Exception: pass


    # DAEMON STOP - User hook function for daemon shutdown
    # @see   DON'T USE IT, use self.stop().    self.stop() calls this hook inside it
    def daemonStop(self):
        self.logger.info("%s Daemon stopped   ((( PID:%d )))" % (self.name, self.pid))


    # DAEMON LOOP - Loop incoming connection until death
    def __daemonLoop(self):
        self.logger.info("Service waiting")
        while self.running:
            try:
                Client, Address = self.sock.accept()                                # TCP Client Socket and Address
                self.logger.debug("sock.accept()")
                Client.settimeout(self.TIMEOUT)                                     # Client inactivity timeout (1min)
                ClientProcess = multiprocessing.Process(target=self.__TCPclientSpawn, args=(Client, Address))
                ClientProcess.daemon = True
                ClientProcess.start()
                self.ProcessPool.append(ClientProcess)
                self.__ProcessPoolJoin()

            except InterruptedError:                                                # Interruzione dopo intercettazione SIGUSR1
                self.logger.info("[SIGUSR1] MAIN - Running:%s" % self.running)
            except Exception as e:
                self.logger.error("!!! [%s:%s] %s" % (e.errno, type(e), str(e)))
                self.logger.error("    %s" % traceback.format_exc())
        # Killing zombie childs, if any
        self.__ProcessKiller()
        self.__ProcessPoolJoin()


    def __TCPclientSpawn(self, Stream, Source):
        Message = Stream.recv(self.BUFFERSIZE).decode('UTF-8').strip(' \r\n')
        if Message == "":
            self.logger.debug("<<<[Empty command], aborting connection !")
            self.SocketClose(Stream)
            return
        self.logger.debug("<<< %s" % (Message))
        self.__MessageWriteDisk(Message)
        self.__SocketClose(Stream)


    # Close an opened socket
    def __SocketClose(self, Socket):
        Socket.shutdown(socket.SHUT_RDWR)
        Socket.close()


    def __MessageWriteDisk(self, Message):
        self.logger.info("Writing to disk [%s]" % Message)
        File = open(self.FILEMESSAGE, "a+")
        File.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + Message + '\n')
        File.close()
