import time
import win32api
import argparse

__author__ = 'Gal_B1t'

debug = False


def calc_delta(sampling_interval):
    """
    This function calculates the change in x and y coordinates in a given time interval

    :param sampling_interval: how fast should we sample the movement of the cursor?
    :return: x and y coordinates delta
    """
    x1, y1 = win32api.GetCursorPos()
    time.sleep(sampling_interval)
    x2, y2 = win32api.GetCursorPos()
    return x2 - x1, y2 - y1


def max_mouse_speed(sampling_time):
    """
    This function returns the maximal derivative in a given sampling interval.
    Note that we treat the abstract value of the

    :param sampling_time: how much time to spend before returning the fastest mouse jump
    :return:
    """
    max_deriv = 0
    timeout = time.time() + sampling_time

    while True:
        dx, dy = calc_delta(0.01)
        if dy == 0:
            pass
        else:
            if debug:
                print "dx:{0} dy:{1} abs(dx/dy):{2} max:{3}".format(str(dx), str(dy), str(abs(dx / dy)), str(max_deriv))
            else:
                pass

            abs_deriv = abs(dx / dy)
            if abs_deriv > max_deriv:
                max_deriv = abs_deriv

        # do this for one minute
        if time.time() > timeout:
            break

    return max_deriv


def mean_mouse_speed(sampling_time):
    """
    This function returns the average derivative in a given sampling interval.
    Note that we treat the abstract value of the

    :param sampling_time: how much time to spend before returning the fastest mouse jump
    :return: the mean of cursor movements - cuckoo's jumps will be high
    """

    movement_speeds = []
    timeout = time.time() + sampling_time

    while True:
        dx, dy = calc_delta(0.01)
        if dy == 0:
            # no vertical movement, we'll also get INF
            pass
        else:
            abs_deriv = abs(dx / dy)
            movement_speeds.append(abs_deriv)

        # do this for one minute
        if time.time() > timeout:
            break
    mean = sum(movement_speeds) / (max(1, len(movement_speeds)))
    return mean


if __name__ == '__main__':

    # mean was mor effective, you can try max as well
    parser = argparse.ArgumentParser(description='Detect sandbox by mouse movement')
    parser.add_argument('-mean', action='store_true')
    parser.add_argument('-max', action='store_true')

    args = parser.parse_args()

    if args.max:
        # based on some tests these are the optimal values
        super_mover_threshold = 50
        fastest_mouse_move = max_mouse_speed(10)

        print "fastest change was:" + str(fastest_mouse_move)

        # if maximal derivative was higher than our threshold declare it is a sandbox
        if fastest_mouse_move > super_mover_threshold:
            # we are in a sandbox
            print "Castles made of sand"
        else:
            # do bad stuff, we are clear
            "Let the games begin"

    elif args.mean:
        avg = mean_mouse_speed(10)
        print "avg was:{0}".format(str(avg))

        if avg > 20:
            print "This is a box of sand"
        else:
            "gogogo"
    else:
        print "please provide either -mean or -max flags"
