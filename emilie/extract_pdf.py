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


def scrap_pdf(path, csvwriter, text_file, do_csv=False):
    print path
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    process_pdf(rsrcmgr, device, fp)
    fp.close()
    device.close()
    text = retstr.getvalue()

    # writing converted pdf to text file
    text_file.write(text)

    # check the words in the text
    print "check dictionary"
    result = False
    if do_csv is True:
        result = check_dictionary(text.split(), path, csvwriter)

    retstr.close()
    return result


def check_dictionary(words, file_path, csvwriter):
    # header
    csvwriter.writerow([file_path])
    csvwriter.writerow(["Word found", "From the word", "Word Weight"])

    total_probability = 0
    print "looping"
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
                    csvwriter.writerow([w, d, word_weight])
                    total_probability += word_weight

    if total_probability == 0.0:
        csvwriter.writerow("NOTHING FOUND!!!")
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


def check_pdf(path):
    filenames = glob.glob(path + "/*.pdf")
    for filepath in filenames:
        check_pdf(filepath)
        #filename = "/media/vortex/disk/music/Africa/Algeria_2013/Projet questionnaire RGA 2013.pdf"



def main_all():

    path = "/home/vortex/Desktop/emilie/Africa/"

    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".pdf"):
                filepath = os.path.join(root, name)
                path, filename, name = get_filename(filepath, True)
                report_csv = os.path.join(path, name + ".csv")
                pdf_to_text = os.path.join(path, name + ".text")
                print os.path.join(path, name + ".text_ERROR_PARSING")
                if os.path.isfile(os.path.join(path, name + ".text_ERROR_PARSING")) is False:
                    with open(pdf_to_text, "wb") as text_file:
                        if os.path.getsize(report_csv) is 0:
                            with open(report_csv, 'wb') as csvfile:
                                csvwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                if os.path.getsize(report_csv) is 0:
                                    result = scrap_pdf(filepath, csvwriter, text_file)
                                    if result is False:
                                        os.rename(report_csv, report_csv+ "_NOTHING_FOUND")
            else:
                print "File error parsed found"

def convert_pdfs(path):
    # path = "/home/vortex/Desktop/emilie/Africa/"
    # path = "/home/vortex/Desktop/emilie/"

    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".pdf"):
                filepath = os.path.join(root, name)
                path, filename, name = get_filename(filepath, True)
                pdf_to_text = os.path.join(path, name + ".text")
                if os.path.isfile(os.path.join(path, name + ".text_ERROR_PARSING")) is False:
                    with open(pdf_to_text, "a") as text_file:
                        if os.path.getsize(pdf_to_text) is 0:
                            try:
                                result = scrap_pdf(filepath, None, text_file)
                            except:
                                os.rename(pdf_to_text, pdf_to_text+ "_ERROR_PARSING")
                                print "Error parsing: " + filepath
                else:
                    print os.path.join(path, name + ".text_ERROR_PARSING")


#path = "/home/vortex/Desktop/emilie/Europe/"
path = "/home/vortex/Desktop/emilie/Asia/"
convert_pdfs(path)
