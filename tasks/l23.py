from tenon.tasks.basic import *
from tenon.scene import Shirt, Pants, Bg, Lighting, Hair, Skin
from tenon.render import Render

class L23Job(Job):
    def config(s):
        s.clothOptions = ['Texture', 'Color'] # Enum type
        s.lightOptions = ['Environment', 'Random']

        # Best option is Texture cloth + Random lighting + Random BG?
        s.clothTexture = 'Texture'
        s.clothTexture = 'Color'
        s.randomBG = True



    def __init__(self):
        self.config()
        self.outputFolder = '/q/cache/lsp_2d_3d/render_output/'
        for i in range(1, 2001):
            t = L23Task()
            t.LSPPoseId = i
            tasks.append(t)

    def setupScene(self): # This will be executed before the job is run
        Shirt.setFolder('//textures/shirt')
        Pants.setFolder('//textures/pants')
        Bg.setFolder('//background/INRIA')
        Hair.setFolder('//textures/hair')
        Skin.setFolder('//textures/skin')

        Render.skyOff() # Disable background

        if not '_outputFolder' in dir(self): # This is the configuration defined in file
            self._outputFolder = self.outputFolder
        
        import bpy, os
        sceneId = os.path.basename(bpy.data.filepath).split('.')[0]
        self.outputFolder = self._outputFolder + '/%s_%s/' % (sceneId, strTimeStamp()) # Put into a subfolder with timestamp


class L23Task(Task):
    requiredProps = Task.requiredProps + ['LSPPoseId']

    def __init__(self):
        Task.__init__(self)
        # Define the property list for this task


    def execute(self):
        self.prefix = 'im%04d' % (int(self.LSPPoseId)) # TODO: Let it start from 1

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
        logging.info('Animate to Pose %s' % self.LSPPoseId)
        tenon.puppet.animateCP(int(self.LSPPoseId))
        # tenon.pose.animateEditBone(int(self.LSPPoseId))
        # This is for debugging
