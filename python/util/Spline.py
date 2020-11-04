#!/usr/bin/env python3
#encoding=utf-8

from . import spline_util

class Spline():
    config = None

    def __init__(self):
        pass

    def check_clockwise(self, spline_dict):
        clockwise = True
        area_total=0
        poly_lengh = len(spline_dict['dots'])
        #print('check poly: (%d,%d)' % (poly[0][0],poly[0][1]))
        for idx in range(poly_lengh):
            #item_sum = ((poly[(idx+1)%poly_lengh][0]-poly[(idx+0)%poly_lengh][0]) * (poly[(idx+1)%poly_lengh][1]-poly[(idx+0)%poly_lengh][1]))
            item_sum = ((spline_dict['dots'][(idx+0)%poly_lengh]['x']*spline_dict['dots'][(idx+1)%poly_lengh]['y']) - (spline_dict['dots'][(idx+1)%poly_lengh]['x']*spline_dict['dots'][(idx+0)%poly_lengh]['y']))
            #print(idx, poly[idx][0], poly[idx][1], item_sum)
            area_total += item_sum
        #print("area_total:",area_total)
        if area_total >= 0:
            clockwise = not clockwise
        return clockwise

    def assign_config(self, config):
        self.config = config

    def hello(self):
        print("world")


    def detect_bmp_data_top(self, bmp_image):
        threshold=0
        data_top=0
        #print("bmp_image.shape:", bmp_image.shape)
        if not bmp_image is None:
            # for PIL
            h,w = bmp_image.height,bmp_image.width

            is_match_data = False
            for y in range(h-2):
                if y==0:
                    continue
                if y>=h-3:
                    continue

                for x in range(w):
                    if bmp_image.getpixel((x, y)) == threshold and bmp_image.getpixel((x, y+1)) == threshold and bmp_image.getpixel((x, y-1)) == threshold:
                       #print("bingo:", x, y-1, bmp_image[x, y])
                       is_match_data = True
                       data_top=y-1
                       break
                if is_match_data:
                    break

        #print("data_top:", data_top)
        return data_top

    def detect_bmp_data_top_cv(self, bmp_image):
        threshold=0
        data_top=0
        #print("bmp_image.shape:", bmp_image.shape)
        if not bmp_image is None:
            # for OpenCV
            h, w, d = bmp_image.shape

            is_match_data = False
            for y in range(h-2):
                if y==0:
                    continue
                if y>=h-3:
                    continue

                for x in range(w):
                    if bmp_image[y, x][0] == threshold and bmp_image[y+1, x][0] == threshold and bmp_image[y-1, x][0] == threshold:
                       #print("bingo:", x, y-1, bmp_image[x, y])
                       is_match_data = True
                       data_top=y-1
                       break
                if is_match_data:
                    break

        #print("data_top:", data_top)
        return data_top


    def trace(self, stroke_dict, unicode_int, bmp_image):
        #print("trace")
        #print(stroke_dict)
        is_modified = False

        glyph_margin={}

        glyph_margin["top"]  = None
        glyph_margin["bottom"] = None
        glyph_margin["left"] = None
        glyph_margin["right"] = None

        if 1 in stroke_dict:
           for key in stroke_dict.keys():
                spline_dict = stroke_dict[key]
                self.detect_margin(spline_dict)

                if glyph_margin["top"] is None:
                    glyph_margin["top"]  = stroke_dict[key]["top"]
                    glyph_margin["bottom"] = stroke_dict[key]["bottom"]
                    glyph_margin["left"] = stroke_dict[key]["left"]
                    glyph_margin["right"] = stroke_dict[key]["right"]

                if glyph_margin["top"] < spline_dict["top"]:
                    glyph_margin["top"]  = spline_dict["top"]
                if glyph_margin["bottom"] > spline_dict["bottom"]:
                    glyph_margin["bottom"] = spline_dict["bottom"]
                if glyph_margin["left"] > spline_dict["left"]:
                    glyph_margin["left"] = spline_dict["left"]
                if glyph_margin["right"] < spline_dict["right"]:
                    glyph_margin["right"] = spline_dict["right"]

        y_offset = 880
        if not bmp_image is None:
            # maybe is empty glyph or control char.
            FF_TOP=glyph_margin["top"]
            
            BMP_TOP=None
            if not FF_TOP is None:
                BMP_TOP=self.detect_bmp_data_top(bmp_image)
                y_offset = (900 - FF_TOP) - BMP_TOP
            
            #print("FF_TOP=",FF_TOP)
            #print("bmp_top=",BMP_TOP)
            #print("y_offset=",y_offset)

        preprocess_result = self.preprocess(stroke_dict, unicode_int)
        if preprocess_result:
            is_modified = True

        for key in stroke_dict.keys():
            spline_dict = stroke_dict[key]
            #print("key:", key, 'code:', spline_dict['dots'][0])
            # for debug
            #if key==5:
            if True:
                clockwise = self.check_clockwise(spline_dict)
                #print("clockwise:", clockwise)
                normalize_result = self.normalize(stroke_dict, key, unicode_int, bmp_image, y_offset)
                if normalize_result:
                    is_modified = True
 
                if clockwise:
                    trace_result = self.trace_black_block(stroke_dict, key, unicode_int, bmp_image, y_offset)
                    if trace_result:
                        is_modified = True
                else:
                    trace_result = self.trace_white_block(stroke_dict, key, unicode_int, bmp_image, y_offset)
                    if trace_result:
                        is_modified = True

            stroke_dict[key] = spline_dict

        return is_modified, stroke_dict

    def detect_margin(self, spline_dict):
        default_int = -9999

        margin_top=default_int
        margin_bottom=default_int
        margin_left=default_int
        margin_right=default_int
        for dot_dict in spline_dict['dots']:
            x=dot_dict['x']

            if x != default_int:
                if margin_right==default_int:
                    # initail assign
                    margin_right=x
                else:
                    # compare top
                    if x > margin_right:
                        margin_right = x

                if margin_left==default_int:
                    # initail assign
                    margin_left=x
                else:
                    # compare bottom
                    if x < margin_left:
                        margin_left = x

            y=dot_dict['y']
            if y !=default_int:
                if margin_top==default_int:
                    # initail assign
                    margin_top=y
                else:
                    # compare top
                    if y > margin_top:
                        margin_top = y

                if margin_bottom==default_int:
                    # initail assign
                    margin_bottom=y
                else:
                    # compare bottom
                    if y < margin_bottom:
                        margin_bottom = y

        spline_dict["top"]  = margin_top
        spline_dict["bottom"] = margin_bottom
        spline_dict["left"] = margin_left
        spline_dict["right"] = margin_right

    def split_spline(self, stroke_dict, unicode_int):
        redo_split = False
        from . import Rule1_Split_Spline

        for key in stroke_dict.keys():
            spline_dict = stroke_dict[key]
            #print("key:", key, 'code:', spline_dict['dots'][0])
            # for debug
            #if key==5:
            if True:
                clockwise = self.check_clockwise(spline_dict)
                #print("clockwise:", clockwise)
                if clockwise:
                    # format code.
                    # start to travel nodes for [RULE #1]
                    # format curve coner as l conver

                    ru1=Rule1_Split_Spline.Rule()
                    ru1.assign_config(self.config)

                    idx=-1
                    redo_travel,idx,new_format_dict_array=ru1.apply(spline_dict, idx)
                    ru1 = None

                    if redo_travel:
                        if new_format_dict_array != None:
                            if len(new_format_dict_array) > 0:
                                new_key_index = len(stroke_dict)+1
                                stroke_dict[new_key_index]={}
                                stroke_dict[new_key_index]['dots']=new_format_dict_array
                        redo_split = True
                        break

            stroke_dict[key] = spline_dict

        #print("after split count:", len(stroke_dict))

        return redo_split

    def preprocess(self, stroke_dict, unicode_int):
        is_modified = False

        MAX_SPLIT_CONNT = 100

        idx=-1
        redo_split=False   # Disable
        #PS: must detect inside/outsdie stroke, before enable this filter!
        #redo_split=True    # Enable
        while redo_split:
            idx+=1
            redo_split=self.split_spline(stroke_dict, unicode_int)
            if redo_split:
                is_modified = True
            if idx >= MAX_SPLIT_CONNT:
                redo_split = False

        return is_modified


    def normalize(self, stroke_dict, key, unicode_int, bmp_image, y_offset):
        is_modified = False

        from . import Rule2_Clean_Noice
        ru2=Rule2_Clean_Noice.Rule()
        ru2.assign_config(self.config)
        ru2.assign_unicode(unicode_int)
        
        from . import Rule3_Merge_Line
        ru3=Rule3_Merge_Line.Rule()
        ru3.assign_config(self.config)
        ru3.assign_unicode(unicode_int)

        from . import Rule4_Almost_Line_Curve
        ru4=Rule4_Almost_Line_Curve.Rule()
        ru4.assign_config(self.config)
        ru4.assign_unicode(unicode_int)

        spline_dict = stroke_dict[key]

        # ==================================================
        # format code block
        # ==================================================

        # format code.
        # start to travel nodes for [RULE #4]
        # format curve coner as l conver
        #print("start Rule # 4...")
        idx=-1
        redo_travel=False   # Disable
        # PS: too many issue...
        #redo_travel=True    # Enable
        while redo_travel:
            redo_travel,idx=ru4.apply(spline_dict, idx)
        ru4 = None


        # start to travel nodes for [RULE #2]
        # noice
        #print("start Rule # 2...")
        idx=-1
        redo_travel=False   # Disable
        redo_travel=True    # Enable
        while redo_travel:
            redo_travel,idx=ru2.apply(spline_dict, idx)
        ru2 = None

        # start to travel nodes for [RULE #3]
        # 有 first point 的關係，有時會有一小段的直線。
        #print("start Rule # 3...")
        idx=-1
        redo_travel=False   # Disable
        redo_travel=True    # Enable
        while redo_travel:
            redo_travel,idx=ru3.apply(spline_dict, idx)
        ru3 = None

        return is_modified

    # run both in clockwise and counter clockwise.
    def trace_common(self, stroke_dict, key, unicode_int, bmp_image, y_offset, inside_stroke_dict, skip_coordinate):
        is_modified = False

        DEBUG_CRASH_RULE = False
        #DEBUG_CRASH_RULE = True

        DISABLE_ALL_RULE = False    # online
        #DISABLE_ALL_RULE = True    # debug specific rule.

        from . import Rule101_Row
        ru101=Rule101_Row.Rule()
        ru101.assign_config(self.config)
        ru101.assign_unicode(unicode_int)

        from . import Rule102_Col
        ru102=Rule102_Col.Rule()
        ru102.assign_config(self.config)
        ru102.assign_unicode(unicode_int)

        from . import Rule103_People
        ru103=Rule103_People.Rule()
        ru103.assign_config(self.config)
        ru103.assign_unicode(unicode_int)

        from . import Rule104_People_Tail
        ru104=Rule104_People_Tail.Rule()
        ru104.assign_config(self.config)
        ru104.assign_unicode(unicode_int)

        from . import Rule105_Left_Top
        ru105=Rule105_Left_Top.Rule()
        ru105.assign_config(self.config)
        ru105.assign_unicode(unicode_int)

        from . import Rule106_Little_Mountain
        ru106=Rule106_Little_Mountain.Rule()
        ru106.assign_config(self.config)
        ru106.assign_unicode(unicode_int)

        from . import Rule107_Eight
        ru107=Rule107_Eight.Rule()
        ru107.assign_config(self.config)
        ru107.assign_unicode(unicode_int)

        # start process here.
        spline_dict = stroke_dict[key]


        # start to travel nodes for [RULE #101]
        # 橫線右邊三角形轉長方形
        if DEBUG_CRASH_RULE:
            print("start Rule # 101...")
        idx=-1
        redo_travel=False   # Disable
        redo_travel=True    # Enable
        if DISABLE_ALL_RULE:
            redo_travel=False
            pass

        skip_coordinate_rule = []
        redo_count=0
        while redo_travel:
            redo_count+=1
            if redo_count==100:
                print("occure bug at rule#101!")
            redo_travel,idx, inside_stroke_dict,skip_coordinate,skip_coordinate_rule=ru101.apply(spline_dict, idx, inside_stroke_dict,skip_coordinate,skip_coordinate_rule)
            if redo_travel:
                is_modified = True
        # redo again after all.
        #ru101 = None

        # start to travel nodes for [RULE #102]
        # 直線開頭三角形轉長方形
        if DEBUG_CRASH_RULE:
            print("start Rule # 102...")
        idx=-1
        redo_travel=False   # Disable
        redo_travel=True    # Enable
        if DISABLE_ALL_RULE:
            redo_travel=False
            pass
            
        skip_coordinate_rule = []
        redo_count=0
        while redo_travel:
            redo_count+=1
            if redo_count==100:
                print("occure bug at rule#102!")
            redo_travel,idx, inside_stroke_dict,skip_coordinate,skip_coordinate_rule=ru102.apply(spline_dict, idx, inside_stroke_dict,skip_coordinate,skip_coordinate_rule)
            if redo_travel:
                is_modified = True
        ru102 = None

        # start to travel nodes for [RULE #103]
        # 「亻」部三角形
        if DEBUG_CRASH_RULE:
            print("start Rule # 103...")
        idx=-1
        redo_travel=False   # Disable
        redo_travel=True    # Enable
        if DISABLE_ALL_RULE:
            redo_travel=False
            pass
        skip_coordinate_rule = []
        redo_count=0
        while redo_travel:
            redo_count+=1
            if redo_count==100:
                print("occure bug at rule#103!")
            redo_travel,idx, inside_stroke_dict,skip_coordinate,skip_coordinate_rule=ru103.apply(spline_dict, idx, inside_stroke_dict,skip_coordinate,skip_coordinate_rule)
            if redo_travel:
                is_modified = True
        ru103 = None


        # start to travel nodes for [RULE #104]
        # 「亻」部三角形
        if DEBUG_CRASH_RULE:
            print("start Rule # 104...")
        idx=-1
        redo_travel=False   # Disable
        redo_travel=True    # Enable
        if DISABLE_ALL_RULE:
            redo_travel=False
            pass
        skip_coordinate_rule = []
        redo_count=0
        while redo_travel:
            redo_count+=1
            if redo_count==100:
                print("occure bug at rule#104!")
            redo_travel,idx, inside_stroke_dict,skip_coordinate,skip_coordinate_rule=ru104.apply(spline_dict, idx, inside_stroke_dict,skip_coordinate,skip_coordinate_rule)
            if redo_travel:
                is_modified = True
        ru104 = None

        # start to travel nodes for [RULE #105]
        # 直線左上角的三角形轉長方形
        if DEBUG_CRASH_RULE:
            print("start Rule # 105...")
        idx=-1
        redo_travel=False   # Disable
        redo_travel=True    # Enable
        if DISABLE_ALL_RULE:
            redo_travel=False
            pass
        skip_coordinate_rule = []
        redo_count=0
        while redo_travel:
            redo_count+=1
            if redo_count==100:
                print("occure bug at rule#105!")
            redo_travel,idx, inside_stroke_dict,skip_coordinate,skip_coordinate_rule=ru105.apply(spline_dict, idx, inside_stroke_dict,skip_coordinate,skip_coordinate_rule)
            if redo_travel:
                is_modified = True
        ru105 = None

        # start to travel nodes for [RULE #106]
        # 二個筆畫，產生出來在直線的三角形
        if DEBUG_CRASH_RULE:
            print("start Rule # 106...")
        idx=-1
        redo_travel=False   # Disable
        redo_travel=True    # Enable
        if DISABLE_ALL_RULE:
            redo_travel=False
            pass
        skip_coordinate_rule = []
        redo_count=0
        while redo_travel:
            redo_count+=1
            if redo_count==100:
                print("occure bug at rule#106!")
            redo_travel,idx, inside_stroke_dict,skip_coordinate,skip_coordinate_rule=ru106.apply(spline_dict, idx, inside_stroke_dict,skip_coordinate,skip_coordinate_rule)
            if redo_travel:
                is_modified = True
        ru106 = None

        # start to travel nodes for [RULE #107]
        # 二個筆畫，產生出來在直線的三角形
        if DEBUG_CRASH_RULE:
            print("start Rule # 107...")
        idx=-1
        redo_travel=False   # Disable
        redo_travel=True    # Enable
        if DISABLE_ALL_RULE:
            redo_travel=False
            pass
        skip_coordinate_rule = []
        redo_count=0
        while redo_travel:
            redo_count+=1
            if redo_count==100:
                print("occure bug at rule#107!")
            redo_travel,idx, inside_stroke_dict,skip_coordinate,skip_coordinate_rule=ru107.apply(spline_dict, idx, inside_stroke_dict,skip_coordinate,skip_coordinate_rule)
            if redo_travel:
                is_modified = True
        ru107 = None

        # start to travel nodes for [RULE #101]
        # PS: 105+106, 改變外形後，會讓 101 重新 match.
        if is_modified:
            if DEBUG_CRASH_RULE:
                print("start Rule # 101...")
            idx=-1
            redo_travel=False   # Disable
            redo_travel=True    # Enable
            if DISABLE_ALL_RULE:
                redo_travel=False
                pass

            skip_coordinate_rule = []
            redo_count=0
            while redo_travel:
                redo_count+=1
                if redo_count==100:
                    print("occure bug at rule#101!")
                redo_travel,idx, inside_stroke_dict,skip_coordinate,skip_coordinate_rule=ru101.apply(spline_dict, idx, inside_stroke_dict,skip_coordinate,skip_coordinate_rule)
                if redo_travel:
                    is_modified = True
            ru101 = None

        return is_modified, inside_stroke_dict, skip_coordinate


    def trace_white_block(self, stroke_dict, key, unicode_int, bmp_image, y_offset):
        is_modified = False

        spline_dict = stroke_dict[key]

        # cache bmp status
        inside_stroke_dict={}

        # cache skip coordinate, same transformed position should not do twice.
        skip_coordinate = []

        # ==================================================
        # transform code block
        # ==================================================
        is_modified, inside_stroke_dict, skip_coordinate = self.trace_common(stroke_dict, key, unicode_int, bmp_image, y_offset, inside_stroke_dict, skip_coordinate)

        return is_modified

    def trace_black_block(self, stroke_dict, key, unicode_int, bmp_image, y_offset):
        is_modified = False

        DEBUG_CRASH_RULE = False
        #DEBUG_CRASH_RULE = True

        DISABLE_ALL_RULE = False    # online
        #DISABLE_ALL_RULE = True    # debug specific rule.

        spline_dict = stroke_dict[key]

        # cache bmp status
        inside_stroke_dict={}

        # cache skip coordinate, same transformed position should not do twice.
        skip_coordinate = []

        # for debug.
        #print("□"*60)
        #print("key:", key, 'code:', spline_dict['dots'][0])
        #if not key == 1:
            #return spline_dict

        # ==================================================
        # transform code block
        # ==================================================
        is_modified, inside_stroke_dict, skip_coordinate = self.trace_common(stroke_dict, key, unicode_int, bmp_image, y_offset, inside_stroke_dict, skip_coordinate)

        return is_modified
