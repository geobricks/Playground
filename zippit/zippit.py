import glob
import os
import zipfile


# create zip file with subfolders
def createZip(outputFilePath, foldersToZip, archiveType="zip"):
    zipfilename = "%s.%s" % (outputFilePath, archiveType)
    print "zip filename: %s" % zipfilename
    zfile = zipfile.ZipFile(os.path.join(zipfilename), 'w', zipfile.ZIP_DEFLATED)
    for folder in foldersToZip:
        print "processing: %s"  % folder
        if not os.path.exists(folder):
            print "ERROR, folder doesn't exists: %s" % folder
        # rootlen => zipped files don't have a deep file tree
        rootlen = len(folder) + 1
        for base, dirs, files in os.walk(folder):
            for file in files:
                dirname = os.path.split(folder)[1]
                fn = os.path.join(base, file)
                zfile.write(fn, os.path.join(dirname, fn[rootlen:]))
    zfile.close()
    return zipfilename


# create GHG products
def createGHGProducts(obj):
    inputPath = obj["inputPath"]
    outputPath = obj["outputPath"]
    archiveType = obj["archiveType"]
    zips = obj["zippit"]

    # Get all country codes (to be used in the folder input and output folder construction
    # TODO: how to make generic?
    codes_folders = glob.glob(os.path.join(inputPath, "*"))
    codes = []
    for folder in codes_folders:
        codes.append(os.path.split(folder)[1])

    # create the zip files
    for to_zip in zips:
        print to_zip["name"]
        outputFilename = to_zip["filename"]
        outputFolderName = to_zip["folderName"]

        # for each country code
        for code in codes:

            # TODO: get all country codes (to be used in the folder input construction)

            # TODO add to the path gaul code i.e. 4326/product/12/product_name.zip
            outputFolderPath = os.path.join(outputPath, outputFolderName)
            if not os.path.isdir(outputFolderPath):
                os.makedirs(outputFolderPath)
            outputFolderPath = os.path.join(outputPath, outputFolderName)

            # Create output folder and subfolder
            if not os.path.isdir(outputFolderPath):
                os.makedirs(outputFolderPath)
            outputFolderPath = os.path.join(outputFolderPath, code)
            if not os.path.isdir(outputFolderPath):
                os.makedirs(outputFolderPath)

            outputFilePath = os.path.join(outputFolderPath, outputFilename)

            # delete file if already exists
            if os.path.isfile(outputFilePath):
                os.remove(outputFilePath)

            folders_to_zip = []
            for folder in to_zip["folders"]:
                # TODO add to the path gaul code i.e. inputPath/12/inputFolder
                folders_to_zip.append(os.path.join(inputPath, code, folder))

            createZip(outputFilePath, folders_to_zip, archiveType)
            #print outputFilePath



obj = {
    "inputPath": "/home/vortex/Desktop/LAYERS/ghg/process_data/test_input/",
    "outputPath": "/home/vortex/Desktop/LAYERS/ghg/process_data/test_output2/4326",
    "archiveType": "zip",
    # this is done in this case for each country
    "zippit": [
        {
           "name": "GFED4 Burned Areas (dry matter)",
           "folderName": "gfed4_burned_areas_dry_matter",
           "filename": "gfed4_burned_areas_dry_matter",
           "metadataFilesPath": [],
           "folders": [
               "CH4_Emissions_Burning_ClosedShrublands",
               "CH4_Emissions_Burning_Grasslands",

           ],
        },
        # {
        #     "name": "GFED4 Burned Areas (dry matter)",
        #     "folderName": "gfed4_burned_areas_dry_matter2",
        #     "filename": "gfed4_burned_areas_dry_matter2",
        #     "metadataFilesPath": [],
        #     "folders": [
        #         "CH4_Emissions_Burning_ClosedShrublands",
        #         "CH4_Emissions_Burning_Grasslands",
        #
        #         ],
        # }
    ]
}


createGHGProducts(obj)