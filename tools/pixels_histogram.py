import matplotlib.pyplot as plt

def draw_histogram(imageName):
    img = plt.imread(imageName)
    plt.hist(img.ravel(), bins=256, range=(0.0, 1.0), fc='k', ec='k')
    plt.show()


