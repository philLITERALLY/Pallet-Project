'''This module determines if a given column is a pass or fail'''

import handle_config    # module to handle config settings

def main(percent, side, col):
    flip = False
    reject = False

    calibPerc = getattr(handle_config, 'SIDE' + str(side) + '_COL' + col + '_PERC')
    
    currentPerc = round(calibPerc / percent * 100, 2)

    if col == 'A' or col == 'C':
        if currentPerc > handle_config.EDGE_REJECT_LEVEL:
            reject = True
        elif currentPerc > handle_config.EDGE_FLIP_LEVEL:
            flip = True
    else:
        if currentPerc > handle_config.MID_REJECT_LEVEL:
            reject = True

    return flip, reject, currentPerc