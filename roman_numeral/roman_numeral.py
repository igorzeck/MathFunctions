# - Roman Numeral converter-
# Parser
def main():
    curr_str = ''
    while curr_str != 'q':
        curr_str = input(": ").upper()

        out = ''

        if curr_str.isdigit():
            out = curr_str
        else:
            out = roman_to_arab(curr_str)

        print(out)


# - Roman -> Arabian numeral
def roman_to_arab(curr_str):
    nums = ['I','V','X','L','C','D','M']

    # Remove non roman numerals
    clean_str = [c.upper() for c in curr_str if c.upper() in nums]
    print('Captured:', clean_str)

    # Variables
    result = 0
    last_mag = 999
    last_ind = -2
    captured = ''
    last_val = 0

    # Checks if there is repeated characters
    if any([ clean_str.count(u) > 3 for u in set(clean_str) ]):
        raise SystemError("Repeated numerals!")

    # Parses the string
    for c in clean_str:
        ind = nums.index(c)
        digit = 5 if ind % 2 else 1
        mag = ind // 2
        val = digit * 10 ** mag

        # If goes from higher rank to lower (w/o valid val) -> flag as bad expression
        try:
            if mag == last_mag or mag == last_mag + 1:
                ind_diff = last_ind - ind
                
                if (ind_diff == -1 and mag == last_mag) or (ind_diff == -2 and mag == last_mag + 1):
                    val = (val - 2 * last_val)
            elif mag > last_mag:
                print(mag, last_mag)
                raise SyntaxError("Invalid Roman number! Wrong magnitude.")
        except SyntaxError as e:
            print(e)
            return 0
        
        result += val
        last_ind = ind
        last_val = val
        last_mag = mag
        captured += c
    return result


if __name__ == '__main__':
    main()