import json
data = parse.urlencode(<your data dict>).encode()
req =  request.Request(<your url>, data=data) # this will make the method "POST"
resp = request.urlopen(req)
data = { 'test1': 10, 'test2': 20 }                 # Data dict
data = json.dumps(data)                             # Dict to Json # Difference is { "test":10, "test2":20 }
data = str(data)                                    # Convert to String
data = data.encode('utf-8')                         # Convert string to byte
req =  request.Request(<your url>, data=data)       # Post Method is invoked if data != None
resp = request.urlopen(req)                         # Response
