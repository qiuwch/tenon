# Script to batch run tasks defined in a data file.
# TODO: Consider rewriting it with protobuf, this is the most messy part of this project
import sys
sys.path.append('..')
import logging
from tenon.tasks.l23 import * # import all the task definition from here

def parseFromFile(filename):
    ''' Read task from csv file, each row corresponds to a task '''
    # Get job type
    classType = os.path.basename(filename).split('_')[0] # A hacky way to get the job type
    logging.info('Load from %s, job type is %s' % (filename, classType))    
    jobClass = eval(classType)
    j = jobClass() # dynamically determine the job type

    tasks = []

    with open(filename, 'r') as f:
        # Read header from file
        line = f.readline()
        sep = line.find(':')
        while sep != -1:
            header = line[:sep].strip()
            content = line[sep+1:].strip()
            setattr(j, header, content)
            line = f.readline()
            sep = line.find(':')

        # print(j.tasktype)
        assert(j.tasktype != None and j.tasktype != "")
        taskClass = eval(j.tasktype)

        j.outputFolder += '/%s/' % strTimeStamp() # Put into a subfolder with timestamp
        while line.strip() == '':
            line = f.readline() # Skip empty line

        # Read task list from file
        headerLine = line
        header = headerLine.strip().split(',')

        line = f.readline()
        while line:
            t = taskClass()
            t.parseFromLine(line, header)
            t.outputFolder = j.outputFolder
            tasks.append(t)
            line = f.readline()

        j.tasks = tasks

    j.validate()

    return j

def ls(id=None):
    ''' Utility to list all available task '''
    import glob
    import tenon.config

    fmt = tenon.config.bpyPathHelper('//*.csv')
    csvFiles = glob.glob(fmt) # TODO: fix path helper
    logging.info('Get all the job files in %s, total number %d' % (fmt, len(csvFiles)))

    js = []
    for ii in range(len(csvFiles)):
        csvFile = csvFiles[ii]
        j = parseFromFile(csvFile)

        js.append(j)

    if not id:
        return js
    else:
        return js[id]

if __name__ == '__main__':
    # Run a unit test here
    import sys
    sys.path.append('..')
    FORMAT = "[%(levelname)s : %(filename)s:%(lineno)s - %(funcName)s() ] %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    print(ls())
