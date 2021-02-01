from gps import *
import json
from datetime import datetime
import time

out_file = "/tmp/location.json"
time_format = "%m/%d/%Y %H:%M:%S"

def get_data_from_report(gpsd, duration, sleep=1):
    start_time = datetime.now()
    updated = False
    while (datetime.now() - start_time).total_seconds() < duration:
        report = gpsd.next()
        if report['class'] == 'TPV':
            if report['mode'] < 3: # Move on if we don't have a 3D fix
                print("No 3D fix. Skipping update.")
                continue
            out_dict = dict()
            out_dict['lat'] = report['lat']
            out_dict['lon'] = report['lon']
            out_dict['last_update'] = datetime.now().strftime(time_format)
            print(f"Updating {out_file} with data from {json.dumps(out_dict,indent=4)}")
            with open(out_file, 'w') as loc_json:
                json.dump(out_dict, loc_json, indent=4)
            updated = True
            break
    if not updated:
        print("Could not get solid GPS data from device. Something might be wrong!")
def main(get_duration, loop_interval):
    gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
    try:
        while True:
            get_data_from_report(gpsd, get_duration)
            time.sleep(loop_interval)
    finally:
        print("Shutting down!")

if __name__ == "__main__":
    main(30, 300)
