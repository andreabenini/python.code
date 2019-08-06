# Various methods for opening files:


# Open pipe for writing, non blocking
def openAndWrite_NonBlocking():
    try:
        f = os.open("myfile", os.O_WRONLY|os.O_NONBLOCK)
        string2Write = "My string to write"
        os.write(f, str.encode("{}\n".format(string2Write)))
        os.close(f)
    except OSError as e:
        # Ignoring ENXIO error because there could be no one reading the pipe on the other side, this is not
        # strictly an error because communicating to nobody would not be a problem (otherwise is an error)
        if e.errno != errno.ENXIO:
            print("ERROR: Cannot write myfile [OS ERROR]: {}".format(str(e)))
    except Exception as e:
        print("ERROR: {}".format(str(e)))
