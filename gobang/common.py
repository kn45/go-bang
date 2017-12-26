def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0


def max_abs(vals):
    if len(vals) < 1:
        raise ValueError('max_abs() arg is an empty sequence')
    ret = vals[0]
    mabs = abs(vals[0])
    for val in vals:
        if abs(val) > mabs:
            ret = val
            mabs = abs(val)
    return ret


if __name__ == '__main__':
    print sign(4)
    print sign(0)
    print sign(-4)
    print max_abs([-5, 6])
    print max_abs([-5, 3])
