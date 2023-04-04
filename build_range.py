def build_range(start, stop):
    result = []
    while start < stop:
        result.append(start)
        start += 1
    return result


def build_range_step(start, stop, step):
    result = []
    while start < stop:
        result.append(start)
        start += step
    return result


start, stop, step = -10, 20, 2
print(build_range_step(start, stop, step))
