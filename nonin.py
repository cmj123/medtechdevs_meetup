import serial
import copy 
import json
import requests

from datetime import datetime, timedelta


real = False

URL = 'http://copd.herokuapp.com/sensors/api/v1.0/measurement_bulk/'
URL = 'http://localhost:8000/sensors/api/v1.0/measurement_bulk/'


if real:

    ser = serial.Serial('/dev/ttyS4', 9600)

    print ser

    configuration = "\x02\x70\x02\x02\x08\x03"

    print "about to write configuration", configuration
    print ':'.join(x.encode('hex') for x in configuration)

    ser.write(configuration)

    x = ser.read(1)

    print x.encode('hex')

    def get_ts():
        return datetime.now().isoformat()

else:
    stime = datetime(2015, 6, 20, 23, 30, 00, 0) 
    ser = open('dump.raw', 'r')

    def get_ts():
        return (stime + timedelta(seconds=(ser.tell() / 4))).isoformat()


sequence  = 1
parameter = 1 

state = {}

submit = []

param_map = {
    1: (1, 2,), # HR
    2: (2, 1,), # SpO2
}

state[1] = {
    'timestamp_start': get_ts(),
    'timestamp_end'  : get_ts(),
    'value': None,
    'sequence': sequence,
    'parameter': param_map[1][0],
    'unit': param_map[1][1],
}

state[2] = {
    'timestamp_start': get_ts(),
    'timestamp_end'  : get_ts(),
    'value': None,
    'sequence': sequence,
    'parameter': param_map[2][0],
    'unit': param_map[2][1],
}

print state[1]

cnt = 0

while True:
    print "attempting to read"
    s = ser.read(4)
    cnt += 1 
    print ':'.join(x.encode('hex') for x in s)

    if ord(s[0]) == 128:
        print 'VALID', ord(s[1]), ord(s[2])

        for rec in (1, 2,):
            val = ord(s[rec])

            if state[rec]['value'] == val:
                state[rec]['timestamp_end'] = get_ts()
            else:
                if state[rec]['value'] is not None:
                    submit.append(copy.deepcopy(state[rec]))
                state[rec]['timestamp_start'] = get_ts()
                state[rec]['timestamp_end']   = get_ts()
                state[rec]['value'] = val

        # if len(submit) > 60*10:
        if cnt > 600:
            cnt = 0
            for rec in (1, 2,):
                submit.append(copy.deepcopy(state[rec]))

                state[rec]['timestamp_start'] = get_ts()
                state[rec]['timestamp_start'] = get_ts()
                state[rec]['value'] = None



            print submit

            r = requests.post(
                URL, 
                data=json.dumps(submit), 
                headers={'Content-type':'application/json'}
            )

            submit = []
            print r, r.content
