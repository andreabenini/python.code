
# Must include importlib
import importlib
from   importlib import util

# Now check if a module is installed or not
if importlib.util.find_spec("requests") is None:
    print("'requests' module not found")
    sys.exit(1)

# Import it when found
import requests

