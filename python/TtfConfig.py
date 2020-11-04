#!/usr/bin/env python3
#encoding=utf-8

class TtfConfig():
    VERSION = "1.047"
    PROCESS_MODE = "SPRING"
    #PROCESS_MODE = "MEATBALL"

    STYLE_INDEX = 4
    STYLE_ARRAY = ["Black","Bold","SemiBold","Medium","Regular","Light","ExtraLight"]
    STYLE=STYLE_ARRAY[STYLE_INDEX]

    DEFAULT_COORDINATE_VALUE = -9999

    # unicode in field
    # 1 to 3
    UNICODE_FIELD = 2

    #BMP_PATH = '/Users/chunyuyao/Documents/noto/bmp'
    # don't use bmp feature.
    BMP_PATH = None

    # for X,Y axis equal compare.
    # each 100 px, +- 8 px.
    EQUAL_ACCURACY_MIN = 3
    EQUAL_ACCURACY_PERCENT = 0.08

    # for rule#101
    # in regular=80 to 57
    # for case:.2639 「真」被擠壓為38
    # for case:uni7665 癥，中間的「山」為29
    ROW_TRIANGLE_HEIGHT_MIN = 26
    # for case:uni4E00 一：104
    ROW_TRIANGLE_HEIGHT_MAX = 115
    
    # in regular=121 to 86
    # for uni5A64「婤」, value:63, 因為被截斷
    # for uni8061,聡: 48
    ROW_TRIANGLE_SLIDE_MIN = 44
    # for case:uni4E00 一：154
    ROW_TRIANGLE_SLIDE_MAX = 165

    # in regular=29,31 to (.26356, 片)47, (case.10924 公, Regular) 73
    ROW_TRIANGLE_CHIN_MIN = 21
    # in regular=85 (uni6C43 汃)
    ROW_TRIANGLE_CHIN_MAX = 95

    # in regular=46, (case.11158 分, Regular) 69
    ROW_TRIANGLE_FLAT_CHIN_MIN = 26
    ROW_TRIANGLE_FLAT_CHIN_MAX = 84

    # for rule#101
    # in regular=103 to 112
    STROKE_WIDTH_MIN = 43
    STROKE_WIDTH_MAX = 133

    # in regular=45 to 42, (case:.17729, 後) 34, (case:.18791, 應) 26
    # for uni8763 蝣的子，19
    COL_TRIANGLE_CHIN_MIN = 17
    COL_TRIANGLE_CHIN_MAX = 55

    def apply_weight_setting(self):
        self.STYLE=self.STYLE_ARRAY[self.STYLE_INDEX]

        if self.STYLE in ["Black"]:
            # black style, for case:三, 131
            self.ROW_TRIANGLE_HEIGHT_MIN = 28
            self.ROW_TRIANGLE_HEIGHT_MAX = 151

            # black style, for case:三, 186
            self.ROW_TRIANGLE_SLIDE_MIN = 54
            self.ROW_TRIANGLE_SLIDE_MAX = 200

            # black style, for case:三, 34, (case.10924 公, Black) 104
            self.ROW_TRIANGLE_CHIN_MIN = 21
            self.ROW_TRIANGLE_CHIN_MAX = 125

            # in regular=46
            self.ROW_TRIANGLE_FLAT_CHIN_MIN = 26
            self.ROW_TRIANGLE_FLAT_CHIN_MAX = 146

            # for rule#101
            # in regular=103 to 112, (case.10924 公, Black) 216
            self.STROKE_WIDTH_MIN = 63
            self.STROKE_WIDTH_MAX = 231
            
            # in regular=45 to 42
            self.COL_TRIANGLE_CHIN_MIN = 25
            self.COL_TRIANGLE_CHIN_MAX = 85

        if self.STYLE in ["Bold"]:
            # in regular=80 to 57
            self.ROW_TRIANGLE_HEIGHT_MIN = 28
            self.ROW_TRIANGLE_HEIGHT_MAX = 141
            # in regular=121 to 86
            self.ROW_TRIANGLE_SLIDE_MIN = 52
            self.ROW_TRIANGLE_SLIDE_MAX = 190
            # in regular=29,31 to (.26356, 片)47
            self.ROW_TRIANGLE_CHIN_MIN = 21
            self.ROW_TRIANGLE_CHIN_MAX = 116

            # in regular=46
            self.ROW_TRIANGLE_FLAT_CHIN_MIN = 26
            self.ROW_TRIANGLE_FLAT_CHIN_MAX = 126

            # for rule#101
            # in regular=103 to 112, (case.10924 公, Black) 216
            self.STROKE_WIDTH_MIN = 58
            self.STROKE_WIDTH_MAX = 208

            # in regular=45 to 42
            self.COL_TRIANGLE_CHIN_MIN = 23
            self.COL_TRIANGLE_CHIN_MAX = 85


        if self.STYLE in ["SemiBold","Medium"]:
            # in regular=80 to 57
            self.ROW_TRIANGLE_HEIGHT_MIN = 28
            self.ROW_TRIANGLE_HEIGHT_MAX = 130
            # in regular=121 to 86
            self.ROW_TRIANGLE_SLIDE_MIN = 46
            self.ROW_TRIANGLE_SLIDE_MAX = 180
            # in regular=29,31 to (.26356, 片)47
            self.ROW_TRIANGLE_CHIN_MIN = 21
            self.ROW_TRIANGLE_CHIN_MAX = 106

            # in regular=46
            self.ROW_TRIANGLE_FLAT_CHIN_MIN = 26
            self.ROW_TRIANGLE_FLAT_CHIN_MAX = 106

            # for rule#101
            # in regular=103 to 112
            self.STROKE_WIDTH_MIN = 53
            self.STROKE_WIDTH_MAX = 183

            # in regular=45 to 42
            self.COL_TRIANGLE_CHIN_MIN = 20
            self.COL_TRIANGLE_CHIN_MAX = 75

        if self.STYLE in ["Light","ExtraLight"]:
            # in regular=80 to 57
            self.ROW_TRIANGLE_HEIGHT_MIN = 24
            self.ROW_TRIANGLE_HEIGHT_MAX = 110
            # in regular=121 to 86
            self.ROW_TRIANGLE_SLIDE_MIN = 39
            self.ROW_TRIANGLE_SLIDE_MAX = 160
            # in regular=29,31 to (.26356, 片)47
            self.ROW_TRIANGLE_CHIN_MIN = 18
            self.ROW_TRIANGLE_CHIN_MAX = 88

            # in regular=46
            self.ROW_TRIANGLE_FLAT_CHIN_MIN = 22
            self.ROW_TRIANGLE_FLAT_CHIN_MAX = 80

            # for rule#101
            # in regular=103 to 112
            self.STROKE_WIDTH_MIN = 38
            self.STROKE_WIDTH_MAX = 133

            # in regular=45 to 42
            self.COL_TRIANGLE_CHIN_MIN = 17
            self.COL_TRIANGLE_CHIN_MAX = 55

    def __init__(self, weight_code):
        import datetime

        self.STYLE_INDEX = int(weight_code)
        self.apply_weight_setting()
        print("Transform Mode:", self.PROCESS_MODE)
        print("Transform Style:", self.STYLE)
        print("Transform Version:", self.VERSION)
        print("Transform Time:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def hello(self):
        print("world!")