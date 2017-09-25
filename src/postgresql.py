

# Execute a SQL statement on the current database
# @see ExecCommand defined in shell.py
# @see DBRootUsername, DBRootPassword, Hostname are three global/local variables used to access pgsql db
def PGSQLExecCommand(SQLCommand='', RaiseError=True, ShellCommand=''):
    if ShellCommand is None or ShellCommand=='':
        PGCommand = "PGPASSWORD=\"%s\" psql --host=%s --no-password --command=\"%s\" --quiet --tuples-only" %
                    (DBRootPassword, HostName, SQLCommand)
    else:
        PGCommand = ShellCommand
    Output, ReturnCode = ExecCommand(['su', '-', DBRootUsername, '-c', PGCommand], DevNull=False)
    if RaiseError:
        if ReturnCode is not 0:
            print("ReturnCode=%s, %s" % (ReturnCode, Output.strip()))
            raise ValueError(Output.strip())
        return Output, ReturnCode

