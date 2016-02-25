import tenon.logging as L
import tenon.obj

def timestamp():
    import datetime
    n = datetime.datetime.now()
    return n.strftime('%Y%m%d-%H%M%S')

class dictwrapper:
    def __init__(self, **kwargs):
        d = dict(**kwargs)
        self.__dict__.update(d)

def sphere_location(radius, az, el):
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

def get_obj(obj):
    if isinstance(obj, str):
        return tenon.obj.get(obj)

def camera_tracK(camera, target, subtarget):
    # Track_to constraint
    camera = get_obj(camera)
    target = get_obj(target)

    c = camera.constraints.new('TRACK_TO')
    c.target = target
    c.track_axis = 'TRACK_NEGATIVE_Z'
    c.up_axis = 'UP_Y'

    L.debug('Camera %s is setup to track obj %s and subtarget %s', camera.name, target.name, subtarget.name)
