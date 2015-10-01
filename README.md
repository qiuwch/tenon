# README
This project warps blender python api for synthetic images rendering. It provides basic functionality to manipulate a blender scene.

## How to generate images with LSP format
1. Define the task file, which contains the definition of the scene.
TODO: Extend the task format. Make sure to include depth in the mode format.

2. Import tenon into blender and run `tenon.task.run(num)`. num is the number of images to generate.

3. Run the matlab script `prepare_lsp.m` to post process the images. The post processing contains cropping, resizing and convert the annotation format.
