#!env python
# Utility script to convert csv from pandas format to Matlab readable format (no header and id column)
import pandas as pd
from config import JOINT_FILENAME

def toMATLAB(jointFilename):
	mapping = {
		'hand.fk.L': 'L.wrist',
		'upper_arm.fk.L': 'L.shoulder',
		'forearm.fk.R': 'R.elbow',
		'upper_arm.fk.R': 'R.shoulder',
		'head': 'HeadTop',
		'forearm.fk.L': 'L.elbow',
		'thigh.fk.L': 'L.hip',
		'shin.fk.L': 'L.knee',
		'thigh.fk.R': 'R.hip',
		'hand.fk.R': 'R.wrist',
		'neck': 'Neck',
		'shin.fk.R': 'R.knee',
		'foot.fk.R': 'R.ankle',
		'foot.fk.L': 'L.ankle',
	}
	reverseMapping = dict((v,k) for k,v in mapping.iteritems())


	order = [
		'R.ankle',
		'R.knee',
		'R.hip',
		'L.hip',
		'L.knee',
		'L.ankle',
		'R.wrist',
		'R.elbow',
		'R.shoulder',
		'L.shoulder',
		'L.elbow',
		'L.wrist',
		'Neck',
		'HeadTop'
	]


	df = pd.read_csv(jointFilename)
	keys = [reverseMapping[v] for v in order]

	newKeys = []
	for k in keys:
		newKeys += [k + '.x', k + '.y']

	newDf = df[newKeys] # Manipulate the order
	newDf.to_csv(jointFilename.split('.')[-2] + '-MATLAB.csv', header=False, index=False);

if __name__ == '__main__':
	toMATLAB(JOINT_FILENAME)