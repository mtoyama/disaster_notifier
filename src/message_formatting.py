from .utils import timestamp_to_readable

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

def format_sms_nws_alert(title, alert_list):
    message = []
    message.append(title)
    count = len(alert_list)
    message.append(f"Weather alerts matching filter: {count}")
    for index, alert in enumerate(alert_list):
        message.append(f"Data for alert {index+1} of {count}:")
        properties = alert['properties']
        message.append(properties["parameters"]["NWSheadline"][0])

        severity = properties['severity']
        message.append(f"Severity: {severity}")

        description = properties['description'].split("\n")
        description_header = description[0]
        message.append(f"Description: {description_header}")

        api_link = properties['@id']
        message.append(f"More information: {api_link}")

        message.append("\n")
    
    return "\n".join(message)