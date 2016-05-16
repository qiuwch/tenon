import matplotlib.pyplot as plt
import os

lsp_tpl = os.path.expanduser('~/Dropbox/dataset/lsp/lsp_dataset/images/im%04d.jpg')
render_tpl = os.path.expanduser('~/Dropbox/workspace/graphics_for_vision/tenon/cache/lsp_synthesized/imgs/%04d.png')
cropped_tpl = os.path.expanduser('~/Dropbox/workspace/graphics_for_vision/tenon/cache/lsp_synthesized/cropped/%04d.png')

i = 1
def show_compare(i):
    lsp_filename = lsp_tpl % i
    render_filename = render_tpl % i
    cropped_filename = cropped_tpl % i

    lsp_im = plt.imread(lsp_filename)
    render_im = plt.imread(render_filename)
    cropped_im = plt.imread(cropped_filename)

    plt.subplot(1, 2, 1)
    plt.imshow(lsp_im)
    plt.axis('off')
    plt.subplot(1, 2, 2)
    # plt.imshow(render_im)
    plt.imshow(cropped_im)
    plt.axis('off')
    plt.show()
    plt.savefig('compare.png')

for i in range(1, 10):
    show_compare(i)
