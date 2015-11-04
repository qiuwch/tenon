from tenon.tasks.basic import *
from tenon.scene import Shirt, Pants, Bg, Lighting, Hair, Skin
from tenon.render import Render

def generate():
    now = datetime.now();
    jobInfo = ObjectDict({
        'name': 'LSP2D3D',
        'shirtFolder': '//textures/cloth/color/',
        'pantsFolder': '//textures/cloth/lower/',
        'filename': '//%s_%02d.%02d.csv' % (L23Job.__name__, now.month, now.day),
        'bgFolder': '//background/INRIA/',
        'outputFolder': '/q/cache/lsp_2d_3d/render_output/',
        'comment': 'Use 2D joint annotation of LSP to manipulate human model',
        'mode': 'ijd'
    })

    j = L23Job()
    for k in jobInfo:
        setattr(j, k, jobInfo[k])

    defTask = L23Task() # Default task
    defTask.mode = jobInfo.mode

    tasks = []

    Shirt.setFolder(j.shirtFolder)
    nShirt = len(Shirt.textures)

    Pants.setFolder(j.pantsFolder)
    nShirt = len(Pants.textures)

    Bg.setFolder(j.bgFolder)
    nBG = len(Bg.textures)

    for i in range(1, 2001):
        t = copy.copy(defTask)
        t.LSPPoseId = i
        t.pantsId = random.randrange(0, nShirt)
        t.bgId = random.randrange(0, nBG)
        t.tshirtId = random.randrange(0, nShirt)
        tasks.append(t)

    j.tasks = tasks
    j.save(bpyPathHelper(j.filename))


class L23Job(Job):
    def setupScene(self):
        # This depends on the specific job requirement
        # Meta information is only useful in this section
        Shirt.setFolder('//textures/shirt')
        Pants.setFolder('//textures/pants')
        Bg.setFolder(self.bgFolder)
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

    def setPose(self):
        import tenon.puppet
        logging.info('Animate to Pose %s' % self.LSPPoseId)
        tenon.puppet.animateCP(int(self.LSPPoseId))
        # tenon.pose.animateEditBone(int(self.LSPPoseId))
        # This is for debugging

    def execute(self):
        self.prefix = 'im%04d' % (int(self.LSPPoseId)) # TODO: Let it start from 1

        # if self.isRendered():
        #     logging.warning('%s exists, skip this task' % self.prefix)
        #     return

        # TODO: timing this script to boost speed

        logging.info('Change background to %s' % self.bgId)
        Bg.changeById(self.bgId)

        Hair.randomChange()
        Skin.randomChange()
        # Shirt.changeById(self.tshirtId)
        # Pants.changeById(self.pantsId)
        Shirt.randomChange()
        Pants.randomChange()
        Lighting.setup()  # Randomly update the lighting

        self.setPose()

        self.render()