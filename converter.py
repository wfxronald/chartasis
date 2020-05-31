import copy

def have_steps(row):
    steps = []
    for index in range(len(row)):
        step = row[index]
        if step != '0':
            steps.append((index+1, step))
    return steps

def det_first_foot(arrow, prev_step=[('X', 5), ('Y', 6)]):
    left = [1,2,3,4,5]
    right = [6,7,8,9,10]

    have_left, have_right = False, False
    if arrow in left:
        have_left = True
    else:  # arrow in right
        have_right = True
        
    for step in prev_step:
        if step[1] in left:
            have_left = True
        else:  # step[1] in right
            have_right = True

    if have_left and have_right:  # double mode
        if arrow <= 5:  # left pad
            return 'X'
        else:  # right pad
            return 'Y'
    elif have_left:  # single mode, left
        if arrow < 3:  # down left, up left
            return 'X'
        elif arrow > 3:  # down right, up right
            return 'Y'
        else:  # center arrow
            return 'Z'
    elif have_right:  # single mode, right
        if arrow < 8:  # down left, up left
            return 'X'
        elif arrow > 8:  # down right, up right
            return 'Y'
        else:  # center arrow
            return 'Z'
    else:  # will not go here
        pass

def opp_foot(foot):
    if foot == 'X' or foot == 'x':
        return 'Y'
    else:  # foot == 'Y' or foot == 'y'
        return 'X'

def copy_hold_from_list(lst):
    result = []
    for ele in lst:
        if ele[0] == 'x' or ele[0] == 'y':
            result.append((ele[0], ele[1]))
    return result

def remove_hold_from_list(lst, arrow):
    result = []
    for ele in lst:
        if ele[1] != arrow:
            result.append((ele[0], ele[1]))
        else:
            result.append((ele[0].upper(), ele[1]))  # convert to normal step
    return result

def det_jump_foot(left_arrow, right_arrow, prev_step):
    for step in prev_step:
        if step[1] == left_arrow:
            return (step[0].upper(), opp_foot(step[0].upper()))
        elif step[1] == right_arrow:
            return (opp_foot(step[0].upper()), step[0].upper())

    return ('X', 'Y')  # if completely new jumps
    # TODO: need to take care of exception in middle fours

# Main function
def convert_to_lr(array_format):
    result = copy.deepcopy(array_format)
    prev_step = []  # format: [('X', 5), ('Y', 6)]

    for measure in result:
        for row in measure:
            if not have_steps(row):  # A row of all zeroes 
                continue

            array_of_arrows = have_steps(row)  # format: [(5, '1'), (6, '1')]

            if len(array_of_arrows) == 2:  # jumps
                left_arrow, left_type = array_of_arrows[0][0], array_of_arrows[0][1]
                right_arrow, right_type = array_of_arrows[1][0], array_of_arrows[1][1]
                jump_foot = det_jump_foot(left_arrow, right_arrow, prev_step)
                prev_step = copy_hold_from_list(prev_step)

                if left_type == '1':
                    next_left = jump_foot[0].upper()
                elif left_type == '2':
                    next_left = jump_foot[0].lower()
                else:
                    prev_step = remove_hold_from_list(prev_step, left_arrow)

                if left_type != '3':
                    row[left_arrow-1] = next_left
                    prev_step.append((next_left, left_arrow))


                if right_type == '1':
                    next_right = jump_foot[1].upper()
                elif right_type == '2':
                    next_right = jump_foot[1].lower()
                else:
                    prev_step = remove_hold_from_list(prev_step, right_arrow)

                if right_type != '3':
                    row[right_arrow-1] = next_right
                    prev_step.append((next_right, right_arrow))

            elif len(array_of_arrows) > 2:
                pass
                # TODO: need to handle triples, brackets

            else:  # single arrow
                arrow, arrow_type = array_of_arrows[0][0], array_of_arrows[0][1]

                if not prev_step:  # first step
                    foot = det_first_foot(arrow)

                    prev_step = copy_hold_from_list(prev_step)
                    if arrow_type == '1':
                        next_foot = foot.upper()
                    elif arrow_type == '2':
                        next_foot = foot.lower()
                    else:  # arrow_type == '3'
                        pass  # will never see hold tip in the beginning

                    if arrow_type != '3':
                        row[arrow-1] = next_foot
                        prev_step.append((next_foot, arrow))

                elif len(prev_step) == 1:  # after a single step
                    tup = prev_step[0]
                    prev_foot, prev_arrow = tup[0], tup[1]

                    if prev_arrow == arrow:  # repeated tap, same foot
                        prev_step = copy_hold_from_list(prev_step)
                        if arrow_type == '1':
                            next_foot = prev_foot.upper()
                        elif arrow_type == '2':
                            next_foot = prev_foot.lower()
                        else:
                            prev_step = remove_hold_from_list(prev_step, arrow)

                        if arrow_type != '3':
                            row[arrow-1] = next_foot
                            prev_step.append((next_foot, arrow))
                        
                    else:  # change leg every time
                        if prev_foot != 'Z':
                            foot = opp_foot(prev_foot)
                        else:
                            # TODO: the previous foot must change too
                            foot = det_first_foot(arrow, prev_step)

                        prev_step = copy_hold_from_list(prev_step)
                        if arrow_type == '1':
                            next_foot = foot.upper()
                        elif arrow_type == '2':
                            next_foot = foot.lower()
                        else:
                            prev_step = remove_hold_from_list(prev_step, arrow)

                        if arrow_type != '3':
                            row[arrow-1] = next_foot
                            prev_step.append((next_foot, arrow))

                else:  # after a jump, triple, etc
                    same_foot = False
                    for tup in prev_step:
                        if tup[1] == arrow:
                            same_foot = True
                            prev_step = copy_hold_from_list(prev_step)
                            if arrow_type == '1':
                                next_foot = tup[0].upper()
                            elif arrow_type == '2':
                                next_foot = tup[0].lower()
                            else:
                                prev_step = remove_hold_from_list(prev_step, arrow)

                            if arrow_type != '3':
                                row[arrow-1] = next_foot
                                prev_step.append((next_foot, arrow))
                            break

                    if not same_foot:
                        foot = det_first_foot(arrow, prev_step)  # pretty much reset like beginning

                        prev_step = copy_hold_from_list(prev_step)
                        if arrow_type == '1':
                            next_foot = foot.upper()
                        elif arrow_type == '2':
                            next_foot = foot.lower()
                        else:
                            prev_step = remove_hold_from_list(prev_step, arrow)

                        if arrow_type != '3':
                            row[arrow-1] = next_foot
                            prev_step.append((next_foot, arrow))

    return result
