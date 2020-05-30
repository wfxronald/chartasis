import copy

def have_steps(row):
    steps = []
    for index in range(len(row)):
        step = row[index]
        if step != '0':
            steps.append((index+1, step))
    return steps

def det_mode(row):
    if len(row) == 5:
        return 'single'
    else:  # len(row) == 10
        return 'double'

def det_first_foot(mode, arrow):
    if mode == 'single':
        if arrow < 3:  # down left, up left
            return 'X'
        elif arrow > 3:  # down right, up right
            return 'Y'
        else:  # center arrow
            return 'Z'
    else:  # mode == 'double'
        if arrow <= 5:  # left pad
            return 'X'
        else:  # right pad
            return 'Y'
        # TODO: sometimes need to see future because not start at center

def opp_foot(foot):
    if foot == 'X':
        return 'Y'
    else:  # foot == 'Y'
        return 'X'

# Main function
def convert_to_lr(array_format):
    result = copy.deepcopy(array_format)
    prev_step = []

    for measure in result:
        for row in measure:
            if not have_steps(row):
                continue

            mode = det_mode(row)
            array_of_arrows = have_steps(row)

            if len(array_of_arrows) == 2:  # jumps
                left_arrow = array_of_arrows[0][0]
                left_type = array_of_arrows[0][1]
                right_arrow = array_of_arrows[1][0]
                right_type = array_of_arrows[1][1]
                if left_type == '1':
                    row[left_arrow-1] = 'X'
                elif left_type == '2':
                    row[left_arrow-1] = 'x'
                if right_type == '1':
                    row[right_arrow-1] = 'Y'
                elif right_type == '2':
                    row[right_arrow-1] = 'y'
                prev_step = [('X', left_arrow), ('Y', right_arrow)]
            elif len(array_of_arrows) > 2:
                pass
                # TODO: need to handle triples, brackets
            else:  # single arrow
                arrow = array_of_arrows[0][0]
                arrow_type = array_of_arrows[0][1]
                if not prev_step:
                    foot = det_first_foot(mode, arrow)
                    if arrow_type == '1':
                        row[arrow-1] = foot
                    elif arrow_type == '2':
                        row[arrow-1] = foot.lower()
                    prev_step = [(foot, arrow)]
                elif len(prev_step) == 1:
                    tup = prev_step[0]
                    prev_foot = tup[0]
                    prev_arrow = tup[1]

                    if prev_arrow == arrow:  # repeated tap
                        if arrow_type == '1':
                            row[arrow-1] = prev_foot
                        elif arrow_type == '2':
                            row[arrow-1] = prev_foot.lower()
                        # no change to prev_step: same foot, same arrow
                    else:  # change leg every time
                        if prev_foot != 'Z':
                            next_foot = opp_foot(prev_foot)
                        else:
                            # TODO: the previous foot must change too
                            next_foot = det_first_foot(mode, arrow)
                        if arrow_type == '1':
                            row[arrow-1] = next_foot
                        elif arrow_type == '2':
                            row[arrow-1] = next_foot.lower()
                        prev_step = [(next_foot, arrow)]
                else:
                    same_foot = False
                    for tup in prev_step:
                        if tup[1] == arrow:
                            same_foot = True
                            if arrow_type == '1':
                                row[arrow-1] = tup[0]
                            elif arrow_type == '2':
                                row[arrow-1] = tup[0].lower()
                            prev_step = [(tup[0], tup[1])]
                            break

                    if not same_foot:
                        foot = det_first_foot(mode, arrow)  # pretty much reset like beginning
                        if arrow_type == '1':
                            row[arrow-1] = foot
                        elif arrow_type == '2':
                            row[arrow-1] = foot.lower()
                        prev_step = [(foot, arrow)]

    return result
