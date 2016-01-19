import logging
def initLogging():
    # Use simple logging in this file
    # See whether I can seperate logging from this program and my library

    logging.basicConfig(filename='test_logging.log',level=logging.DEBUG,
        format='%(asctime)s %(message)s', datefmt='%Y%m%d-%H%M%S')

    logger = logging.getLogger('root')
    # This will setup the default logger
    # The default level for this logging system is info
    # a = logging
    a = logger
    a.info('Hello world')
    a.error('This is an error')
    a.warning('This is a warning')
    a.debug('Debug information')

# initLogging()

# Make sure the log information from tenon would not contaminate here
tenonpath = '..'
import sys; sys.path.append(tenonpath)
import tenon


tenon.run(__file__, '../demo.blend')
if tenon.inblender():
    tenon.render.write('demo.png')
    tenon.logging.info('Write image to demo.png')

    logging.info('The execution is completed')
