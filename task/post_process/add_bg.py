import glob
import matplotlib.pyplot as plt
import os
import pandas as pd

nobgfiles = glob.glob('/q/cache/tenon/rendered/no_bg/imgs/*.png')

for i in nobgfiles:
    print(i)
    im = plt.imread(i)
    plt.imshow(im)

    # Load joint location
    csvfile = '/q/cache/tenon/rendered/no_bg/joint/im0001.csv'
    df = pd.read_csv(csvfile, header=None)

    def cropPatch():
        for i in len(df[0]):
            jointName = df[0][i]
            x = df[1][i]
            y = df[2][i]

            plt.plot(x, y)

    plt.savefig('%s.png' % os.path.basename(i))

