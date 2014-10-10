import xlrd
import glob
import os
from pgeo.utils.filesystem import unzip, get_filename

xls_parser = {
    # "file_path": "DEU-2012-2000-v1.2.xls",
    "file_path": "aus-2014-crf-15apr.zip",
    "parser": [
        {
            "sheet_name"         : "Table4.A",
            "rows"               : [8, 10, 11, 16, 17, 18, 19, 20, 21, 22, 23],
            "col_label"          : 0,
            "col_value"          : 1,
            "label_element_text" : "Activity data",
            "translate_labels"   : False,
            "lang"               : "E"
        },
        {
            "sheet_name"         : "Table4.A",
            "rows"               : [8, 10, 11, 16, 17, 18, 19, 20, 21, 22, 23],
            "col_label"          : 0,
            "col_value"          : 4,
            "label_element_text" : "Implied Emission Factor",
            "translate_labels"   : False,
            "lang"               : "E"
        },
        {
            "sheet_name"         : "Summary2",
            "rows"               : [27],
            "col_label"          : 0,
            "col_value"          : 7,
            "label_element_text" : "Implied Emission Factor",
            "translate_labels"   : False,
            "lang"               : "E"
        }
    ]
}


class GHGXlsParser():

    def __init__(self, xls_parser):
        self.xls_parser = xls_parser

    def process(self):
        # process zip file
        path = unzip(self.xls_parser["file_path"])
        files_path = glob.glob(os.path.join(path, "*"))
        data = []
        for file_path in files_path:
            print file_path
            self.xls_parser["file_path"] = file_path
            d = {}
            d["name"], d["year"] = self.parse_filename(get_filename(file_path))
            d["data"] = self.process_xls()
            data.append(d)
        return data

    def parse_filename(self, filename):
        split = filename.split("-")
        return split[0], split[2]

    def process_xls(self):
        obj = []
        workbook = xlrd.open_workbook(self.xls_parser["file_path"])
        for p in self.xls_parser["parser"]:
            sheet = workbook.sheet_by_name(p["sheet_name"])
            rows = p["rows"]
            col_label = p["col_label"]
            col_value = p["col_value"]
            label_element_text = p["label_element_text"]
            data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
            for row in rows:
                obj.append(["code?", str(data[row][col_label]), str(data[row][col_value]), label_element_text])
        return obj


ghg = GHGXlsParser(xls_parser)
print ghg.process()