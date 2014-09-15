from spectral import *
import pylab



img = open_image('/home/vortex/Downloads/sample-data-master/92AV3C.lan').load()


gt = open_image('/home/vortex/Downloads/sample-data-master/92AV3GT.GIS').read_band(0)

v = imshow(classes=gt)

classes = create_training_classes(img, gt)

gmlc = GaussianClassifier(classes)

clmap = gmlc.classify_image(img)

v = imshow(classes=clmap)

gtresults = clmap * (gt != 0)

v = imshow(classes=gtresults)


# Minimum distance Classification