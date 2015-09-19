import serial
import copy 
import json
import requests

from datetime import datetime, timedelta


real = True
        # If real = True -> process /dev/ttyS4
        # else -> process dump.raw
mode8 = True
        # if mode8 = False -> process mode 2
        # else -> process mode8 dump (higher data rate)

URL = 'http://copd.herokuapp.com/sensors/api/v1.0/measurement_bulk/'
URL = 'http://localhost:8000/sensors/api/v1.0/measurement_bulk/'


if real:

    ser = serial.Serial('/dev/ttyS4', 9600)

    print ser

    if mode8:
        configuration = "\x02\x70\x02\x02\x08\x03"
    else:
        configuration = "\x02\x70\x02\x02\x02\x03"


    print "about to write configuration", configuration
    print ':'.join(x.encode('hex') for x in configuration)

    ser.write(configuration)

    x = ser.read(1)

    print x.encode('hex')

    def get_ts():
        return datetime.now().isoformat()

else:
    stime = datetime(2015, 6, 29, 23, 30, 00, 0) 
    ser = open('dump.raw', 'r')

    if mode8:
        def get_ts():
            return (stime + timedelta(microseconds=(ser.tell() * 1000 / 5 / 75))).isoformat()
    else:
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

# print state[1]

cnt = 0
scnt = 0

prev_pulse = 0  
prev_cnt   = 0
pp_sync = False

spa = 0

def process_record(rec, val):
    if state[rec]['value'] == val:
        state[rec]['timestamp_end'] = get_ts()
    else:
        if state[rec]['value'] is not None:
            submit.append(copy.deepcopy(state[rec]))
        state[rec]['timestamp_start'] = get_ts()
        state[rec]['timestamp_end']   = get_ts()
        state[rec]['value'] = val


def submit_data():
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

while True:
    # print "attempting to read"

    if mode8:
        s = ser.read(5)
    else:
        s = ser.read(4)
    cnt += 1 
    scnt += 1
    print ':'.join(x.encode('hex') for x in s)


    if mode8:
        pleth = ord(s[1]) * 256 + ord(s[2])
    
        pulse = (ord(s[0]) & 0x06) / 2

        snsa = ord(s[0]) & 0x70

        sync = ord(s[0]) & 0x01

        if sync:
            scnt = 0

        if snsa == 0:
            if scnt == 0:
                process_record(1, hr)
                process_record(2, spo2)

                new_hr = ord(s[3]) * 256

            if scnt == 1:
                new_hr += ord(s[3])
                hr = new_hr 

            if scnt == 2:
                spo2 = ord(s[3])

            if scnt == 7:
                stat2 = ord(s[3])
                spa = (stat2 & 0x20) / 0x20  

            # print cnt, pleth, pulse

            if pulse > 1:
                prev_cnt = cnt
                pp_sync = False

            if pulse == 1 and prev_pulse == 0:
                nonin_pp = 75.0/(float(hr) / 60)

                
                if (cnt - prev_cnt) < (nonin_pp * 0.5) or (cnt - prev_cnt) > (nonin_pp * 1.5):
                    pass # Sorry, fake 

                else:                
                    if pp_sync:
                        pass
                        # print float(cnt - prev_cnt) / 75.0
                        if spa: 
                            print cnt, 60 * 75 / float(cnt - prev_cnt), nonin_pp, hr

                prev_pulse = pulse
                prev_cnt   = cnt

            if prev_pulse == 1 and pulse == 0:
                prev_pulse = pulse

                pp_sync = True


        else:
            prev_cnt = cnt
            pp_sync = False

        if (cnt % (600 * 75)) == 0:
            submit_data()


    else:
        if ord(s[0]) == 128:
            print 'VALID', ord(s[1]), ord(s[2])

            for rec in (1, 2,):
                val = ord(s[rec])
                process_record(rec, val)

            # if len(submit) > 60*10:
            if cnt % 600 == 0:
                submit_data()