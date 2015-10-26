import logging
import bpy


def getObject(objectName):
	obj = bpy.data.objects.get(objectName)
	if not obj:
		logging.error('Model %s does not exist' % objectName)

	return obj

class Models: # TODO: consider cache for here
    def modelName():
        keys = bpy.data.armatures.keys()
        logging.debug('Get %d armatures %s' % (len(keys), keys))

        modelNames = []
        for k in keys:
            humanModel = bpy.data.objects.get(k)
            if humanModel:
                logging.debug('Model %s exists' % k)
                modelNames.append(k)
            else:
                logging.debug('Model %s not exist' % k)

        if len(modelNames) != 1:
            logging.error('%d is invalid number of human models' % len(modelNames))

        return modelNames[0]

    def humanModel():
    	return getObject(Models.modelName())

    def bodyMesh():
    	return getObject('%s:Body' % Models.modelName())

    def upperCloth():
        return getObject('%s:short01' % Models.modelName())

    def lowerCloth():
    	return getObject('%s:jeans01' % Models.modelName())

    def hair():
    	return getObject('%s:mhair02' % Models.modelName())
