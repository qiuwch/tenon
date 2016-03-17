import tenon.logging as L
import tenon.obj
import os

def timestamp():
    import datetime
    n = datetime.datetime.now()
    return n.strftime('%Y%m%d-%H%M%S')

class dictwrapper:
    def __init__(self, **kwargs):
        d = dict(**kwargs)
        self.__dict__.update(d)

if tenon.inblender():
    def sphere_location(radius, az, el):
        '''
        The input of az, el should be angle, not radius
        The visualization of az/el is in
        https://en.wikipedia.org/wiki/Horizontal_coordinate_system
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
        else:
            return obj

    def camera_track(camera, target, subtarget=None):
        # Track_to constraint
        camera = get_obj(camera)
        target = get_obj(target)
        if camera == None or target == None:
            L.error('Fail to setup camera tracking.\nCamera %s and target %s invalid', camera, target)
            return

        c = camera.constraints.new('TRACK_TO')
        c.target = target
        c.track_axis = 'TRACK_NEGATIVE_Z'
        c.up_axis = 'UP_Y'

        L.debug('Camera %s is setup to track obj %s and subtarget %s', camera, target, subtarget)

