import tkinter as tk
from tkinter import ttk
from typing import List, Tuple
import model as mo
import config as cf

# global var
START_FLAG = True  # do not redraw grid when pressing start the first time


class MainApp(tk.Frame):
    """
    Main application class for the pathfinding visualization.
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the MainApp.

        Parameters:
        - root (tk.Tk): The root window.

        Returns:
        - None
        """
        tk.Frame.__init__(self)
        self.root = root
        self.alg = tk.StringVar()
        self.delay = tk.StringVar()
        self.prob = tk.StringVar()
        self.make_grid_panel()
        self.make_control_panel()
        self.re_plot()

    def pause(self) -> None:
        """
        Pause the application for a specified delay.

        Returns:
        - None
        """
        self.root.after(int(self.delay.get()) * 25)  # pause in msec
        self.root.update_idletasks()  # redraw widgets

    def make_grid_panel(self) -> None:
        """
        Create and initialize the grid frame.

        Returns:
        - None
        """
        left_frame = tk.Frame(self.root)
        left_frame.grid(column=0, row=0, padx=3, pady=12)
        self.canvas = tk.Canvas(left_frame, height=cf.H+4*cf.TR,
                                width=cf.W+4*cf.TR, borderwidth=-cf.TR, bg=cf.BG_C)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def make_grid(self) -> None:
        """
        Draw the grid lines on the canvas.

        Returns:
        - None
        """
        # vertical lines
        for i in range(0, cf.W+1, cf.CELL):
            self.canvas.create_line(
                i+cf.TR, 0+cf.TR, i+cf.TR, cf.H+cf.TR, fill=cf.GRID_C)
        # horizontal lines
        for i in range(0, cf.H+1, cf.CELL):
            self.canvas.create_line(
                0+cf.TR, i+cf.TR, cf.W+cf.TR, i+cf.TR, fill=cf.GRID_C)

    def init_grid(self) -> None:
        """
        Initialize the grid with random blocked nodes.

        Returns:
        - None
        """
        for x in range(cf.SIZE):
            for y in range(cf.SIZE):
                node = (x, y)
                if mo.bernoulli_trial(self):
                    mo.set_grid_value(node, 'b')  # set as blocked
                    self.plot_node(node, color=cf.BLOCK_C)
                else:
                    mo.set_grid_value(node, -1)

        mo.set_grid_value(cf.START, 0)
        mo.set_grid_value(cf.GOAL, -1)

    def plot_line_segment(self, x0: int, y0: int, x1: int, y1: int, color: str) -> None:
        """
        Draw a line segment on the canvas.

        Parameters:
        - x0, y0, x1, y1 (int): Coordinates of the line segment.
        - color (str): Color of the line.

        Returns:
        - None
        """
        self.canvas.create_line(x0*cf.CELL+cf.TR, y0*cf.CELL+cf.TR,
                                x1*cf.CELL+cf.TR, y1*cf.CELL+cf.TR, fill=color, width=2)

    def plot_node(self, node: Tuple[int, int], color: str) -> None:
        """
        Draw a node on the canvas.

        Parameters:
        - node (Tuple[int, int]): Coordinates of the node.
        - color (str): Color of the node.

        Returns:
        - None
        """
        x0 = node[0]*cf.CELL - 4
        y0 = node[1]*cf.CELL - 4
        x1 = x0 + 8 + 1
        y1 = y0 + 8 + 1
        self.canvas.create_rectangle(
            x0+cf.TR, y0+cf.TR, x1+cf.TR, y1+cf.TR, fill=color)

    def make_control_panel(self) -> None:
        """
        Create the control panel containing start button, algorithm selection, delay, and probability inputs.

        Returns:
        - None
        """
        right_frame = tk.Frame(self.root)
        right_frame.grid(column=1, row=0, padx=3, pady=12)
        lf1 = tk.LabelFrame(right_frame)
        lf1.grid(column=0, row=0, padx=8, pady=4)
        lf1.grid_rowconfigure(2, minsize=10)

        def start_search() -> None:
            """
            Start the pathfinding search.

            Returns:
            - None
            """
            global START_FLAG
            if not START_FLAG:
                self.re_plot()
            START_FLAG = False
            mo.search(self, cf.START, cf.GOAL)

        start_button = tk.Button(
            lf1, text="Start", command=start_search, width=10)
        start_button.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        def select_alg() -> None:
            """
            Print the selected algorithm.

            Returns:
            - None
            """
            print('algorithm =', self.alg.get())

        r1_button = tk.Radiobutton(
            lf1, text='UC', variable=self.alg, value='UC', command=select_alg)
        r1_button.grid(column=1, row=3, columnspan=2, sticky='w')
        r2_button = tk.Radiobutton(
            lf1, text='A*', variable=self.alg, value='A*', command=select_alg)
        r2_button.grid(column=1, row=4, columnspan=2, sticky='w')
        self.alg.set('UC')

        def box_update1(event: tk.Event) -> None:
            """
            Print the selected delay.

            Returns:
            - None
            """
            print('delay is set to:', box1.get())

        def box_update2(event: tk.Event) -> None:
            """
            Print the selected blocking probability.

            Returns:
            - None
            """
            print('prob. blocking is set to:', box2.get())

        lf2 = tk.LabelFrame(right_frame, relief="sunken")
        lf2.grid(column=0, row=1, padx=5, pady=5)
        tk.Label(lf2, text="Delay").grid(column=1, row=1, sticky='w')
        box1 = ttk.Combobox(lf2, textvariable=self.delay,
                            state='readonly', width=6)
        box1.grid(column=1, row=2, sticky='w')
        box1['values'] = tuple(str(i) for i in range(5))
        box1.current(1)
        box1.bind("<<ComboboxSelected>>", box_update1)

        tk.Label(lf2, text="Prob. blocking").grid(column=1, row=3, sticky='w')
        box2 = ttk.Combobox(lf2, textvariable=self.prob,
                            state='readonly', width=6)
        box2.grid(column=1, row=4, sticky='ew')
        box2['values'] = tuple(str(i) for i in range(5))
        box2.current(2)
        box2.bind("<<ComboboxSelected>>", box_update2)

    def re_plot(self) -> None:
        """
        Repaint the grid and nodes on the canvas.

        Returns:
        - None
        """
        self.canvas.delete("all")
        self.make_grid()
        self.init_grid()
        self.plot_node(cf.START, color=cf.START_C)
        self.plot_node(cf.GOAL, color=cf.GOAL_C)

    def draw_path(self, path: List[Tuple[int, int]]) -> None:
        """
        Draw the path on the canvas.

        Parameters:
        - path (List[Tuple[int, int]]): List of coordinates representing the path.

        Returns:
        - None
        """
        current = cf.GOAL
        while current != cf.START:
            prev = path[current]
            self.plot_line_segment(
                prev[0], prev[1], current[0], current[1], color=cf.FINAL_C)
            current = prev


# create and start GUI
root = tk.Tk()
root.title('A* demo')

app = MainApp(root)
root.mainloop()
