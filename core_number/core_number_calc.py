# - Core number calculator -

def main():
    num_str = '1312'
    # - Checks if number is only digits -
    if not num_str.isdigit():
        print("Not only digits!")
        exit(0)

    # - Checks if core number is 4 digits -
    if len(num_str) < 4:
        print("Not long enoguh (less than 4 digits)!")
        exit(0)

    # - Group number list -
    core_number = -1
    best_order = []
    best_group = []
    curr_str = num_str

    while len(curr_str) > 3:
        for group in group_digits(curr_str, False):
            group_unified = [''.join(in_group) for in_group in group]
            # '0X' shouldn't count, but 'X0' should!
            invalid = False
            for group_str in group_unified:
                if len(group_str) > 1:
                    # So single zeros aren't flaggeds
                    if len(group_str.lstrip('0')) < len(group_str):
                        invalid = True
                        print(group_unified, 'invalid!')
            if invalid:
                continue
            numeric_group = list(map(float, group_unified))
            ops_ords, low_value = compute_core(numeric_group)

            if (low_value < core_number or core_number < 0) and low_value >= 0:
                core_number = low_value
                best_order = ops_ords
                best_group = group
        print(core_number)
        curr_str = str(int(core_number))

    if core_number < 0:
        print("Core number not found!")
    else:
        full_str = ''.join(list(map(str.__add__, best_order, best_group)))
        print("Lowest:", full_str + '=' + str(int(core_number)))

def group_digits(digits: list[str], verbose = False):
    # - Generator for number list -
    # Put 1 number at a time into a basket
    # ix is the start of the next index
    for i1 in range(1, len(digits) - 2):
        if verbose:
            print(i1,'->', digits[i1])
        for i2 in range(i1 + 1, len(digits) - 1):
            if verbose:
                print(i2,'->', digits[i2])
            for i3 in range(i2 + 1, len(digits)):
                if verbose:
                    print(i3,'->', digits[i3])
                yield digits[0:i1], digits[i1:i2], digits[i2:i3], digits[i3:]


def compute_core(nums: list[float], verbose = True):
    ops = {'+':float.__add__, '*':float.__mul__, '/':float.__truediv__, '-':float.__sub__}
    sortable_ops = ['*', '/', '-']
    # For now, by hand
    # Find lowest less than 4 digits numver
    low_order = ['+','*','-','/']
    lowest_val = -9999
    for _ops in permute_list(sortable_ops):
        ops_ordered = ['+'] + _ops

        if verbose:
            print(ops_ordered)
        
        num_id = 0
        curr_val = 0.0
        for op_ord in ops_ordered:
            # It will never be below zero, but alas...
            if not (op_ord == '/' and nums[num_id] <= 0):
                _op_func = ops[op_ord]
                curr_val = _op_func(curr_val,nums[num_id])
            else:
                curr_val = -1
                break
            num_id += 1
        if (curr_val < lowest_val or lowest_val < 0) and (curr_val > 0) and (curr_val.is_integer()):
            lowest_val = curr_val
            low_order = ops_ordered
    
    if verbose:
        print(low_order)
        print(nums)
        print("Operations:", low_order)
        print("Core:", lowest_val)
    
    return low_order, lowest_val


def permute_list(l: list):
    for order in permute_order(len(l), [], []):
        yield [l[o] for o in order]


def permute_order(n, order: list[int], all_order: list, level: int = 0):
    old_order = order
    if level < n:
        for i in range(n):
            order = old_order
            if i not in order:
                order = permute_order(n, order + [i], all_order, level + 1)
    elif level == n:
        all_order.append(order)

    if level == 0:
        return all_order
    else:
        return order


if __name__ == '__main__':
    main()
    print("MMCCXIII: ", compute_core([1000,200,11,2], False))