import tkinter as tk


class thing(tk.Canvas):
    def __init__(self, random_frame):
        tk.Canvas.__init__(self, random_frame, width=100, height=100)

        draw_line(3)

        foo = 2
        do_something()
        lambda: do_something()

        def draw_line(x: int):
            self.create_line(x, 0, x, 50, fill="black", width=10)

        def do_something():
            foo = foo + 2


class c2:
    def __init__(self) -> None:
        bar = 5
        add_2(bar)

        def add_2(foo):
            foo = foo + 2
            print(foo)
