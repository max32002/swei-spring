#!/usr/bin/env python3
#encoding=utf-8

from . import spline_util
from . import Rule

# RULE # 107
# 八 的右上角三角形
class Rule(Rule.Rule):
    def __init__(self):
        pass

    def apply(self, spline_dict, resume_idx, inside_stroke_dict,skip_coordinate, skip_coordinate_rule):
        redo_travel=False
        check_first_point = False

        # default: 1.15 (uni39D2,㧒)
        # default: 1.11 (uni39D2,㧒)
        SLIDE_1_PERCENT_MIN = 0.99
        SLIDE_1_PERCENT_MAX = 1.27

        # default: 1.625 (uni39D2,㧒)
        SLIDE_2_PERCENT_MIN = 1.475
        SLIDE_2_PERCENT_MAX = 1.755

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
                    debug_coordinate_list = [[689,836]]
                    if not([format_dict_array[idx]['x'],format_dict_array[idx]['y']] in debug_coordinate_list):
                        continue

                    print("="*30)
                    print("index:", idx)
                    for debug_idx in range(8):
                        print(debug_idx-2,": val#107:",format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['code'],'-(',format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['distance'],')')

                # begin travel.
                is_match_pattern = True

                # match 
                if is_match_pattern:
                    fail_code = 100
                    is_match_pattern = False
                    
                    if format_dict_array[(idx+1)%nodes_length]['t'] == 'l':
                        if format_dict_array[(idx+2)%nodes_length]['t'] == 'c':
                            is_match_pattern = True

                if is_match_pattern:
                    fail_code = 200
                    is_match_pattern = False
                    if format_dict_array[(idx+0)%nodes_length]['distance'] >= self.config.ROW_TRIANGLE_HEIGHT_MIN:
                        fail_code = 201
                        if format_dict_array[(idx+0)%nodes_length]['distance'] <= self.config.ROW_TRIANGLE_HEIGHT_MAX:
                            fail_code = 202
                            if format_dict_array[(idx+1)%nodes_length]['distance'] >= self.config.ROW_TRIANGLE_SLIDE_MIN:
                                fail_code = 203
                                if format_dict_array[(idx+1)%nodes_length]['distance'] <= self.config.ROW_TRIANGLE_SLIDE_MAX:
                                    if format_dict_array[(idx+2)%nodes_length]['distance'] >= 100:
                                        if format_dict_array[(idx+2)%nodes_length]['distance'] > format_dict_array[(idx+1)%nodes_length]['distance']:
                                            if format_dict_array[(idx+2)%nodes_length]['distance'] > format_dict_array[(idx+0)%nodes_length]['distance']:
                                                is_match_pattern = True

                if is_match_pattern:
                    fail_code = 300
                    is_match_pattern = False

                    if format_dict_array[(idx+0)%nodes_length]['x_direction']>0:
                        if format_dict_array[(idx+0)%nodes_length]['y_direction']<0:
                            fail_code = 320
                            if format_dict_array[(idx+1)%nodes_length]['x_direction']<0:
                                if format_dict_array[(idx+1)%nodes_length]['y_direction']<0:
                                    fail_code = 330
                                    if format_dict_array[(idx+2)%nodes_length]['x_direction']>0:
                                        if format_dict_array[(idx+2)%nodes_length]['y_direction']<0:
                                            is_match_pattern = True

                    # 針對成功的做排除。
                    # for case: 氫 的巠.
                    if is_match_pattern:
                        if format_dict_array[(idx-1+nodes_length)%nodes_length]['distance'] > format_dict_array[(idx+1)%nodes_length]['distance']:
                            if format_dict_array[(idx-1+nodes_length)%nodes_length]['distance'] > format_dict_array[(idx+0)%nodes_length]['distance']:
                                if format_dict_array[(idx-1+nodes_length)%nodes_length]['x_direction'] > 0:
                                    if format_dict_array[(idx-1+nodes_length)%nodes_length]['y_direction'] > 0:
                                        fail_code = 340
                                        is_match_pattern = False

                    # for case: uni9127,鄧的登。
                    if is_match_pattern:
                        if format_dict_array[(idx+2)%nodes_length]['x'] < format_dict_array[(idx+0)%nodes_length]['x']:
                            fail_code = 341
                            is_match_pattern = False

                # skip small angle
                if is_match_pattern:
                    fail_code = 400
                    is_match_pattern = False

                    slide_percent_1 = 0
                    slide_percent_2 = 0

                    slide_percent_1 = spline_util.slide_percent(format_dict_array[(idx+0)%nodes_length]['x'],format_dict_array[(idx+0)%nodes_length]['y'],format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'])
                    slide_percent_2 = spline_util.slide_percent(format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'],format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'])

                    if is_debug_mode:
                        print("slide_percent 1:", slide_percent_1)
                        print("data:",format_dict_array[(idx+0)%nodes_length]['x'],format_dict_array[(idx+0)%nodes_length]['y'],format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'])
                        print("slide_percent 2:", slide_percent_2)
                        print("data:",format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'],format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'])

                    if slide_percent_1 >= SLIDE_1_PERCENT_MIN and slide_percent_1 <= SLIDE_1_PERCENT_MAX:
                        fail_code = 410
                        if slide_percent_2 >= SLIDE_2_PERCENT_MIN and slide_percent_2 <= SLIDE_2_PERCENT_MAX:
                            is_match_pattern = True

                if is_debug_mode:
                    if not is_match_pattern:
                        print("#", idx,": debug fail_code#107:", fail_code)
                        pass
                    else:
                        print("match rule #107")
                        print(idx,"debug rule107:",format_dict_array[idx]['code'])
                        pass

                if is_match_pattern:
                    # convert c to l
                    if format_dict_array[(idx+2)%nodes_length]['t'] == 'c':
                        new_code = " %d %d l 1\n" % (format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'])
                        format_dict_array[(idx+2)%nodes_length]['t']='l'
                        format_dict_array[(idx+2)%nodes_length]['code']=new_code
                        self.apply_code(format_dict_array, (idx+2)%nodes_length)

                    del format_dict_array[(idx+1)%nodes_length]
                    if idx > (idx+1)%nodes_length:
                        idx -=1
                    nodes_length = len(format_dict_array)
    
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
