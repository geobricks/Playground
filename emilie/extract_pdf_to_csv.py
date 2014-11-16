
from pdfminer.pdfparser import PDFDocument, PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, process_pdf
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from cStringIO import StringIO
import csv
import os
import glob
import ntpath
import shutil

report_file = "/home/vortex/Desktop/emilie/report.csv"

dictionary = {
    "en": {
        "stock": 1.0,
        "storage": 1.0,
        "cereal stock": 1.0,
        "left over": "1.0",
        "infrastructure": 0.1,
        "cereal": 0.1,
        "grain": 0.1,
        "facilities": 0.5,
        "capacity": 0.5,
        "facility": 0.5
    },
    "fr": [],
    "es": []
}

black_list = {
    "livestock"
}


def scrap_text_file(text_file, csvwriter):
    file = open(text_file, 'r')
    text = file.read()
    return check_dictionary(text.split(), text_file, csvwriter)


def check_dictionary(words, file_path, csvwriter):
    # header
    csvwriter.writerow([file_path])
    csvwriter.writerow(["Word found", "From the word", "Word Weight"])

    total_probability = 0
    index = 0
    for w in words:
        for d in dictionary["en"]:
            if d in w.lower():
                check_black_list = True
                for bl in black_list:
                    if bl in w.lower():
                        check_black_list = False
                        break;

                if check_black_list:
                    print d, w, " add to report"
                    word_weight = dictionary["en"][d]
                    try:
                        csvwriter.writerow([words[index-1] + " " + w + " " + words[index+1], d, word_weight])
                    except:
                        csvwriter.writerow([w, d, word_weight])
                    total_probability += word_weight
        index = index+1
    if total_probability == 0.0:
        csvwriter.writerow(["NOTHING FOUND!!!"])
        return False
    else:
        csvwriter.writerow(["Total Probability", total_probability])
        return True

        # csvwriter.writerow([])
        # csvwriter.writerow(["--------------------------"])


def get_filename(filepath, extension=False):
    drive, path = os.path.splitdrive(filepath)
    path, filename = os.path.split(path)
    name = os.path.splitext(filename)[0]
    if extension is True:
        return path, filename, name
    else:
        return name


def main_all(path):

    #path = "/home/vortex/Desktop/emilie/Africa/"
    #path = "/home/vortex/Desktop/emilie/North and Central America/"
    counter_all = 0
    counter_true = 0
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".text"):
                counter_all = counter_all+1
                filepath = os.path.join(root, name)
                path, filename, name = get_filename(filepath, True)
                report_csv = os.path.join(path, name + ".csv")
                if os.path.isfile(report_csv + "_NOTHING_FOUND") is True:
                    os.remove(report_csv + "_NOTHING_FOUND")


                with open(report_csv, 'wb') as csvfile:
                    #if os.path.getsize(report_csv) is 0:
                    print filepath
                    csvwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    #if os.path.getsize(report_csv) is 0:
                    result = scrap_text_file(filepath, csvwriter)
                    if result is False:
                        print "FALSE: ", report_csv
                        os.rename(report_csv, report_csv+ "_NOTHING_FOUND")
                    else:
                        counter_true = counter_true+1
                        print "TRUE: ", report_csv

    print str(counter_true) + "/" + str(counter_all)


def clean_unused_folders(path):
    paths = glob.glob(path + "/*")
    for p in paths:
        if os.path.isdir(p):
            sub_paths = glob.glob(p + "/*")
            for sub_path in sub_paths:
                if os.path.isdir(sub_path):
                    if "questionnaire" not in sub_path.lower():
                        print sub_path
                        shutil.rmtree(sub_path)

path = "/home/vortex/Desktop/emilie/"
#clean_unused_folders(path)
main_all(path)