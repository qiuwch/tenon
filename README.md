Project tenon is a set of python scripts to automatically control blender rendering.

After clone this repo to disk. Run `demo.py` to render a bunch of images to data folder. The output of blender will be redirected to `blender_stdout.log`. If the result is not as expected, check the log file for diagnosis. If an error shows 'can not find blender', configure `tenon/setting.py` to specify `blender` binary.

These scripts can be used in a headless mode for rendering, or be loaded into blender for interactive manipulation.

# Example: Render synthetic human images

Before using this tool, makehuman addons for blender needs to be installed and configured correctly first. Otherwise the synthetic human pose will be very weird.

## Install makehuman blender tools
1. The tools should be downloaded from [here](http://www.makehuman.org/download.php)

2. The addons should be enabled in blender
- menu: file -> user preferences -> file -> auto execution, check `Auto Run Python Scripts`.
- menu: file -> add-ons -> use search function to find "Make Target" and "MakeWalk", select them.
- click `Save User Settings`

## Synthesize human images
```bash
cd examples
python ./demo_lsp_pose.py
```

Rendered images will be saved to examples/lsp
