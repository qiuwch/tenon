import os
import matplotlib.pyplot as plt

lspfile_ptr = os.path.expanduser('~/Dropbox/dataset/lsp/lsp_dataset/images/im%04d.jpg')
l23file_ptr = os.path.expanduser('~/Dropbox/dataset/synthetic/l23_v2/imgs/im%04d.png')

for i in range(1, 2001):
    print(i)
    lsp_im = plt.imread(lspfile_ptr % i)
    l23_im = plt.imread(l23file_ptr % i)
    plt.subplot(2, 1, 1)
    plt.imshow(lsp_im)
    plt.axis('off')
    plt.subplot(2, 1, 2)
    plt.imshow(l23_im)
    plt.axis('off')
    plt.savefig('compare/%d.png' % i)

