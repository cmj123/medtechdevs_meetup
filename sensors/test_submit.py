import requests
import json


URL = 'http://localhost:8000/sensors/api/v1.0/measurement_bulk/'

data = [ 
    {
        'timestamp_start': '2015-06-16T20:13:30Z',
        'timestamp_end'  : '2015-06-16T20:13:35Z',
        'value'          : '98.000000',
        'parameter'      : 1,
        'sequence'       : 1
    },
    {
        'timestamp_start': '2015-06-16T20:13:35Z',
        'timestamp_end'  : '2015-06-16T20:13:36Z',
        'value'          : '98.500000',
        'parameter'      : 1,
        'sequence'       : 1
    }
]

print json.dumps(data)

r = requests.post(URL, data=json.dumps(data), headers={'Content-type':'application/json'})

print r, r.content