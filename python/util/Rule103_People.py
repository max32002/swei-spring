#!/usr/bin/env python3
#encoding=utf-8

from . import spline_util
from . import Rule

# RULE # 103
# 「亻」部三角形
# PS: 因為 array size change, so need redo.
class Rule(Rule.Rule):
    def __init__(self):
        pass

    def apply(self, spline_dict, resume_idx, inside_stroke_dict,skip_coordinate,skip_coordinate_rule):
        redo_travel=False
        check_first_point = False

        # default: 1.20, for case:.10075 例, reqular:1.433
        # for case:uni905C 遜, 0.925 / 0.72 / 1.785
        # for case:uni6B8D 殍, 0.64 / 0.725 / 1.775
        # for uni9BCA,鯊的魚. 0.465 / 0.535 / 1.98
        SLIDE_3_PERCENT_MIN = 0.41
        SLIDE_3_PERCENT_MAX = 1.60

        # default: 0.8 to 0.53
        SLIDE_4_PERCENT_MIN = 0.43
        SLIDE_4_PERCENT_MAX = 0.99

        # default: 1.7
        SLIDE_5_PERCENT_MIN = 1.55
        SLIDE_5_PERCENT_MAX = 1.89

        # for uni947F,鑿的羊. 0.175 / 0.715 / 1.985
        SLIDE_13_PERCENT_MIN = 0.01
        SLIDE_13_PERCENT_MAX = 0.60

        # clone
        format_dict_array=[]
        format_dict_array = spline_dict['dots'][1:]
        format_dict_array = self.caculate_distance(format_dict_array)

        nodes_length = len(format_dict_array)
        #print("orig nodes_length:", len(spline_dict['dots']))
        #print("format nodes_length:", nodes_length)
        #print("resume_idx:", resume_idx)

        rule_need_lines = 5
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
                    #print(idx, "#103, match:", format_dict_array[idx]['x'],format_dict_array[idx]['y'])
                    debug_coordinate_list = [[854,640]]
                    if not([format_dict_array[idx]['x'],format_dict_array[idx]['y']] in debug_coordinate_list):
                        continue

                    print("="*30)
                    print("index:", idx)
                    for debug_idx in range(9):
                        print(debug_idx-2,": values for rule101:",format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['code'],'-(',format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['distance'],')')

                # begin travel.
                is_match_pattern = True

                # match ??lc?
                if is_match_pattern:
                    fail_code = 100
                    is_match_pattern = False
                    if True:
                    #if format_dict_array[(idx+2)%nodes_length]['t'] == 'l':
                        # for case:.18791 應，+3=l
                        #if format_dict_array[(idx+3)%nodes_length]['t'] == 'c':
                        if format_dict_array[(idx+4)%nodes_length]['t'] == 'l':
                            # +5下巴，不限定為曲線，可處理直線下巴。

                            # for uni9BCA,鯊的魚.
                            #if format_dict_array[(idx+6)%nodes_length]['t'] == 'l':
                            if True:
                                is_match_pattern = True

                if is_match_pattern:
                    fail_code = 200
                    is_match_pattern = False

                    if format_dict_array[(idx+3)%nodes_length]['distance'] >= self.config.COL_TRIANGLE_CHIN_MIN:
                        fail_code = 230
                        if format_dict_array[(idx+3)%nodes_length]['distance'] <= self.config.STROKE_WIDTH_MAX:
                            fail_code = 240
                            if format_dict_array[(idx+4)%nodes_length]['distance'] >= self.config.COL_TRIANGLE_CHIN_MIN:
                                fail_code = 250
                                if format_dict_array[(idx+4)%nodes_length]['distance'] <= self.config.STROKE_WIDTH_MAX:
                                    fail_code = 260
                                    # usually, +5 should be a little long.
                                    if format_dict_array[(idx+5)%nodes_length]['distance'] >= self.config.COL_TRIANGLE_CHIN_MIN:
                                        is_match_pattern = True

                if is_match_pattern:
                    fail_code = 300
                    is_match_pattern = False

                    # 「/」
                    if format_dict_array[(idx+2)%nodes_length]['x_direction'] < 0:
                        fail_code = 310
                        if format_dict_array[(idx+3)%nodes_length]['x_direction'] > 0:
                            fail_code = 311
                            if format_dict_array[(idx+4)%nodes_length]['x_direction'] < 0:
                                fail_code = 312
                                # for normal case.
                                if format_dict_array[(idx+5)%nodes_length]['x_equal_fuzzy']:
                                    is_match_pattern = True
                                
                                # for uni9BCA,鯊的魚.
                                if format_dict_array[(idx+5)%nodes_length]['x_direction'] < 0:
                                    is_match_pattern = True

                if is_match_pattern:
                    fail_code = 400
                    is_match_pattern = False

                    if format_dict_array[(idx+3)%nodes_length]['y1'] <= format_dict_array[(idx+2)%nodes_length]['y']:
                        if format_dict_array[(idx+3)%nodes_length]['y_direction'] < 0:
                            if format_dict_array[(idx+4)%nodes_length]['y_direction'] <= 0:
                                if format_dict_array[(idx+5)%nodes_length]['y_direction'] <= 0:
                                    is_match_pattern = True

                # for 「立」模式.
                is_standup_mode = False

                # skip small angle
                if is_match_pattern:
                    fail_code = 500
                    is_match_pattern = False

                    #slide_percent_2 = spline_util.slide_percent(format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'],format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'])
                    slide_percent_3 = spline_util.slide_percent(format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'],format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'],format_dict_array[(idx+4)%nodes_length]['x'],format_dict_array[(idx+4)%nodes_length]['y'])
                    slide_percent_4 = spline_util.slide_percent(format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'],format_dict_array[(idx+4)%nodes_length]['x'],format_dict_array[(idx+4)%nodes_length]['y'],format_dict_array[(idx+5)%nodes_length]['x'],format_dict_array[(idx+5)%nodes_length]['y'])
                    slide_percent_5 = spline_util.slide_percent(format_dict_array[(idx+4)%nodes_length]['x'],format_dict_array[(idx+4)%nodes_length]['y'],format_dict_array[(idx+5)%nodes_length]['x'],format_dict_array[(idx+5)%nodes_length]['y'],format_dict_array[(idx+6)%nodes_length]['x'],format_dict_array[(idx+6)%nodes_length]['y'])

                    #if True:
                    #if False:
                    if is_debug_mode:
                        #print("slide_percent 2:", slide_percent_2)
                        #print("data:",format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'],format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'])
                        print("slide_percent 3:", slide_percent_3)
                        #print("data:",format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'],format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'],format_dict_array[(idx+4)%nodes_length]['x'],format_dict_array[(idx+4)%nodes_length]['y'])
                        print("slide_percent 4:", slide_percent_4)
                        print("slide_percent 5:", slide_percent_5)

                    # if will fail, try virtual line.
                    if slide_percent_5 > SLIDE_5_PERCENT_MAX:
                        x2 = format_dict_array[(idx+5)%nodes_length]['x']
                        y2 = format_dict_array[(idx+5)%nodes_length]['y']
                        if format_dict_array[(idx+5)%nodes_length]['t']=='c':
                            x2 = format_dict_array[(idx+5)%nodes_length]['x2']
                            y2 = format_dict_array[(idx+5)%nodes_length]['y2']
                        slide_percent_5 = spline_util.slide_percent(x2,y2,format_dict_array[(idx+5)%nodes_length]['x'],format_dict_array[(idx+5)%nodes_length]['y'],format_dict_array[(idx+6)%nodes_length]['x'],format_dict_array[(idx+6)%nodes_length]['y'])
                        if is_debug_mode:
                            print("slide_percent 5 virtual:", slide_percent_5)

                    is_pass_dot_3_check = False
                    if slide_percent_3 >= SLIDE_3_PERCENT_MIN and slide_percent_3 <= SLIDE_3_PERCENT_MAX:
                        fail_code = 510
                        is_pass_dot_3_check = True

                    if not is_pass_dot_3_check:
                        fail_code = 511
                        if format_dict_array[(idx+2)%nodes_length]['y_equal_fuzzy']:
                            fail_code = 511
                            if slide_percent_3 >= SLIDE_13_PERCENT_MIN and slide_percent_3 <= SLIDE_13_PERCENT_MAX:
                                is_pass_dot_3_check = True
                                is_standup_mode = True

                    if is_pass_dot_3_check:
                        if slide_percent_4 >= SLIDE_4_PERCENT_MIN and slide_percent_4 <= SLIDE_4_PERCENT_MAX:
                            fail_code = 520
                            
                            if slide_percent_5 >= SLIDE_5_PERCENT_MIN and slide_percent_5 <= SLIDE_5_PERCENT_MAX:
                                is_match_pattern = True

                if is_debug_mode:
                    if not is_match_pattern:
                        print("#", idx,": debug fail_code#103:", fail_code)
                        pass
                    else:
                        print("match rule #103")
                        print(idx,"debug rule103:",format_dict_array[idx]['code'])
                        pass

                if is_match_pattern:

                    # for 「立」模式.
                    if not is_standup_mode:
                        # normal case.

                        # update 1
                        # no matter +5 dot is c or l, force convert to l.
                        new_code = " %d %d l 1\n" % (format_dict_array[(idx+5)%nodes_length]['x'],format_dict_array[(idx+5)%nodes_length]['y'])
                        format_dict_array[(idx+5)%nodes_length]['t']="l"
                        format_dict_array[(idx+5)%nodes_length]['code']=new_code
                        #print("old_code:", old_code)
                        #print("new_code:", new_code)

                        # update 2
                        # make the line straight.
                        old_code = format_dict_array[(idx+3)%nodes_length]['code']
                        old_code_array = old_code.split(' ')
                        if format_dict_array[(idx+3)%nodes_length]['t']=="l":
                            old_code_array[1]=str(format_dict_array[(idx+5)%nodes_length]['x'])
                        else:
                            old_code_array[5]=str(format_dict_array[(idx+5)%nodes_length]['x'])
                        new_code = ' '.join(old_code_array)
                        format_dict_array[(idx+3)%nodes_length]['code']=new_code

                        #print("del code:", format_dict_array[(idx+3)%nodes_length]['code'])
                        del format_dict_array[(idx+4)%nodes_length]

                        # we generated nodes
                        #skip_coordinate.append([center_x,center_y])
                    else:
                        # 「立」模式.
                        # PS: 考慮只有spring mode 才把半圓換成直線。
                        #if self.config.PROCESS_MODE == "SPRING":
                        new_code = " %d %d l 1\n" % (format_dict_array[(idx+5)%nodes_length]['x'],format_dict_array[(idx+5)%nodes_length]['y'])
                        format_dict_array[(idx+5)%nodes_length]['t']="l"
                        format_dict_array[(idx+5)%nodes_length]['code']=new_code

                        # TODO:
                        # resize +4 length.



                    redo_travel=True
                    check_first_point = True
                    resume_idx = -1
                    break

        if redo_travel:
            nodes_length = len(format_dict_array)
            code_added = format_dict_array[(idx+0)%nodes_length]['code']
            #print("code_added:", code_added)
            skip_coordinate_rule.append(code_added)

        if check_first_point:
            # check close path.
            self.reset_first_point(format_dict_array, spline_dict)

        return redo_travel, resume_idx, inside_stroke_dict,skip_coordinate,skip_coordinate_rule
