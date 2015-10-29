def render():
    import bpy, sys

    # Space between = is required
    PWD = '/q/run/'
    sitePkg = '/usr/local/lib/python3.4/site-packages/'

    for v in [PWD, sitePkg]:
        sys.path.append(v)

    # Setup the logging for this session
    import logging
    debugFile = bpy.path.abspath('//debug.log')
    print('Log is saved to %s' % debugFile)
    logging.basicConfig(filename=debugFile,level=logging.DEBUG)
    logging.info('Test message.')

    import tenon.job as jb
    ts = jb.ls()
    ts[0].run()

if __name__ == '__main__':
    render()
