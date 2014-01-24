import bisect


class PossibleValue(object):
    def __init__(self, value, function_to_check, func_args, func_kwargs):
        self.function_to_check = function_to_check
        self.func_args = func_args
        self.func_kwargs = func_kwargs
        self.value = value

    def __cmp__(self, other):
        if self.function_to_check(self.value, *self.func_args, **self.func_kwargs):
            return -1
        return 1


class FakeList(object):
    def __init__(self, function_to_check, func_args, func_kwargs):
        self.function_to_check = function_to_check
        self.func_args = func_args
        self.func_kwargs = func_kwargs

    def __getitem__(self, index):
        return PossibleValue(index, self.function_to_check, self.func_args, self.func_kwargs)


def find_value_range_to_check(function_to_check, start, scale_factor, func_args, func_kwargs):
    max_value_to_check = start
    min_value_to_check = 0

    while function_to_check(max_value_to_check, *func_args, **func_kwargs):
        # Since this passed, we can set a new minimum value above this
        min_value_to_check = max_value_to_check + 1
        # Keep doubling max_value_to_check until we find something too high
        max_value_to_check *= scale_factor
    return max_value_to_check, min_value_to_check


def guess(function_to_check, *func_args, **func_kwargs):
    start = func_kwargs.pop('start', 10)
    scale_factor = func_kwargs.pop('scale_factor', 2)

    max_value_to_check, min_value_to_check = find_value_range_to_check(
        function_to_check,
        start,
        scale_factor,
        func_args,
        func_kwargs,
    )

    fake_list = FakeList(function_to_check, func_args, func_kwargs)
    leftmost_value_greater_than = bisect.bisect_right(
        fake_list,
        "this value doesn't matter",
        lo=min_value_to_check,
        hi=max_value_to_check,
    )
    return leftmost_value_greater_than - 1
