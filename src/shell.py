# EXEC COMMAND - Execute a command on the current shell
# @param Command (array|string) Something to execute, it might be an array or a string
def ExecCommand(Command=[], DevNull=True):
    # default:Devnull, otherwise redirected on stdout
    StdErr = open('/dev/null', 'w') if DevNull else subprocess.STDOUT
    if isinstance(Command, (list, tuple)):          # An array, executed "normally"
        Process = subprocess.Popen(Command, stdout=subprocess.PIPE, stderr=StdErr)
    else:                                           # Command is a string, running it into a shell
        Process = subprocess.Popen(Command, stdout=subprocess.PIPE, stderr=StdErr, shell=True)
    Process.wait()
    return Process.communicate()[0], Process.returncode
#
# Output, ReturnCode = ExecCommand('systemctl daemon-reload')
# if ReturnCode is not 0:
#     print('something went wrong (%s)' % ReturnCode)
# else:
#     print('Output: %s' % Output)

# Compact version of the above function
def ExecCommand(Command=''):
    result = os.popen(f"ls -la").read().encode()

# Exec stdin pipe command
def ExecStdinPipeCommand(Command):
    myProcess = subprocess.Popen(['cat', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    myProcess.stdin.write(bytes("Hello World\nSecond Line", encoding='UTF-8'))
    output = myProcess.communicate()[0]
    myProcess.stdin.close()
    print(output)
    
def subProcessCommand(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        return True
    print(f"stdout: {stdout.decode()}")
    print(f"stderr: {stderr.decode()}")
    return False


# Assorted filesystem functions
shutil.rmtree(Dir, True)                # Recursive delete
shutil.copytree(Template, Dir, True)    # Recursive copy
shutil.copytree(SourceDir, DestDir)
shutil.copyfile(FileSource, FileDestination)
