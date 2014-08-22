from spe


img = open_image('/home/vortex/Downloads/sample-data-master/92AV3C.lan').load()


gt = open_image('/home/vortex/Downloads/sample-data-master/92AV3GT.GIS').read_band(0)

v = imshow(classes=gt)