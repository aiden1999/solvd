# generate_lookup_tables.py
def generate_butterfly_table():
    table = {}
    for r in range(12):
        for c in range(12):
            table[(r, c)] = (c // 3) + ((r // 3) * 4)
    return table


def generate_cross_table():
    table = {}
    for r in range(21):
        for c in range(21):
            r3 = r // 3
            if r3 <= 1:
                table[(r, c)] = (c - 6) // 3 + r3 * 3
            elif r3 <= 4:
                table[(r, c)] = c // 3 + (7 * r3) - 8
            else:
                table[(r, c)] = (c - 6) // 3 + (r3 * 3) + 12
    return table


def generate_flower_table():
    table = {}
    for r in range(15):
        for c in range(15):
            if r <= 2:
                table[(r, c)] = (c - 3) // 3
            elif r <= 11:
                table[(r, c)] = (c // 3) + ((r // 3) * 5) - 2
            else:
                table[(r, c)] = ((c - 3) // 3) + 18
    return table


def generate_gattai_table():
    table = {}
    for row in range(15):
        for col in range(15):
            if row <= 2:
                table[(row, col)] = (col - 3) // 3
            elif row <= 5:
                table[(row, col)] = ((col - 3) // 3) + 3
            elif row <= 11:
                table[(row, col)] = ((col // 3) + 7) + (((row - 6) // 3) * 5)
            else:
                table[(row, col)] = (col // 3) + 17
    return table


def generate_kazaguruma_table():
    table = {}
    for row in range(21):
        for col in range(21):
            if row <= 2:
                table[(row, col)] = (col - 3) // 3
            elif row <= 5:
                table[(row, col)] = (col // 3) + 2
            elif row <= 8:
                table[(row, col)] = (col // 3) + 8
            elif row <= 11:
                table[(row, col)] = (col // 3) + 15
            elif row <= 14:
                table[(row, col)] = (col // 3) + 22
            elif row <= 17:
                table[(row, col)] = (col // 3) + 28
            else:
                table[(row, col)] = (col // 3) + 31
    return table


def generate_samurai_table():
    table = {}
    for row in range(21):
        for col in range(21):
            if row <= 2:
                if col <= 11:
                    table[(row, col)] = col // 3
                else:
                    table[(row, col)] = (col // 3) - 1
            elif row <= 5:
                if col <= 11:
                    table[(row, col)] = (col // 3) + 6
                else:
                    table[(row, col)] = (col // 3) + 5
            elif row <= 8:
                table[(row, col)] = (col // 3) + 12
            elif row <= 11:
                table[(row, col)] = (col // 3) + 17
            elif row <= 14:
                table[(row, col)] = (col // 3) + 22
            elif row <= 17:
                if col <= 11:
                    table[(row, col)] = (col // 3) + 29
                else:
                    table[(row, col)] = (col // 3) + 28
            else:
                if col <= 11:
                    table[(row, col)] = (col // 3) + 35
                else:
                    table[(row, col)] = (col // 3) + 34
    return table


def generate_sohei_table():
    table = {}
    for row in range(21):
        for col in range(21):
            if row <= 2:
                table[(row, col)] = (col // 3) - 2
            elif row <= 5:
                table[(row, col)] = (col // 3) + 1
            elif row <= 8:
                table[(row, col)] = (col // 3) + 6
            elif row <= 11:
                if col <= 11:
                    table[(row, col)] = (col // 3) + 13
                else:
                    table[(row, col)] = (col // 3) + 12
            elif row <= 14:
                table[(row, col)] = (col // 3) + 19
            elif row <= 17:
                table[(row, col)] = (col // 3) + 24
            else:
                table[(row, col)] = (col // 3) + 27
    return table


def write_lookup_file():
    thing = generate_sohei_table()
    with open("box_lookup_tables.py", "a") as f:
        f.write("SOHEI_LOOKUP = {\n")
        for key, value in thing.items():
            f.write(f"    {key}: {value},\n")
        f.write("}\n")


write_lookup_file()

