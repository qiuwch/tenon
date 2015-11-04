from tenon.tasks.l23 import L23Job

def ls():
	jobs = activeJobs()
	return jobs

# Define available jobs here
def activeJobs():
	jobs = []

	l23_color_cloth = L23Job()
	l23_color_cloth.cloth = 'color'
	l23_color_cloth.name = 'L23 dataset with pure color cloth'
	jobs.append(l23_color_cloth)

	l23_texture_cloth = L23Job()
	l23_texture_cloth.cloth = 'texture'
	l23_texture_cloth.name = 'L23 dataset with Texture pattern as cloth'
	jobs.append(l23_texture_cloth)

	return jobs



