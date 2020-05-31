import copy

def have_steps(row):
    steps = []
    for index in range(len(row)):
        step = row[index]
        if step != '0':
            steps.append((index+1, step))
    return steps

def opp_foot(foot):
    if foot == 'X' or foot == 'x':
        return 'Y'
    else:  # foot == 'Y' or foot == 'y'
        return 'X'

def copy_hold_from_list(lst):
    result = []
    for ele in lst:
        if ele[0] == 'x' or ele[0] == 'y' or ele[0] == 'z':
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

def det_first_foot(arrow, prev_step=[('X', 5), ('Y', 6)]):
    hold = copy_hold_from_list(prev_step)
    if hold:
        return opp_foot(hold[0][0])

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

def det_jump_foot(left_arrow, right_arrow, prev_step):
    bracketables = [(3,4), (2,3), (3,5), (1,3),
                    (8,9), (7,8), (8,10), (6,8),
                    (4,7), (5,6)]
    if len(prev_step) > 2:  # after brackets and quads, just reset
        return ('X', 'Y')

    hold = copy_hold_from_list(prev_step)
    if len(hold) == 1:
        if (left_arrow, right_arrow) in bracketables or (right_arrow, left_arrow) in bracketables:
            occupied_foot = hold[0][0]
            free_foot = opp_foot(occupied_foot)
            return (free_foot, free_foot)

    for step in prev_step:
        if step[1] == left_arrow:
            return (step[0].upper(), opp_foot(step[0].upper()))
        elif step[1] == right_arrow:
            return (opp_foot(step[0].upper()), step[0].upper())

    return ('X', 'Y')  # if completely new jumps
    # TODO: need to take care of exception in middle fours
    # TODO: need to take care of hold + brackets

def prev_foot(arrow, prev_step):
    for step in prev_step:
        if step[1] == arrow:
            return step[0].upper()

def group_brackets(array_of_arrows, prev_step):
    # ordered brackets: top before bottom, right before left
    bracketables = [(3,4), (2,3), (3,5), (1,3),
                    (8,9), (7,8), (8,10), (6,8),
                    (4,7), (5,6)]

    result = []
    plain_arrows = [arrow[0] for arrow in array_of_arrows]
    assign_to_left = []
    assign_to_right = []

    if len(plain_arrows) == 3:  # for triples, follow preferred placing for center step
        for tup in bracketables:
            if tup[0] in plain_arrows and tup[1] in plain_arrows:  # can be bracketed
                if tup[0] == plain_arrows[0]:
                    if prev_foot(tup[0], prev_step) == 'Y' or prev_foot(tup[1], prev_step) == 'Y':
                        assign_to_right = [tup[0], tup[1]]
                    else:  # prev_foot == 'X' or None
                        assign_to_left = [tup[0], tup[1]]
                else:
                    if prev_foot(tup[0], prev_step) == 'X' or prev_foot(tup[1], prev_step) == 'X':
                        assign_to_left = [tup[0], tup[1]]
                    else:  # prev_foot == 'Y' or None
                        assign_to_right = [tup[0], tup[1]]
                break

        if not assign_to_right:
            for arrow in plain_arrows:
                if arrow not in assign_to_left:
                    assign_to_right.append(arrow)
        if not assign_to_left:
            for arrow in plain_arrows:
                if arrow not in assign_to_right:
                    assign_to_left.append(arrow)

    elif len(plain_arrows) == 4:  # for quads, there is only one way
        assign_to_left.append(plain_arrows[0])  # TODO: middle four exception, can be both ways
        for arrow in plain_arrows[1:]:
            if (plain_arrows[0], arrow) in bracketables and len(assign_to_left) < 2:
                assign_to_left.append(arrow)
            else:
                assign_to_right.append(arrow)

    return (assign_to_left, assign_to_right)

def det_type(foot, type):
    if type == '1':
        return foot.upper()
    elif type == '2':
        return foot.lower()

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
                left_arrow, left_type = array_of_arrows[0]
                right_arrow, right_type = array_of_arrows[1]
                jump_foot = det_jump_foot(left_arrow, right_arrow, prev_step)
                prev_step = copy_hold_from_list(prev_step)

                if left_type != '3':
                    next_left = det_type(jump_foot[0], left_type)
                    row[left_arrow-1] = next_left
                    prev_step.append((next_left, left_arrow))
                else:
                    prev_step = remove_hold_from_list(prev_step, left_arrow)

                if right_type != '3':
                    next_right = det_type(jump_foot[1], right_type)
                    row[right_arrow-1] = next_right
                    prev_step.append((next_right, right_arrow))
                else:
                    prev_step = remove_hold_from_list(prev_step, right_arrow)

            elif len(array_of_arrows) == 3 or len(array_of_arrows) == 4:  # triples, quads
                left, right = group_brackets(array_of_arrows, prev_step)
                prev_step = copy_hold_from_list(prev_step)

                for arrow in array_of_arrows:
                    if arrow[0] in left:
                        left_arrow, left_type = arrow
                        if left_type != '3':
                            next_left = det_type('X', left_type)
                            row[left_arrow-1] = next_left
                            prev_step.append((next_left, left_arrow))
                        else:
                            prev_step = remove_hold_from_list(prev_step, left_arrow)

                    else:  # arrow[0] in right
                        right_arrow, right_type = arrow
                        if right_type != '3':
                            next_right = det_type('Y', right_type)
                            row[right_arrow-1] = next_right
                            prev_step.append((next_right, right_arrow))
                        else:
                            prev_step = remove_hold_from_list(prev_step, right_arrow)

            elif len(array_of_arrows) > 4:  # hands
                pass  # ignore hands for now

            else:  # single arrow
                arrow, arrow_type = array_of_arrows[0]

                if not prev_step:  # first step
                    foot = det_first_foot(arrow)
                    prev_step = copy_hold_from_list(prev_step)
                    if arrow_type != '3':
                        next_foot = det_type(foot, arrow_type)
                        row[arrow-1] = next_foot
                        prev_step.append((next_foot, arrow))
                    else:  # arrow_type == '3'
                        pass  # will never see hold tip in the beginning

                elif len(prev_step) == 1:  # after a single step
                    tup = prev_step[0]
                    prev_foot, prev_arrow = tup

                    if prev_arrow == arrow:  # repeated tap, same foot
                        prev_step = copy_hold_from_list(prev_step)
                        if arrow_type != '3':
                            next_foot = det_type(prev_foot, arrow_type)
                            row[arrow-1] = next_foot
                            prev_step.append((next_foot, arrow))
                        else:
                            prev_step = remove_hold_from_list(prev_step, arrow)        
                        
                    else:  # change leg every time
                        if prev_foot != 'Z':
                            foot = opp_foot(prev_foot)
                        else:
                            # TODO: the previous foot must change too
                            foot = det_first_foot(arrow, prev_step)

                        prev_step = copy_hold_from_list(prev_step)
                        if arrow_type != '3':
                            next_foot = det_type(foot, arrow_type)
                            row[arrow-1] = next_foot
                            prev_step.append((next_foot, arrow))
                        else:
                            prev_step = remove_hold_from_list(prev_step, arrow)

                else:  # after a jump, triple, etc
                    same_foot = False
                    for tup in prev_step:
                        if tup[1] == arrow:
                            same_foot = True
                            prev_step = copy_hold_from_list(prev_step)
                            if arrow_type != '3':
                                next_foot = det_type(tup[0], arrow_type)
                                row[arrow-1] = next_foot
                                prev_step.append((next_foot, arrow))
                            else:
                                prev_step = remove_hold_from_list(prev_step, arrow)
                            break

                    if not same_foot:
                        foot = det_first_foot(arrow, prev_step)  # pretty much reset like beginning

                        prev_step = copy_hold_from_list(prev_step)
                        if arrow_type != '3':
                            next_foot = det_type(foot, arrow_type)
                            row[arrow-1] = next_foot
                            prev_step.append((next_foot, arrow))
                        else:
                            prev_step = remove_hold_from_list(prev_step, arrow)

    return result
