class EarthquakeTrigger:
    def __init__(self,
                 json_dict=None,
                 id=None,
                 min_magnitude=None,
                 tsunami=None,
                 location=None,
                 radius=None):
        if json_dict:
            self.id = json_dict['id']
            self.min_magnitude = json_dict['min_magnitude']
            self.tsunami = json_dict['tsunami']
            self.location = json_dict['location']
            self.radius = json_dict['radius']
        else:
            self.id = id
            self.min_magnitude = min_magnitude
            self.tsunami = tsunami
            self.location = location
            self.radius = radius
    
    def test_trigger(self,
                     magnitude,
                     tsunami,
                     location):
        array = [
            self.test_min_magnitude(magnitude),
            self.test_tsunami(tsunami),
            self.test_location(location)
        ]

        if False in array:
            return False
        else:
            return True

    def test_min_magnitude(self, magnitude):
        if self.min_magnitude is None: 
            return True
        elif magnitude >= self.min_magnitude:
            return True
        else:
            return False
    
    def test_tsunami(self, tsunami):
        if self.tsunami is None:
            return True
        elif tsunami == self.tsunami:
            return True
        else:
            return False
    
    def test_location(self, location):
        #$TODO test location
        return True

