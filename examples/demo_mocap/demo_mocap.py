# Demo script to show how to generate random lighting
import sys, os
sys.path.append(os.path.expanduser('~/Dropbox/workspace/tenon/code'))
import tenon

rootdir = './../../'

def main():
    '''
    Manually set up:
    - Let camera track the head of human model
    '''
    tenon.render.DepthMode.disable()
    tenon.render.writevideo('video/')
    tenon.logging.info('Complete rendering video')

    tenon.render.DepthMode.enable()
    tenon.render.writevideo('depth/')
    tenon.logging.info('Complete rendering depth')

    # Output the joint location
    for fid in range(10):
        tenon.obj.scene.frame_set(fid)
        # set to frame
        joints = exportJoint() # TODO: update this with JointInfo class in lsppose
        serializeJointInfo('joint/%04d.csv' % fid, joints)


if not tenon.inblender():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('scenefile', default = '../../../data/mocap_demo_scene.blend', help = 'The scene file for rendering')

    args = parser.parse_args()

    tenon.run(__file__, args.scenefile)
else:
    main()
