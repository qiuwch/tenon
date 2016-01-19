def timestamp():
    import datetime
    n = datetime.datetime.now()
    return n.strftime('%Y%m%d-%H%M%S')

class dictwrapper:
    def __init__(self, **kwargs):
        d = dict(**kwargs)
        self.__dict__.update(d)

def sphereLocation(radius, az, el):
    ''' 
    The input of az, el should be angle, not radius
    '''
    import math
    az = math.radians(az)
    el = math.radians(el)
    z = radius * math.sin(el)
    r = radius * math.cos(el)
    x = r * math.cos(az)
    y = r * math.sin(az)
    return [x, y, z]
