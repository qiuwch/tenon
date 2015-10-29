import logging
import bpy


def getObject(objectName):
	obj = bpy.data.objects.get(objectName)
	if not obj:
		logging.error('Model %s does not exist' % objectName)

	return obj

class Models: # TODO: consider cache for here
    @classmethod
    def modelName(cls):
        keys = bpy.data.armatures.keys()
        logging.debug('Get %d armatures %s' % (len(keys), keys))

        modelNames = []
        for k in keys:
            humanModel = bpy.data.objects.get(k)
            humanBody = bpy.data.objects.get('%s:Body' % k)
            if humanModel and humanBody:
                logging.debug('Model %s exists' % k)
                modelNames.append(k)
            else:
                logging.debug('Model %s not exist' % k)

        if len(modelNames) != 1:
            logging.error('%d is invalid number of human models' % len(modelNames))
            return ''
            
        return modelNames[0]

    @classmethod
    def humanModel(cls):
    	return getObject(cls.modelName())

    @classmethod
    def bodyMesh(cls):
    	return getObject('%s:Body' % cls.modelName())

    @classmethod
    def upperCloth(cls): # TODO: consider rewrite this, not robust
        return getObject('%s:short01' % cls.modelName())

    @classmethod
    def lowerCloth(cls):
    	return getObject('%s:jeans01' % cls.modelName())

    @classmethod
    def hair(cls):
    	return getObject('%s:mhair02' % cls.modelName())
