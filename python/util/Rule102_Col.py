#!/usr/bin/env python3
#encoding=utf-8

from . import spline_util
from . import Rule

# RULE # 102
# 直線開頭三角形轉長方形
# PS: 因為 array size change, so need redo.
class Rule(Rule.Rule):
    def __init__(self):
        pass

    def apply(self, spline_dict, resume_idx, inside_stroke_dict,skip_coordinate, skip_coordinate_rule):
        redo_travel=False
        check_first_point = False

        # default（normal): 1.3 to 1.43, (橫線) 1.733, (for case:.26335 狀) 1.233
        SLIDE_1_PERCENT_MIN = 1.11
        SLIDE_1_PERCENT_MAX = 1.83

        # default: 0.7 to 0.53, 
        SLIDE_2_PERCENT_MIN = 0.43
        SLIDE_2_PERCENT_MAX = 0.8

        # default: 1.76 to 1.9, (橫線) 1.9-1.96, (for case:.26335 狀) 1.633
        # for case uni6507 攇, 1.99
        SLIDE_3_PERCENT_MIN = 1.52
        SLIDE_3_PERCENT_MAX = 1.99

        # for uni83A3 莣, 1.25/0.81/1.79
        SLIDE_11_PERCENT_MIN = 1.05
        SLIDE_11_PERCENT_MAX = 1.45
        SLIDE_12_PERCENT_MIN = 0.50
        SLIDE_12_PERCENT_MAX = 1.01
        SLIDE_13_PERCENT_MIN = 1.59
        SLIDE_13_PERCENT_MAX = 1.99

        # for case: uni8F9C 辜的辛的立的右上角。 0.325/0.725/1.98
        # for case: uni9059 遙的缶。0.865 / 0.6 / 1.95
        # PS: 這裡的判斷 和 rule103 是重覆判斷。
        SLIDE_21_PERCENT_MIN = 0.01
        SLIDE_21_PERCENT_MAX = 1.45

        # clone
        format_dict_array=[]
        format_dict_array = spline_dict['dots'][1:]
        format_dict_array = self.caculate_distance(format_dict_array)

        nodes_length = len(format_dict_array)
        #print("orig nodes_length:", len(spline_dict['dots']))
        #print("format nodes_length:", nodes_length)
        #print("resume_idx:", resume_idx)

        rule_need_lines = 4
        fail_code = -1
        if nodes_length >= rule_need_lines:
            for idx in range(nodes_length):
                if idx <= resume_idx:
                    # skip traveled nodes.
                    continue

                is_debug_mode = False
                #is_debug_mode = True

                # 要轉換的角，不能就是我們產生出來的點。
                if [format_dict_array[idx]['x'],format_dict_array[idx]['y']] in skip_coordinate:
                    if is_debug_mode:
                        print("match skip dot +0:",[format_dict_array[(idx+0)%nodes_length]['x'],format_dict_array[(idx+0)%nodes_length]['y']])
                        pass
                    continue

                if format_dict_array[idx]['code'] in skip_coordinate_rule:
                    if is_debug_mode:
                        print("match skip skip_coordinate_rule +0:",[format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y']])
                        pass
                    continue

                is_debug_mode = False
                #is_debug_mode = True

                if is_debug_mode:
                    debug_coordinate_list = [[558,696]]
                    if not([format_dict_array[idx]['x'],format_dict_array[idx]['y']] in debug_coordinate_list):
                        continue

                    print("="*30)
                    print("index:", idx)
                    for debug_idx in range(8):
                        print(debug_idx-2,": val#102:",format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['code'],'-(',format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['distance'],')')

                # begin travel.
                is_match_pattern = True

                # match ??lc?
                if is_match_pattern:
                    fail_code = 100
                    is_match_pattern = False
                    if format_dict_array[(idx+2)%nodes_length]['t'] == 'l':
                        if format_dict_array[(idx+3)%nodes_length]['t'] == 'c':
                            is_match_pattern = True

                is_more_one_dot = False

                if is_match_pattern:
                    fail_code = 200
                    is_match_pattern = False
                    if format_dict_array[(idx+1)%nodes_length]['distance'] >= self.config.STROKE_WIDTH_MIN:
                        fail_code = 210
                        if format_dict_array[(idx+1)%nodes_length]['distance'] <= self.config.STROKE_WIDTH_MAX:
                            fail_code = 220
                            
                            if format_dict_array[(idx+2)%nodes_length]['distance'] >= self.config.COL_TRIANGLE_CHIN_MIN:
                                fail_code = 230
                                if format_dict_array[(idx+2)%nodes_length]['distance'] <= self.config.COL_TRIANGLE_CHIN_MAX:
                                    is_match_pattern = True

                            # +2 & +3 are small edge.
                            # for case: uni6AB9 檹
                            # ps: 可能同時 is_match_pattern = True 在 fail_code 230 還有下面的 fail_code 240
                            small_edge_sum = format_dict_array[(idx+2)%nodes_length]['distance']+format_dict_array[(idx+3)%nodes_length]['distance']
                            #print("small_edge_sum:",small_edge_sum)
                            if format_dict_array[(idx+2)%nodes_length]['distance'] < 45:
                                if format_dict_array[(idx+3)%nodes_length]['distance'] < 45:
                                    fail_code = 240
                                    if small_edge_sum >= self.config.COL_TRIANGLE_CHIN_MIN:
                                        if small_edge_sum <= self.config.COL_TRIANGLE_CHIN_MAX:
                                            if format_dict_array[(idx+2)%nodes_length]['x_direction'] == format_dict_array[(idx+3)%nodes_length]['x_direction']:
                                                if format_dict_array[(idx+2)%nodes_length]['y_direction'] == format_dict_array[(idx+3)%nodes_length]['y_direction']:
                                                    is_more_one_dot = True
                                                    is_match_pattern = True

                # for case: uni8F9C 辜的辛的立的右上角。
                # 是否第一個邊，與其他筆畫合併。
                is_first_edge_merged = False

                if is_match_pattern:
                    fail_code = 300
                    is_match_pattern = False
                    # 「/」頭在上。
                    if format_dict_array[(idx+0)%nodes_length]['x_direction'] >= 0:
                        fail_code = 310
                        if format_dict_array[(idx+1)%nodes_length]['x_direction'] > 0:
                            fail_code = 311
                            if format_dict_array[(idx+2)%nodes_length]['x_direction'] < 0:
                                fail_code = 312
                                if format_dict_array[(idx+3)%nodes_length]['x_direction'] <= 0:
                                    is_match_pattern = True

                    # for case: uni9059 遙的辶的最左下角。
                    # 「/」頭在下。
                    # PS: 目前未拔除。
                    if format_dict_array[(idx+0)%nodes_length]['x_direction'] <= 0:
                        fail_code = 315
                        if format_dict_array[(idx+1)%nodes_length]['x_direction'] > 0:
                            fail_code = 316
                            if format_dict_array[(idx+2)%nodes_length]['x_direction'] < 0:
                                fail_code = 317
                                if format_dict_array[(idx+3)%nodes_length]['x_direction'] >= 0:
                                    is_match_pattern = True

                    # 「＼」
                    if not is_match_pattern:
                        if format_dict_array[(idx+0)%nodes_length]['x_direction'] <= 0:
                            fail_code = 320
                            if format_dict_array[(idx+1)%nodes_length]['x_direction'] > 0:
                                fail_code = 321
                                if format_dict_array[(idx+2)%nodes_length]['x_direction'] < 0:
                                    fail_code = 322
                                    if format_dict_array[(idx+3)%nodes_length]['x_direction'] >= 0:
                                        is_match_pattern = True

                    # 「|」common case 頭在上。
                    if not is_match_pattern:
                        if format_dict_array[(idx+0)%nodes_length]['x_equal_fuzzy']:
                            fail_code = 330
                            if format_dict_array[(idx+1)%nodes_length]['x_direction'] > 0:
                                fail_code = 331
                                if format_dict_array[(idx+2)%nodes_length]['x_direction'] < 0:
                                    fail_code = 332
                                    if format_dict_array[(idx+3)%nodes_length]['x_equal_fuzzy']:
                                        is_match_pattern = True

                    # 「一」接近橫線的版本。
                    if not is_match_pattern:
                        if format_dict_array[(idx+0)%nodes_length]['y_equal_fuzzy']:
                            fail_code = 335
                            if format_dict_array[(idx+1)%nodes_length]['x_direction'] > 0:
                                fail_code = 336
                                if format_dict_array[(idx+2)%nodes_length]['x_direction'] < 0:
                                    fail_code = 337
                                    if format_dict_array[(idx+3)%nodes_length]['y_equal_fuzzy']:
                                        is_match_pattern = True

                    # for case: uni8F9C 辜的辛的立的右上角。
                    # for case: uni9059 遙的缶。
                    # 「/」
                    if not is_match_pattern:
                        if format_dict_array[(idx+0)%nodes_length]['x_direction'] <= 0:
                            fail_code = 340
                            if format_dict_array[(idx+1)%nodes_length]['x_direction'] > 0:
                                fail_code = 341
                                if format_dict_array[(idx+2)%nodes_length]['x_direction'] < 0:
                                    fail_code = 342
                                    if format_dict_array[(idx+3)%nodes_length]['x_direction'] <= 0:
                                        is_match_pattern = True
                                        is_first_edge_merged = True

                if is_debug_mode:
                    print("is_first_edge_merged:", is_first_edge_merged)
                    #print("fail_code:",fail_code)

                if is_match_pattern:
                    fail_code = 400
                    is_match_pattern = False

                    is_pass_dot0_check = False
                    if format_dict_array[(idx+0)%nodes_length]['y_direction'] > 0:
                        fail_code = 410
                        is_pass_dot0_check = True

                    # for case: uni8F9C 辜的辛的立的右上角。
                    if is_first_edge_merged:
                        if format_dict_array[(idx+0)%nodes_length]['y_direction'] <= 0 or format_dict_array[(idx+0)%nodes_length]['y_equal_fuzzy']:
                            fail_code = 411
                            is_pass_dot0_check = True

                    if is_pass_dot0_check:
                        if format_dict_array[(idx+1)%nodes_length]['y_direction'] <= 0:
                            #print(format_dict_array[(idx+2)%nodes_length]['y_direction'])
                            if format_dict_array[(idx+3)%nodes_length]['y1'] <= format_dict_array[(idx+2)%nodes_length]['y']:
                                if format_dict_array[(idx+3)%nodes_length]['y_direction'] < 0:
                                    is_match_pattern = True

                # skip small angle
                if is_match_pattern:
                    fail_code = 500
                    is_match_pattern = False

                    slide_percent_1 = spline_util.slide_percent(format_dict_array[(idx+0)%nodes_length]['x'],format_dict_array[(idx+0)%nodes_length]['y'],format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'])
                    slide_percent_2 = spline_util.slide_percent(format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'],format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'])
                    slide_percent_3 = spline_util.slide_percent(format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'],format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'],format_dict_array[(idx+4)%nodes_length]['x'],format_dict_array[(idx+4)%nodes_length]['y'])

                    #if True:
                    #if False:
                    if is_debug_mode:
                        print("slide_percent 1:", slide_percent_1)
                        print("data:",format_dict_array[(idx+0)%nodes_length]['x'],format_dict_array[(idx+0)%nodes_length]['y'],format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'])
                        print("slide_percent 2:", slide_percent_2)
                        print("data:",format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'],format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'])
                        print("slide_percent 3:", slide_percent_3)
                        print("data:",format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'],format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'],format_dict_array[(idx+4)%nodes_length]['x'],format_dict_array[(idx+4)%nodes_length]['y'])

                    # if real line is almost straight, try virtual line.
                    if slide_percent_3 >= 2.0:
                        if format_dict_array[(idx+3)%nodes_length]['t']=='c':
                            x2 = format_dict_array[(idx+3)%nodes_length]['x2']
                            y2 = format_dict_array[(idx+3)%nodes_length]['y2']
                            slide_percent_3 = spline_util.slide_percent(x2,y2,format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'],format_dict_array[(idx+4)%nodes_length]['x'],format_dict_array[(idx+4)%nodes_length]['y'])
                            if is_debug_mode:
                                print("slide_percent 3 (x2,y2):", slide_percent_3)
                                print("data:",x2,y2,format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'],format_dict_array[(idx+4)%nodes_length]['x'],format_dict_array[(idx+4)%nodes_length]['y'])

                    if slide_percent_1 >= SLIDE_1_PERCENT_MIN and slide_percent_1 <= SLIDE_1_PERCENT_MAX:
                        fail_code = 510
                        if slide_percent_2 >= SLIDE_2_PERCENT_MIN and slide_percent_2 <= SLIDE_2_PERCENT_MAX:
                            fail_code = 520
                            if slide_percent_3 >= SLIDE_3_PERCENT_MIN and slide_percent_3 <= SLIDE_3_PERCENT_MAX:
                                is_match_pattern = True

                    # for uni83A3 莣, 1.25/0.81/1.79
                    if not is_match_pattern:
                        if slide_percent_1 >= SLIDE_11_PERCENT_MIN and slide_percent_1 <= SLIDE_11_PERCENT_MAX:
                            fail_code = 530
                            if slide_percent_2 >= SLIDE_12_PERCENT_MIN and slide_percent_2 <= SLIDE_12_PERCENT_MAX:
                                fail_code = 540
                                if slide_percent_3 >= SLIDE_13_PERCENT_MIN and slide_percent_3 <= SLIDE_13_PERCENT_MAX:
                                    is_match_pattern = True

                    if not is_match_pattern:
                        if is_more_one_dot:
                            slide_percent_2 = spline_util.slide_percent(format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'],format_dict_array[(idx+4)%nodes_length]['x'],format_dict_array[(idx+4)%nodes_length]['y'])
                            slide_percent_3 = spline_util.slide_percent(format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'],format_dict_array[(idx+4)%nodes_length]['x'],format_dict_array[(idx+4)%nodes_length]['y'],format_dict_array[(idx+5)%nodes_length]['x'],format_dict_array[(idx+5)%nodes_length]['y'])

                            if slide_percent_1 >= SLIDE_1_PERCENT_MIN and slide_percent_1 <= SLIDE_1_PERCENT_MAX:
                                fail_code = 550
                                if slide_percent_2 >= SLIDE_2_PERCENT_MIN and slide_percent_2 <= SLIDE_2_PERCENT_MAX:
                                    fail_code = 551
                                    if slide_percent_3 >= SLIDE_3_PERCENT_MIN and slide_percent_3 <= SLIDE_3_PERCENT_MAX:
                                        is_match_pattern = True

                    # for case: uni8F9C 辜的辛的立的右上角。
                    if not is_match_pattern:
                        if slide_percent_1 >= SLIDE_21_PERCENT_MIN and slide_percent_1 <= SLIDE_21_PERCENT_MAX:
                            fail_code = 560
                            if slide_percent_2 >= SLIDE_12_PERCENT_MIN and slide_percent_2 <= SLIDE_12_PERCENT_MAX:
                                fail_code = 561
                                if slide_percent_3 >= SLIDE_13_PERCENT_MIN and slide_percent_3 <= SLIDE_13_PERCENT_MAX:
                                    is_match_pattern = True

                if is_debug_mode:
                    if not is_match_pattern:
                        print("#", idx,": debug fail_code#101:", fail_code)
                        pass
                    else:
                        print("match rule #102")
                        print(idx,"debug rule102:",format_dict_array[idx]['code'])
                        pass

                if is_match_pattern:
                    if False:
                    #if True:
                        print("#"*40)
                        for debug_idx in range(7):
                            print(debug_idx-2,": values for rule102:",format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['code'],'-(',format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['distance'],')')

                    ending_x = format_dict_array[(idx+3)%nodes_length]['x']
                    #ending_y = format_dict_array[(idx+2)%nodes_length]['y']

                    # update 1
                    old_code = format_dict_array[(idx+2)%nodes_length]['code']
                    old_code_array = old_code.split(' ')
                    #x = int(float(old_code_array[1]))
                    #y = int(float(old_code_array[2]))
                    old_code_array[1]=str(ending_x)
                    new_code = ' '.join(old_code_array)
                    format_dict_array[(idx+2)%nodes_length]['code']=new_code
                    #print("old_code:", old_code)
                    #print("new_code:", new_code)

                    #print("del code:", format_dict_array[(idx+3)%nodes_length]['code'])
                    del format_dict_array[(idx+3)%nodes_length]

                    # we generated nodes
                    #skip_coordinate.append([center_x,center_y])

                    redo_travel=True
                    check_first_point = True
                    resume_idx = -1
                    break

        if check_first_point:
            # check close path.
            self.reset_first_point(format_dict_array, spline_dict)

        return redo_travel, resume_idx, inside_stroke_dict,skip_coordinate, skip_coordinate_rule
