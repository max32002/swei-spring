#!/usr/bin/env python3
#encoding=utf-8

from . import spline_util
from . import Rule

# RULE # 106
# 二個筆畫，產生出來在直線的三角形
# PS: 因為 array size change, so need redo.
class Rule(Rule.Rule):
    def __init__(self):
        pass

    def apply(self, spline_dict, resume_idx, inside_stroke_dict,skip_coordinate, skip_coordinate_rule):
        redo_travel=False
        check_first_point = False

        SLASH_LENGTH_MIN = 35
        SLASH_LENGTH_MAX = 180

        # default: 1.78 (uni68F0,棰)
        SLIDE_1_PERCENT_MIN = 1.58
        SLIDE_1_PERCENT_MAX = 1.93

        # default: 1.34 (uni68F0,棰) / 1.49 (uni8F1F,輟)
        SLIDE_2_PERCENT_MIN = 1.14
        SLIDE_2_PERCENT_MAX = 1.60

        # default: 1.86 (uni68F0,棰)
        SLIDE_3_PERCENT_MIN = 1.66
        SLIDE_3_PERCENT_MAX = 1.93

        # default: 0.79 (uni6935,椵)
        SLIDE_13_PERCENT_MIN = 0.65
        SLIDE_13_PERCENT_MAX = 0.95

        # default: 0.69 (uni695C,楜)
        SLIDE_21_PERCENT_MIN = 0.55
        SLIDE_21_PERCENT_MAX = 0.85

        # default: 1.54 (uni6691,暑) / 1.04 (uni653F,政) / 0.91 (uni6472,摲)
        SLIDE_33_PERCENT_MIN = 0.71
        SLIDE_33_PERCENT_MAX = 1.74

        # for uni8F1F「輟」 0.54
        # very short edge.
        SLIDE_43_PERCENT_MIN = 0.14
        SLIDE_43_PERCENT_MAX = 1.74

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
                    debug_coordinate_list = [[398,363]]
                    if not([format_dict_array[idx]['x'],format_dict_array[idx]['y']] in debug_coordinate_list):
                        continue

                    print("="*30)
                    print("index:", idx)
                    for debug_idx in range(8):
                        print(debug_idx-2,": val#106:",format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['code'],'-(',format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['distance'],')')

                # begin travel.
                is_match_pattern = True

                # for 「暑」
                is_end_with_slash = False

                # match ?ll?l
                if is_match_pattern:
                    fail_code = 100
                    is_match_pattern = False
                    
                    if True:
                    # for 「奿」和「妀」，+1=='c', skip check +1=='l'
                    #if format_dict_array[(idx+1)%nodes_length]['t'] == 'l':
                        if format_dict_array[(idx+2)%nodes_length]['t'] == 'l':
                            is_match_pattern = True
                            if format_dict_array[(idx+4)%nodes_length]['x'] > (format_dict_array[(idx+3)%nodes_length]['x'] + 4):
                                if format_dict_array[(idx+4)%nodes_length]['y'] > (format_dict_array[(idx+3)%nodes_length]['y'] + 4):
                                    is_end_with_slash = True

                                    # for uni56CD,"囍",居然右邊的橫線較高。
                                    if format_dict_array[(idx+3)%nodes_length]['y_equal_fuzzy']:
                                        is_end_with_slash = False


                if is_match_pattern:
                    fail_code = 200
                    is_match_pattern = False
                    if format_dict_array[(idx+1)%nodes_length]['distance'] >= self.config.ROW_TRIANGLE_HEIGHT_MIN:
                        fail_code = 201
                        if format_dict_array[(idx+1)%nodes_length]['distance'] <= self.config.ROW_TRIANGLE_HEIGHT_MAX:
                            fail_code = 202
                            if format_dict_array[(idx+2)%nodes_length]['distance'] >= self.config.ROW_TRIANGLE_SLIDE_MIN:
                                fail_code = 203
                                if format_dict_array[(idx+2)%nodes_length]['distance'] <= self.config.ROW_TRIANGLE_SLIDE_MAX:
                                    is_match_pattern = True


                # for 「椵」
                is_end_with_vertical = False
                # for 「楜」
                is_begin_with_vertical = False
                
                if is_match_pattern:
                    fail_code = 300
                    is_match_pattern = False

                    is_pass_dot_0_check = False
                    if format_dict_array[(idx+0)%nodes_length]['y_equal_fuzzy']:
                        if format_dict_array[(idx+0)%nodes_length]['x_direction'] > 0:
                            is_pass_dot_0_check = True

                    if format_dict_array[(idx+0)%nodes_length]['x_equal_fuzzy']:
                        if format_dict_array[(idx+0)%nodes_length]['y_direction'] < 0:
                            is_pass_dot_0_check = True
                            is_begin_with_vertical = True
                            
                    if is_pass_dot_0_check:
                        fail_code = 310
                        if format_dict_array[(idx+1)%nodes_length]['x_direction']>0:
                            if format_dict_array[(idx+1)%nodes_length]['y_direction']>0:
                                fail_code = 320
                                if format_dict_array[(idx+2)%nodes_length]['x_direction']>0:
                                    if format_dict_array[(idx+2)%nodes_length]['y_direction']<0:
                                        fail_code = 330

                                        # case for 「棰」
                                        if format_dict_array[(idx+3)%nodes_length]['y_equal_fuzzy']:
                                            if format_dict_array[(idx+3)%nodes_length]['x_direction'] > 0:
                                                is_match_pattern = True
                                        
                                        # case for 「椵」
                                        if format_dict_array[(idx+3)%nodes_length]['x_equal_fuzzy']:
                                            is_match_pattern = True
                                            is_end_with_vertical = True

                                        # for 「暑」
                                        if is_end_with_slash:
                                            if format_dict_array[(idx+3)%nodes_length]['x_direction'] > 0:
                                                if format_dict_array[(idx+3)%nodes_length]['y_direction'] > 0:
                                                    is_match_pattern = True

                                        # for uni8F1F「輟」
                                        # very short edge.
                                        if format_dict_array[(idx+3)%nodes_length]['distance'] <= 20:
                                            is_match_pattern = True


                    if is_debug_mode:
                        print("is_begin_with_vertical:", is_begin_with_vertical)
                        print("is_end_with_slash:", is_end_with_slash)
                        print("is_end_with_vertical:", is_end_with_vertical)

                # skip small angle
                if is_match_pattern:
                    fail_code = 400
                    is_match_pattern = False

                    slide_percent_1 = 0
                    slide_percent_2 = 0
                    slide_percent_3 = 0

                    slide_percent_1 = spline_util.slide_percent(format_dict_array[(idx+0)%nodes_length]['x'],format_dict_array[(idx+0)%nodes_length]['y'],format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'])
                    slide_percent_2 = spline_util.slide_percent(format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'],format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'])
                    slide_percent_3 = spline_util.slide_percent(format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'],format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'],format_dict_array[(idx+4)%nodes_length]['x'],format_dict_array[(idx+4)%nodes_length]['y'])

                    if is_debug_mode:
                        print("slide_percent 1:", slide_percent_1)
                        print("data:",format_dict_array[(idx+0)%nodes_length]['x'],format_dict_array[(idx+0)%nodes_length]['y'],format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'])
                        print("slide_percent 2:", slide_percent_2)
                        print("data:",format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'],format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'])
                        print("slide_percent 3:", slide_percent_3)
                        print("data:",format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'],format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'],format_dict_array[(idx+4)%nodes_length]['x'],format_dict_array[(idx+4)%nodes_length]['y'])

                    # come from horizon
                    is_pass_slide_1_check = False

                    if not is_begin_with_vertical:
                        if slide_percent_1 >= SLIDE_1_PERCENT_MIN and slide_percent_1 <= SLIDE_1_PERCENT_MAX:
                            fail_code = 410
                            is_pass_slide_1_check = True
                    else:
                        if slide_percent_1 >= SLIDE_21_PERCENT_MIN and slide_percent_1 <= SLIDE_21_PERCENT_MAX:
                            fail_code = 411
                            is_pass_slide_1_check = True

                    if is_pass_slide_1_check:
                        if slide_percent_2 >= SLIDE_2_PERCENT_MIN and slide_percent_2 <= SLIDE_2_PERCENT_MAX:
                            fail_code = 420

                            if not is_end_with_vertical:
                                # normal case.
                                if not is_end_with_slash:
                                    if slide_percent_3 >= SLIDE_3_PERCENT_MIN and slide_percent_3 <= SLIDE_3_PERCENT_MAX:
                                        is_match_pattern = True
                                else:
                                    # end with splash.
                                    if slide_percent_3 >= SLIDE_33_PERCENT_MIN and slide_percent_3 <= SLIDE_33_PERCENT_MAX:
                                        is_match_pattern = True
                            else:
                                # end with vertical
                                if slide_percent_3 >= SLIDE_13_PERCENT_MIN and slide_percent_3 <= SLIDE_13_PERCENT_MAX:
                                    is_match_pattern = True

                            # for uni8F1F「輟」
                            # very short edge.
                            # ps: 這個可能會 is_end_with_slash / is_end_with_vertical / is_end_with_horizon
                            if not is_match_pattern:
                                if format_dict_array[(idx+3)%nodes_length]['distance'] <= 20:
                                    if slide_percent_3 >= SLIDE_43_PERCENT_MIN and slide_percent_3 <= SLIDE_43_PERCENT_MAX:
                                        is_match_pattern = True

                if is_debug_mode:
                    if not is_match_pattern:
                        print("#", idx,": debug fail_code#106:", fail_code)
                        pass
                    else:
                        print("match rule #106")
                        print(idx,"debug rule106:",format_dict_array[idx]['code'])
                        pass

                if is_match_pattern:
                    if self.config.PROCESS_MODE == "SPRING":
                        # update 1
                        if not is_end_with_slash:
                            # normal case.
                            new_code = " %d %d l 1\n" % (format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'])
                            format_dict_array[(idx+2)%nodes_length]['code']=new_code

                            # only convert c to l.
                            new_code = " %d %d l 1\n" % (format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'])
                            format_dict_array[(idx+3)%nodes_length]['code']=new_code
                        else:
                            # end with slash.
                            new_code = " %d %d l 1\n" % (format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'])
                            format_dict_array[(idx+2)%nodes_length]['code']=new_code
                            
                            # convert c to l, and move y position.
                            new_code = " %d %d l 1\n" % (format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'])
                            format_dict_array[(idx+3)%nodes_length]['code']=new_code


                        self.apply_code(format_dict_array, (idx+2)%nodes_length)
                        self.apply_code(format_dict_array, (idx+3)%nodes_length)

                    if self.config.PROCESS_MODE == "MEATBALL":
                        self.apply_round(format_dict_array,idx)
    
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

        return redo_travel, resume_idx, inside_stroke_dict,skip_coordinate, skip_coordinate_rule
