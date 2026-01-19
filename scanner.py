def is_doji(o, h, l, c):
    body = abs(c - o)
    range_ = h - l
    if range_ == 0:
        return False
    return body <= (range_ * 0.1)
