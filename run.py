import sys
sys.path.append('/q/run/')
from tenon.tasks.l23 import L23Job

def ls():
    jobs = activeJobs()
    return jobs

# Define available jobs here
def activeJobs():
    jobs = []

    l23_texture_cloth = L23Job('l23textureBrodatz')
    l23_texture_cloth.cloth = 'textureBrodatz'
    l23_texture_cloth.comment = 'L23 dataset with Texture pattern as cloth'
    jobs.append(l23_texture_cloth)

    return jobs

def inactiveJobs():
    jobs = []

    l23_color_cloth = L23Job('l23color')
    l23_color_cloth.cloth = 'color'
    l23_color_cloth.comment = 'L23 dataset with pure color cloth'
    jobs.append(l23_color_cloth)

def run():
    import bpy

    import logging
    debugFile = bpy.path.abspath('//debug.log')
    print('Log is saved to %s' % debugFile)
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers[:]: # Reset the existing config
        logging.root.removeHandler(handler)

    logging.basicConfig(filename=debugFile,level=logging.DEBUG)
    logging.info('Test message.')

    # Setup the logging for this session
    import logging
    debugFile = bpy.path.abspath('//debug.log')
    print('Log is saved to %s' % debugFile)
    logging.basicConfig(filename=debugFile,level=logging.DEBUG)
    logging.info('Test message.')

    ts = ls()
    ts[0].run(1000)

if __name__ == '__main__':
    run()
