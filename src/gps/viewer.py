from gps import *
import json
import os

gpsd = gps(mode=WATCH_ENABLE)
try:
    while True:
        report = gpsd.next()
        print(json.dumps(report, default=lambda x: x.__dict__, indent=4))
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    print("Exiting")
