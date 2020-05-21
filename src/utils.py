import datetime
import pytz
import geopy.distance

def format_sms_earthquake(title, earthquake_list):
    message = []
    message.append(title)
    count = len(earthquake_list)
    message.append(f"Earthquakes matching filter: {count}")
    for index, earthquake in enumerate(earthquake_list):
        message.append(f"Data for earthquake {index+1} of {count}:")
        properties = earthquake["properties"]
        message.append(properties["title"])

        time = timestamp_to_readable(properties["time"])
        message.append(f"Time: {time}")

        alert = properties["alert"]
        message.append(f"Alert level: {alert}")

        mag = properties["mag"]
        message.append(f"Magnitude: {mag}")

        tsunami = properties["tsunami"]
        if tsunami == 1:
            message.append(f"Tsunami: Possible event indicated")
        else:
            message.append(f"Tsunami: Event not indicated")
        
        url = properties["url"]
        message.append(f"More details: {url}")
        message.append("\n")
    
    return "\n".join(message)
    
def timestamp_to_readable(timestamp: int) -> str:
    timestamp = datetime.datetime.fromtimestamp(timestamp//1000)
    timestamp_tz = timestamp.astimezone(pytz.timezone("US/Pacific"))
    return timestamp_tz.strftime("%Y/%m/%d %H:%M:%S %Z")

def lat_long_check_within_radius(latlong1: tuple,
                                 latlong2: tuple) -> int:
    return geopy.distance.vincenty(latlong1, latlong2).miles
        