import time
import win32api
import argparse
from ctypes import windll


debug = True
USER32 = windll.user32
mouse_move_timeout = 10


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


def detect_by_click_location():
    """
    Cuckoo always clicks on the same spot in the screen
    Accumulate 10 clicking events
    :return: True iff all events are in Cuckoo's "favorite spot"
    """
    click_locations = []

    # center of the screen in the x axis
    x_center = USER32.GetSystemMetrics(0) / 2
    was_clicked = False

    # collect 5 clicking samples
    while True:
        lmb_state = win32api.GetKeyState(0x01)

        # button pressed
        if lmb_state < 0:
            was_clicked = True

        # button released
        elif lmb_state >= 0 and was_clicked:
            x, y = win32api.GetCursorPos()
            click_locations.append({"x": x, "y": y})
            was_clicked = False

        time.sleep(0.001)

        if len(click_locations) == 5:
            for click_location in click_locations:
                # verify all clicks are in the same position, hardcoded in cuckoo
                if not(click_location["x"] == x_center and click_location["y"] == 0):
                    return False
            return True


def detect_by_clicking_speed():
    """
    Cuckoo clicks the left mouse button for exactly 50 milliseconds
    Sample 10 clicking events and calculate its average value
    :return: return True iff all are equal to cuckoo's hardcoded value +- 1 millisecond
    """
    click_times = []
    was_clicked = False

    # collect 10 clicking samples
    while True:
        lmb_state = win32api.GetKeyState(0x01)

        # button pressed
        if lmb_state < 0:
            was_clicked = True
            start_time = time.time()

        # button released
        elif lmb_state >= 0 and was_clicked:
            elapsed_time = time.time() - start_time
            click_times.append(elapsed_time)
            was_clicked = False

        time.sleep(0.001)

        if len(click_times) == 10:
            avg_click_duration = sum(click_times) / len(click_times)
            if 0.0048 < avg_click_duration < 0.0052:
                return True
            else:
                return False


def max_mouse_speed(sampling_time):
    """
    This function returns the maximal derivative in a given sampling interval.
    Note that we treat the abstract value of the

    :param sampling_time: how much time to spend before returning the fastest mouse jump
    :return: True iff the fastest movement is slower than super_mover_threshold
    """

    # based on some tests these are the optimal values
    super_mover_threshold = 50

    max_deriv = 0
    timeout = time.time() + sampling_time

    while True:
        dx, dy = calc_delta(0.01)
        if dy == 0:
            pass
        else:
            if debug:
                print "dx:{0} dy:{1} abs(dx/dy):{2} max:{3}".format(str(dx), str(dy), str(abs(dx / dy)),str(max_deriv))
            else:
                pass

            abs_deriv = abs(dx/dy)
            if abs_deriv > max_deriv:
                max_deriv = abs_deriv

        # do this for one minute
        if time.time() > timeout:
            break

    print "fastest change was:" + str(max_deriv)

    # if maximal derivative was higher than our threshold declare it is a sandbox
    if max_deriv > super_mover_threshold:
        return True
    else:
        return False


def mean_mouse_speed(sampling_time):
    """
    This function returns the average derivative in a given sampling interval.
    Note that we treat the abstract value of the
    :param sampling_time: how much time to spend before returning the fastest mouse jump
    :return: True iff the mean of cursor movements is high
    """

    movement_speeds = []
    timeout = time.time() + sampling_time
    mean_threshold = 20

    while True:
        dx, dy = calc_delta(0.01)
        if dy == 0:
            # no vertical movement, we'll also get INF
            pass
        else:
            abs_deriv = abs(dx/dy)
            movement_speeds.append(abs_deriv)

        # do this for one minute
        if time.time() > timeout:
            break
    mean = sum(movement_speeds)/(max(1,len(movement_speeds)))

    print "avg was:{0}".format(str(mean))

    if mean > mean_threshold:
        return True
    else:
        return False


if __name__ == '__main__':
    # mean was mor effective, you can try max as well
    parser = argparse.ArgumentParser(description='Detect sandbox by mouse movement')
    parser.add_argument('-mean', action='store_true')
    parser.add_argument('-max', action='store_true')
    parser.add_argument('-timing', action='store_true')
    parser.add_argument('-location', action='store_true')

    args = parser.parse_args()

    if args.max:
        if max_mouse_speed(mouse_move_timeout):
            print "Castles made of sand"
        else:
            "Let the games begin"

    elif args.mean:
        if mean_mouse_speed(mouse_move_timeout):
            print "This is a box of sand"
        else:
            "gogogo"

    elif args.timing:
        if detect_by_clicking_speed():
            print "Hello Cuckoo"
        else:
            print "You are clear to proceed"

    elif args.location:
        if detect_by_click_location():
            print "Hoot hoot"
        else:
            print "Bring it on!"

    else:
        print "Usage:\n\tpython SmoothCriminal.py <-mean|-max|-timing|-location>"
