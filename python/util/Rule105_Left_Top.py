#!/usr/bin/env python3
#encoding=utf-8

from . import spline_util
from . import Rule

# RULE # 105
# 直線左上角的三角形轉長方形
# PS: 因為 array size change, so need redo.
class Rule(Rule.Rule):
    def __init__(self):
        pass

    def apply(self, spline_dict, resume_idx, inside_stroke_dict,skip_coordinate, skip_coordinate_rule):
        redo_travel=False
        check_first_point = False

        SLASH_LENGTH_MIN = 35
        SLASH_LENGTH_MAX = 180

        # default: 1.10
        SLIDE_1_PERCENT_MIN = 0.90
        SLIDE_1_PERCENT_MAX = 1.30

        # default: 1.95
        SLIDE_2_PERCENT_MIN = 1.80
        SLIDE_2_PERCENT_MAX = 1.99

        # default: 1.2 for (uni695C,楜)
        SLIDE_12_PERCENT_MIN = 1.05
        SLIDE_12_PERCENT_MAX = 1.35

        # default: 1.38 for (uni8236,舶)
        # default: 1.77 for (uni6B1E,欞)
        # default: 1.89 for (uni66AB,暫)
        SLIDE_22_PERCENT_MIN = 1.28
        SLIDE_22_PERCENT_MAX = 1.94

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
                    debug_coordinate_list = [[575,628]]
                    if not([format_dict_array[idx]['x'],format_dict_array[idx]['y']] in debug_coordinate_list):
                        continue

                    print("="*30)
                    print("index:", idx)
                    for debug_idx in range(8):
                        print(debug_idx-2,": val#105:",format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['code'],'-(',format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['distance'],')')

                # begin travel.
                is_match_pattern = True

                # begin with slash.
                is_begin_with_slash = False

                # match ?ll
                if is_match_pattern:
                    fail_code = 100
                    is_match_pattern = False

                    if format_dict_array[(idx+1)%nodes_length]['t'] == 'l':
                        if format_dict_array[(idx+2)%nodes_length]['t'] == 'l':
                            is_match_pattern = True
                    else:
                        # == 'c'
                        # for uni645C 貫
                        if format_dict_array[(idx+0)%nodes_length]['distance'] >= 60:
                            if format_dict_array[(idx+1)%nodes_length]['x'] > format_dict_array[(idx+0)%nodes_length]['x']:
                                if format_dict_array[(idx+1)%nodes_length]['y'] > format_dict_array[(idx+0)%nodes_length]['y']:
                                    is_match_pattern = True
                                    is_begin_with_slash = True

                is_end_with_vertical = False

                if is_match_pattern:
                    fail_code = 200
                    is_match_pattern = False

                    is_pass_edge_1_check = False

                    if format_dict_array[(idx+0)%nodes_length]['x_equal_fuzzy']:
                        if format_dict_array[(idx+0)%nodes_length]['y_direction'] > 0:
                            is_pass_edge_1_check = True

                    if is_begin_with_slash:
                        is_pass_edge_1_check = True

                    if is_pass_edge_1_check:
                        if format_dict_array[(idx+1)%nodes_length]['x_direction']>0:
                            if format_dict_array[(idx+1)%nodes_length]['y_direction']<0:
                                
                                # case 1: horizon
                                if format_dict_array[(idx+2)%nodes_length]['y_equal_fuzzy']:
                                    if format_dict_array[(idx+2)%nodes_length]['x_direction']>0:
                                        is_match_pattern = True

                                # case 2: vertical
                                if format_dict_array[(idx+2)%nodes_length]['x_equal_fuzzy']:
                                    is_match_pattern = True
                                    is_end_with_vertical = True

                                # case 3: slash
                                # for case uni642C 搬。
                                if format_dict_array[(idx+3)%nodes_length]['x'] > format_dict_array[(idx+2)%nodes_length]['x']:
                                    if format_dict_array[(idx+3)%nodes_length]['y'] > format_dict_array[(idx+2)%nodes_length]['y']:
                                        is_match_pattern = True
                                        is_end_with_vertical = True


                # skip small angle
                if is_match_pattern:
                    fail_code = 300
                    is_match_pattern = False

                    slide_percent_1 = spline_util.slide_percent(format_dict_array[(idx+0)%nodes_length]['x'],format_dict_array[(idx+0)%nodes_length]['y'],format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'])
                    slide_percent_2 = spline_util.slide_percent(format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'],format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'])

                    #if True:
                    #if False:
                    if is_debug_mode:
                        print("slide_percent 1:", slide_percent_1)
                        print("data:",format_dict_array[(idx+0)%nodes_length]['x'],format_dict_array[(idx+0)%nodes_length]['y'],format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'])
                        print("slide_percent 2:", slide_percent_2)
                        print("data:",format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y'],format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y'])

                        print("is_end_with_vertical:", is_end_with_vertical)

                    # come from horizon
                    if slide_percent_1 >= SLIDE_1_PERCENT_MIN and slide_percent_1 <= SLIDE_1_PERCENT_MAX:
                        fail_code = 310

                        if not is_end_with_vertical:
                            fail_code = 320
                            # horizon.
                            if slide_percent_2 >= SLIDE_2_PERCENT_MIN and slide_percent_2 <= SLIDE_2_PERCENT_MAX:
                                is_match_pattern = True
                        else:
                            fail_code = 330
                            # slash or vertical.
                            if slide_percent_2 >= SLIDE_12_PERCENT_MIN and slide_percent_2 <= SLIDE_12_PERCENT_MAX:
                                is_match_pattern = True
                            else:
                                # for uni6B1E,欞的口
                                # for long edge, large angel.
                                fail_code = 340
                                
                                if format_dict_array[(idx+0)%nodes_length]['x_equal_fuzzy']:
                                    if format_dict_array[(idx+1)%nodes_length]['distance']>=80:
                                        if slide_percent_2 >= SLIDE_22_PERCENT_MIN and slide_percent_2 <= SLIDE_22_PERCENT_MAX:
                                            is_match_pattern = True

                                # for uni66AB,暫的斤
                                if not is_match_pattern:
                                    fail_code = 350
                                    if format_dict_array[(idx+0)%nodes_length]['x_equal_fuzzy']:
                                        if format_dict_array[(idx+1)%nodes_length]['match_stroke_width']:
                                            if format_dict_array[(idx+0)%nodes_length]['distance']>=90:
                                                if format_dict_array[(idx+2)%nodes_length]['distance']>=90:
                                                    if format_dict_array[(idx+0)%nodes_length]['distance'] > format_dict_array[(idx+1)%nodes_length]['distance']:
                                                        if format_dict_array[(idx+2)%nodes_length]['distance'] > format_dict_array[(idx+1)%nodes_length]['distance']:
                                                            if slide_percent_2 >= SLIDE_22_PERCENT_MIN and slide_percent_2 <= SLIDE_22_PERCENT_MAX:
                                                                is_match_pattern = True


                if is_debug_mode:
                    if not is_match_pattern:
                        print("#", idx,": debug fail_code#105:", fail_code)
                        pass
                    else:
                        print("match rule #105")
                        print(idx,"debug rule105:",format_dict_array[idx]['code'])
                        pass

                if is_match_pattern:
                    # update 1
                    old_code = format_dict_array[(idx+1)%nodes_length]['code']
                    old_code_array = old_code.split(' ')
                    if format_dict_array[(idx+1)%nodes_length]['t']=='l':
                        old_code_array[2]=str(format_dict_array[(idx+2)%nodes_length]['y'])
                    else:
                        old_code_array[6]=str(format_dict_array[(idx+2)%nodes_length]['y'])
                    new_code = ' '.join(old_code_array)
                    format_dict_array[(idx+1)%nodes_length]['code']=new_code
                    self.apply_code(format_dict_array, (idx+1)%nodes_length)
                    
                    if is_debug_mode:
                        print("old_code +1:", old_code)
                        print("new_code +1:", new_code)

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
