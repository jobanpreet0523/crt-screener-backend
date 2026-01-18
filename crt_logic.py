def grade_setup(rr, htf_bias, liquidity):
    if rr >= 3 and htf_bias and liquidity:
        return "A+"
    if rr >= 2:
        return "A"
    if rr >= 1.5:
        return "B"
    return "C"
