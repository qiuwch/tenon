from tenon.task import *
from tenon.scene import Shirt, Pants, Bg, Lighting, Hair, Skin
from tenon.render import Render

class L23Job(Job):
    def __init__(self):
        jointinfo = '/q/cache/tenon/lsp_3d_joint/2015101415_v2/%04d.csv'

        self.lightOptions = ['environment', 'random']
        self.bgOptions = ['on', 'off']

        # Pure color
        # self.shirtFolder = '//textures/shirt'
        # self.pantsFolder = '//textures/pants'

        # Texture Brodatz
        # self.shirtFolder = '//textures/ColorBrodatzPng'
        # self.pantsFolder = '//textures/ColorBrodatzPng'

        # A lot of random color
        # self.shirtFolder = '//textures/randomColor'
        # self.pantsFolder = '//textures/randomColor'

        # Skin color from makehuman repo
        # self.skinFolder = '//textures/skin'
        # self.skinFolder = '//textures/randSkinColor'
        
        self.bg = 'on'
        self.light = 'random'

        self.tasks = []
        for i in range(1, 2001):
            t = L23Task()
            t.pose = jointinfo % i
            t.prefix = 'im%04d' % i
            self.tasks.append(t)

    def finish(self):
        # Write post-processing script to this folder, this is a very hacky way
        cropCmd = '''\
#!env sh
matlab -nosplash -nodesktop –nojvm –noFigureWindows -r "addpath('/q/run/tenon/util/lsp'); lsp_convert_format('.');"\
'''
        with open(self.outputFolder + '/crop.sh', 'w') as f:
            f.write(cropCmd)

    def setupScene(self): # This will be executed before the job is run
        # Setup cloth
        Shirt.setFolder(self.shirtFolder)
        Pants.setFolder(self.pantsFolder)

        # Setup background
        if self.bg not in self.bgOptions:
            logging.error('Background option %s is invalid' % self.bg)
        else:
            if self.bg == 'on':
                Bg.setFolder('//background/INRIA')
                Render.skyOn()
            elif self.bg == 'off':
                Render.skyOff()

        Hair.setFolder('//textures/hair')
        Skin.setFolder(self.skinFolder)

        # self.outputFolder = self.baseFolder + '/%s_%s/' % (self.name, tenon.util.shorttimestamp()) # Put into a subfolder with timestamp




class L23Task(Task):
    requiredProps = Task.requiredProps + ['LSPPoseId']

    def __init__(self):
        Task.__init__(self)
        self.mode = 'ijd'
        # Define the property list for this task


    def execute(self):
        # if self.isRendered():
        #     logging.warning('%s exists, skip this task' % self.prefix)
        #     return

        Bg.randomChange()
        Hair.randomChange()
        Skin.randomChange()
        Shirt.randomChange()
        Pants.randomChange()
        Lighting.setup()  # Randomly update the lighting

        self.setPose()

        self.render() # Define in Task

    def setPose(self):
        import tenon.puppet
        logging.info('Animate to Pose %s' % self.pose)
        tenon.puppet.animateCP(self.pose)
        # tenon.pose.animateEditBone(int(self.LSPPoseId))
        # This is for debugging
