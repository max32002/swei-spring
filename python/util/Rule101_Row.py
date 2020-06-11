#!/usr/bin/env python3
#encoding=utf-8

from . import spline_util
from . import Rule

# RULE # 101
# 橫線右邊三角形轉長方形
# PS: 因為 array size change, so need redo.
class Rule(Rule.Rule):
    def __init__(self):
        pass

    def apply(self, spline_dict, resume_idx, inside_stroke_dict,skip_coordinate):
        redo_travel=False
        check_first_point = False

        # default: 1.76, (.26310, 為) 1.83
        SLIDE_1_PERCENT_MIN = 1.66
        SLIDE_1_PERCENT_MAX = 1.94

        # default: 0.63 (.2639,真) 0.76
        VERTICAL_SLIDE_1_PERCENT_MIN = 0.53
        VERTICAL_SLIDE_1_PERCENT_MAX = 0.89

        # default: 1.36 to 1.2, (.26310, 為) 1.46
        SLIDE_2_PERCENT_MIN = 1.10
        SLIDE_2_PERCENT_MAX = 1.56

        # default: 1.13 to 1.26,(.2639,真)1.36, (.26356, 片) 1.0, (.10924, 公) 0.80
        SLIDE_3_PERCENT_MIN = 0.70
        SLIDE_3_PERCENT_MAX = 1.47

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

                # 要轉換的角，不能就是我們產生出來的點。
                if [format_dict_array[idx]['x'],format_dict_array[idx]['y']] in skip_coordinate:
                    continue

                is_debug_mode = False
                #is_debug_mode = True

                if is_debug_mode:
                    debug_coordinate_list = [[563,183]]
                    if not([format_dict_array[idx]['x'],format_dict_array[idx]['y']] in debug_coordinate_list):
                        continue

                    print("="*30)
                    print("index:", idx)
                    for debug_idx in range(8):
                        print(debug_idx-2,": val#101:",format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['code'],'-(',format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['distance'],')')

                # begin travel.
                is_match_pattern = True

                # come from vertical line
                is_from_vertical = False

                # two kind of chini
                is_flat_chin = False

                # from right to left.
                is_goto_left = False

                # slash mode, for case:.12816
                is_slash_with_arm = False

                # for case:湖的月，左右的二個三角形直接連在一起。
                is_slash_with_triangle = False

                # match ?ll?c
                if is_match_pattern:
                    fail_code = 100
                    is_match_pattern = False
                    if format_dict_array[(idx+1)%nodes_length]['t'] == 'l':
                        if format_dict_array[(idx+2)%nodes_length]['t'] == 'l':
                            if format_dict_array[(idx+4)%nodes_length]['t'] == 'c':
                                is_match_pattern = True

                            if format_dict_array[(idx+4)%nodes_length]['t'] == 'l':
                                is_match_pattern = True
                                is_flat_chin = True

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
                                    fail_code = 204

                                    if not is_flat_chin:
                                        fail_code = 210
                                        # curve chin
                                        if format_dict_array[(idx+3)%nodes_length]['distance'] >= self.config.ROW_TRIANGLE_CHIN_MIN:
                                            fail_code = 211
                                            if format_dict_array[(idx+3)%nodes_length]['distance'] <= self.config.ROW_TRIANGLE_CHIN_MAX:
                                                is_match_pattern = True
                                    else:
                                        fail_code = 220
                                        # flat chin
                                        if format_dict_array[(idx+3)%nodes_length]['distance'] >= self.config.ROW_TRIANGLE_FLAT_CHIN_MIN:
                                            fail_code = 221
                                            if format_dict_array[(idx+3)%nodes_length]['distance'] <= self.config.ROW_TRIANGLE_FLAT_CHIN_MAX:
                                                is_match_pattern = True

                if is_match_pattern:
                    fail_code = 300
                    is_match_pattern = False
                    # 右上角的三角形。
                    if format_dict_array[(idx+0)%nodes_length]['x_direction'] > 0:
                        if format_dict_array[(idx+1)%nodes_length]['x_direction'] > 0:
                            if format_dict_array[(idx+2)%nodes_length]['x_direction'] > 0:
                                if format_dict_array[(idx+3)%nodes_length]['x_direction'] < 0:
                                    is_match_pattern = True

                    # allow +0 vertical or horizontal
                    if format_dict_array[(idx+0)%nodes_length]['x_equal_fuzzy']:
                        if format_dict_array[(idx+1)%nodes_length]['x_direction'] > 0:
                            if format_dict_array[(idx+2)%nodes_length]['x_direction'] > 0:
                                if format_dict_array[(idx+3)%nodes_length]['x_direction'] < 0:
                                    is_match_pattern = True
                                    is_from_vertical = True

                    # 左下角的三角形。
                    if format_dict_array[(idx+0)%nodes_length]['x_direction'] < 0:
                        if format_dict_array[(idx+1)%nodes_length]['x_direction'] < 0:
                            if format_dict_array[(idx+2)%nodes_length]['x_direction'] < 0:
                                if format_dict_array[(idx+3)%nodes_length]['x_direction'] > 0:
                                    is_match_pattern = True
                                    is_goto_left = True


                if is_match_pattern:
                    fail_code = 400
                    is_match_pattern = False
                    # allow +0 vertical or horizontal
                    if format_dict_array[(idx+0)%nodes_length]['y_equal_fuzzy']:
                        fail_code = 410
                        if format_dict_array[(idx+1)%nodes_length]['y_direction'] > 0:
                            if format_dict_array[(idx+2)%nodes_length]['y_direction'] < 0:
                                if format_dict_array[(idx+3)%nodes_length]['y_direction'] < 0:
                                    is_match_pattern = True

                    if is_from_vertical:
                        fail_code = 420
                        if format_dict_array[(idx+1)%nodes_length]['y_direction'] > 0:
                            if format_dict_array[(idx+2)%nodes_length]['y_direction'] < 0:
                                if format_dict_array[(idx+3)%nodes_length]['y_direction'] < 0:
                                    is_match_pattern = True

                    # 左下角的三角形。
                    if is_goto_left:
                        fail_code = 430
                        if format_dict_array[(idx+0)%nodes_length]['y_equal_fuzzy']:
                            if format_dict_array[(idx+1)%nodes_length]['y_direction'] < 0:
                                if format_dict_array[(idx+2)%nodes_length]['y_direction'] > 0:
                                    if format_dict_array[(idx+3)%nodes_length]['y_direction'] > 0:
                                        is_match_pattern = True

                    # 增加新的 case: not horizontal line
                    RIGHT_ARM_LENGTH_MIN = 100
                    RIGHT_ARM_VERTICAL_DIFF_MAX = 3
                    RIGHT_ARM_HORIZONTAL_DIFF_MAX = 3
                    # for case:.12816 「嘠」.
                    # for case:.15996 尾。
                    if not is_match_pattern:
                        fail_code = 440

                        new_x2, new_y2 = spline_util.two_point_extend(format_dict_array[(idx+4)%nodes_length]['x'],format_dict_array[(idx+4)%nodes_length]['y'],format_dict_array[(idx+5)%nodes_length]['x'],format_dict_array[(idx+5)%nodes_length]['y'],-1 * format_dict_array[(idx+0)%nodes_length]['distance'])
                        next_line_distance = spline_util.get_distance(new_x2, new_y2,format_dict_array[(idx+5)%nodes_length]['x'],format_dict_array[(idx+5)%nodes_length]['y'])
                        left_height = abs(format_dict_array[(idx+0)%nodes_length]['y']-format_dict_array[(idx+5)%nodes_length]['y'])
                        right_height = abs(format_dict_array[(idx+1)%nodes_length]['y']-new_y2)
                        height_diff = abs(left_height - right_height)
                        width_diff = abs(format_dict_array[(idx+0)%nodes_length]['distance'] - next_line_distance)
                        if is_debug_mode:
                            print("+0 length:", format_dict_array[(idx+0)%nodes_length]['distance'])
                            print("maybe next line end coordinate:",new_x2, new_y2)
                            print("left_height:", left_height)
                            print("right_height:", right_height)
                            print("height_diff:", height_diff)
                            print("width_diff:", width_diff)

                        if height_diff <= RIGHT_ARM_VERTICAL_DIFF_MAX and width_diff <= RIGHT_ARM_HORIZONTAL_DIFF_MAX:
                            if format_dict_array[(idx+0)%nodes_length]['x_direction'] > 0:
                                if format_dict_array[(idx+1)%nodes_length]['y_direction'] > 0:
                                    if format_dict_array[(idx+1)%nodes_length]['x_direction'] > 0:
                                        if format_dict_array[(idx+2)%nodes_length]['x_direction'] > 0:
                                            if format_dict_array[(idx+2)%nodes_length]['y_direction'] < 0:
                                                if format_dict_array[(idx+3)%nodes_length]['y_direction'] < 0:
                                                    if format_dict_array[(idx+4)%nodes_length]['x_direction'] < 0:
                                                        if format_dict_array[(idx+4)%nodes_length]['y_direction'] < 0:
                                                            is_match_pattern = True
                                                            is_slash_with_arm = True
                                                            pass

                    RIGHT_SLASH_WITH_TRIANGLE_LENGTH_MIN = 130
                    # 實際值是=48, 允許再多一點.
                    RIGHT_ARM_Y_GAP_MAX = 58
                    # for case:.24367 湖, 遇到 bold,black 才會遇到。
                    # 最少，手要伸這麼長才能判斷斜線。
                    if format_dict_array[(idx+0)%nodes_length]['distance'] >= RIGHT_SLASH_WITH_TRIANGLE_LENGTH_MIN:
                        fail_code = 450
                        if format_dict_array[(idx+4)%nodes_length]['distance'] >= RIGHT_SLASH_WITH_TRIANGLE_LENGTH_MIN:
                            if format_dict_array[(idx+0)%nodes_length]['y']-format_dict_array[(idx+1)%nodes_length]['y'] <= RIGHT_ARM_Y_GAP_MAX:
                                if format_dict_array[(idx+0)%nodes_length]['x_direction'] > 0:
                                    if format_dict_array[(idx+0)%nodes_length]['y_direction'] < 0:
                                        if format_dict_array[(idx+1)%nodes_length]['y_direction'] > 0:
                                            if format_dict_array[(idx+1)%nodes_length]['x_direction'] > 0:
                                                if format_dict_array[(idx+2)%nodes_length]['x_direction'] > 0:
                                                    if format_dict_array[(idx+2)%nodes_length]['y_direction'] < 0:
                                                        if format_dict_array[(idx+3)%nodes_length]['y_direction'] < 0:
                                                            if format_dict_array[(idx+4)%nodes_length]['y_direction'] < 0:
                                                                is_match_pattern = True
                                                                is_slash_with_triangle = True

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

                    if slide_percent_2 >= SLIDE_2_PERCENT_MIN and slide_percent_2 <= SLIDE_2_PERCENT_MAX:
                        fail_code = 510
                        if slide_percent_3 >= SLIDE_3_PERCENT_MIN and slide_percent_3 <= SLIDE_3_PERCENT_MAX:
                            fail_code = 520
                            if not is_from_vertical:
                                fail_code = 530
                                # come from horizon
                                if slide_percent_1 >= SLIDE_1_PERCENT_MIN and slide_percent_1 <= SLIDE_1_PERCENT_MAX:
                                    is_match_pattern = True
                            else:
                                fail_code = 540
                                # com from vertical
                                if slide_percent_1 >= VERTICAL_SLIDE_1_PERCENT_MIN and slide_percent_1 <= VERTICAL_SLIDE_1_PERCENT_MAX:
                                        is_match_pattern = True

                if is_debug_mode:
                    if not is_match_pattern:
                        print("#", idx,": debug fail_code#101:", fail_code)
                        pass
                    else:
                        print("match rule #101")
                        print(idx,"debug rule101:",format_dict_array[idx]['code'])
                        pass


                if is_match_pattern:
                    
                    if False:
                    #if True:
                        print("#"*40)
                        for debug_idx in range(8):
                            print(debug_idx-2,"values for rule101:",format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['code'])

                    is_row_mode = True
                    is_mouth_mode = False
                    is_row_vertial_mode = False


                    X_EQUAL_ACCURACY=5
                    if not is_from_vertical:
                        # come from horizon
                        if not is_goto_left:
                            if format_dict_array[(idx+4)%nodes_length]['y_direction'] < 0:
                                # for case "口"
                                if format_dict_array[(idx+5)%nodes_length]['t'] == 'l':
                                    if format_dict_array[(idx+4)%nodes_length]['x_equal_fuzzy']:
                                        is_row_mode = False
                                        is_mouth_mode = True
                                    if format_dict_array[(idx+4)%nodes_length]['x_direction'] <= 0:
                                        is_row_mode = False
                                        is_mouth_mode = True
                                # for case "包" & case:.26026,熱.
                                if format_dict_array[(idx+5)%nodes_length]['t'] == 'c':
                                    if format_dict_array[(idx+4)%nodes_length]['y_direction'] < 0:
                                        is_row_mode = False
                                        is_mouth_mode = True
                        else:
                            # from right goto left
                            if format_dict_array[(idx+4)%nodes_length]['y_direction'] > 0:
                                    # for case "口"
                                    if format_dict_array[(idx+5)%nodes_length]['t'] == 'l':
                                        if format_dict_array[(idx+4)%nodes_length]['x_equal_fuzzy']:
                                            is_row_mode = False
                                            is_mouth_mode = True
                                        if format_dict_array[(idx+4)%nodes_length]['x_direction'] >= 0:
                                            is_row_mode = False
                                            is_mouth_mode = True
                                    # for case "包"
                                    if format_dict_array[(idx+5)%nodes_length]['t'] == 'c':
                                        if format_dict_array[(idx+4)%nodes_length]['x_direction'] >= 0:
                                            is_row_mode = False
                                            is_mouth_mode = True
                    else:
                        is_row_mode = False
                        is_row_vertial_mode = True

                    if is_row_mode:
                        #print("is_row_mode")
                        ending_x = format_dict_array[(idx+3)%nodes_length]['x']
                        ending_y = format_dict_array[(idx+5)%nodes_length]['y']

                        # update 1
                        old_code = format_dict_array[(idx+1)%nodes_length]['code']
                        old_code_array = old_code.split(' ')
                        #x = int(float(old_code_array[1]))
                        #y = int(float(old_code_array[2]))
                        old_code_array[1]=str(ending_x)
                        new_code = ' '.join(old_code_array)
                        format_dict_array[(idx+1)%nodes_length]['code']=new_code
                        #print("old_code:", old_code)
                        #print("new_code:", new_code)

                        # update 2
                        old_code = format_dict_array[(idx+2)%nodes_length]['code']
                        old_code_array = old_code.split(' ')
                        #x = int(float(old_code_array[1]))
                        #y = int(float(old_code_array[2]))
                        old_code_array[1]=str(ending_x)
                        old_code_array[2]=str(ending_y)
                        new_code = ' '.join(old_code_array)
                        format_dict_array[(idx+2)%nodes_length]['code']=new_code
                        #print("old_code:", old_code)
                        #print("new_code:", new_code)

                        #print("del code:", format_dict_array[(idx+4)%nodes_length]['code'])
                        del format_dict_array[(idx+4)%nodes_length]

                        if idx > (idx+4)%nodes_length:
                            idx -= 1

                        nodes_length = len(format_dict_array)
                        #print("del code:", format_dict_array[(idx+3)%nodes_length]['code'])
                        del format_dict_array[(idx+3)%nodes_length]

                    # we generated nodes
                    #skip_coordinate.append([center_x,center_y])

                        redo_travel=True
                        check_first_point = True
                        resume_idx = -1
                        break

                    if is_mouth_mode:
                        #print("is_mouth_mode")
                        ending_x = format_dict_array[(idx+4)%nodes_length]['x']
                        ending_y = format_dict_array[(idx+0)%nodes_length]['y']
                        
                        # update 1
                        old_code = format_dict_array[(idx+2)%nodes_length]['code']
                        old_code_array = old_code.split(' ')
                        #x = int(float(old_code_array[1]))
                        #y = int(float(old_code_array[2]))
                        old_code_array[1]=str(ending_x)
                        old_code_array[2]=str(format_dict_array[(idx+1)%nodes_length]['y'])

                        # 由於 slash mode，必需使用 extend 不然 stroke 會變細。
                        #print("is_slash_with_arm:", is_slash_with_arm)
                        if is_slash_with_arm:
                            arm_distance = spline_util.get_distance(ending_x,ending_y,format_dict_array[(idx+0)%nodes_length]['x'],format_dict_array[(idx+0)%nodes_length]['y'])
                            extend_x,extend_y=spline_util.two_point_extend(format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y'],format_dict_array[(idx+0)%nodes_length]['x'],format_dict_array[(idx+0)%nodes_length]['y'], -1 * arm_distance)
                            old_code_array[1]=str(extend_x)
                            old_code_array[2]=str(extend_y)

                        new_code = ' '.join(old_code_array)
                        format_dict_array[(idx+2)%nodes_length]['code']=new_code

                        #del format_dict_array[(idx+4)%nodes_length]
                        #if idx > (idx+4)%nodes_length:
                            #idx -= 1
                        # convert c to l
                        if format_dict_array[(idx+4)%nodes_length]['t'] == 'c':
                            new_code = " %d %d l 1\n" % (format_dict_array[(idx+4)%nodes_length]['x'],format_dict_array[(idx+4)%nodes_length]['y'])
                            format_dict_array[(idx+4)%nodes_length]['t']='l'
                            format_dict_array[(idx+4)%nodes_length]['code']=new_code

                        nodes_length = len(format_dict_array)
                        del format_dict_array[(idx+3)%nodes_length]
                        if idx > (idx+3)%nodes_length:
                            idx -= 1

                        #nodes_length = len(format_dict_array)
                        #del format_dict_array[(idx+2)%nodes_length]
                        #if idx > (idx+2)%nodes_length:
                            #idx -= 1

                        redo_travel=True
                        check_first_point = True
                        resume_idx = -1
                        break

                    if is_row_vertial_mode:
                        #print("is_row_vertial_mode")

                        # PS: 因為「真」的橫線會被誤刪。

                        is_remove_tail = False

                        if is_remove_tail:
                            ending_x = format_dict_array[(idx+0)%nodes_length]['x']
                            ending_y = format_dict_array[(idx+5)%nodes_length]['y']
                            
                            # update 1
                            old_code = format_dict_array[(idx+1)%nodes_length]['code']
                            old_code_array = old_code.split(' ')
                            #x = int(float(old_code_array[1]))
                            #y = int(float(old_code_array[2]))
                            old_code_array[2]=str(ending_y)
                            new_code = ' '.join(old_code_array)
                            format_dict_array[(idx+1)%nodes_length]['code']=new_code

                            del format_dict_array[(idx+4)%nodes_length]
                            if idx > (idx+4)%nodes_length:
                                idx -= 1

                            nodes_length = len(format_dict_array)
                            del format_dict_array[(idx+3)%nodes_length]
                            if idx > (idx+3)%nodes_length:
                                idx -= 1

                            nodes_length = len(format_dict_array)
                            del format_dict_array[(idx+2)%nodes_length]
                            if idx > (idx+2)%nodes_length:
                                idx -= 1
                        else:
                            # longer.
                            #ending_x = format_dict_array[(idx+3)%nodes_length]['x']
                            # shooter
                            ending_x = format_dict_array[(idx+4)%nodes_length]['x']
                            ending_y = format_dict_array[(idx+5)%nodes_length]['y']

                            # update 1
                            old_code = format_dict_array[(idx+2)%nodes_length]['code']
                            old_code_array = old_code.split(' ')
                            #x = int(float(old_code_array[1]))
                            #y = int(float(old_code_array[2]))
                            old_code_array[1]=str(ending_x)
                            old_code_array[2]=str(format_dict_array[(idx+1)%nodes_length]['y'])
                            new_code = ' '.join(old_code_array)
                            format_dict_array[(idx+2)%nodes_length]['code']=new_code
                            #print("old_code:", old_code)
                            #print("new_code:", new_code)

                            # convert c to l
                            if format_dict_array[(idx+4)%nodes_length]['t'] == 'c':
                                new_code = " %d %d l 1\n" % (ending_x,format_dict_array[(idx+4)%nodes_length]['y'])
                                format_dict_array[(idx+4)%nodes_length]['t']='l'
                                format_dict_array[(idx+4)%nodes_length]['code']=new_code

                            nodes_length = len(format_dict_array)
                            del format_dict_array[(idx+3)%nodes_length]
                            if idx > (idx+3)%nodes_length:
                                idx -= 1

                        redo_travel=True
                        check_first_point = True
                        resume_idx = -1
                        break


        if check_first_point:
            # check close path.
            self.reset_first_point(format_dict_array, spline_dict)

        return redo_travel, resume_idx, inside_stroke_dict,skip_coordinate
