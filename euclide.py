def euclide(a, b):
    if a > b:
        a, b = b, a
    while b != 0:
        a,b = b,b%a
    return a

def euclide_rec(a, b):
    if a > b:
        a, b = b, a
    if b != 0:
        a, b = b, b%a
        return euclide(a, b)
    return a

euclide_line = lambda a, b: (
    (((c := a, a := b, b:= c) if a > b else 0),
        (euclide_line_sub := lambda a, b: (
            (r := b%a, a := b, b := r), 
            a if b == 0 else euclide_line_sub(a, b)
        )[1])(a, b)
    )[1]
)
for a in range(1, 100):
    for b in range(1, 100):
        print(f"{a=} {b=} {(e_l := euclide_line(a, b))} {(e_f := euclide(a, b))}")
        if e_l != e_f:
            break



euclide_line = lambda a, b: ((((c := a, a := b, b:= c) if a > b else 0),(euclide_line_sub := lambda a, b: ((r := b%a, a := b, b := r), a if b == 0 else euclide_line_sub(a, b))[1])(a, b))[1])