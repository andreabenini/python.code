# Various methods for opening files:
with open("filename.txt", "rt") as f:
    data_lines = f.readlines()

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

        
# Object, serialization, json and so on...

# Save python object to file
import pickle as pkl
# Save object
with open("file.pickle", "wb") as f:
    pkl.dump(object, f) 
# Load object
with open("file.pickle", "rb") as f:
    object = pkl.load(f)

# Load CSV as a python list of dicts
import csv
with open("data.csv") as csv_file:
    list_of_dicts = list(csv.DictReader(csv_file))

# JSON string to python dict, and back
import json
json_dict = json.loads(json_formatted_string)
json_formatted_string = json.dumps(json_dict)
