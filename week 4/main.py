from tkinter import Canvas, StringVar, Tk, BOTH, Event
from tkinter.ttk import Frame, Label, LabelFrame, Button, Combobox, Style

import model as mo
import config as cf

# Global variable to track whether the grid needs to be redrawn on start
START_FLAG = True


class MainApp(Frame):
    """
    GUI
    """

    def __init__(self, root: Tk) -> None:
        """
        Initialize the MainApp.

        Parameters:
            root (Tk): The root window.
        """
        Frame.__init__(self, root)
        self.root: Tk = root
        self.delay: StringVar = StringVar()
        self.make_grid_panel()
        self.make_control_panel()
        self.re_plot()

    def pause(self) -> None:
        """
        Pause the execution for a given delay in milliseconds.
        """
        self.root.after(int(self.delay.get()) * cf.DELAY)
        self.root.update_idletasks()

    def make_grid_panel(self) -> None:
        """
        Initialize the grid frame and canvas.
        """
        left_frame: Frame = Frame(self.root)
        left_frame.grid(column=0, row=0, padx=12, pady=12)
        self.canvas: Canvas = Canvas(left_frame, height=cf.H+4*cf.TR,
                                     width=cf.W+4*cf.TR, borderwidth=-cf.TR, bg=cf.BG_C)
        self.canvas.pack(fill=BOTH, expand=True)

    def make_grid(self) -> None:
        """
        Draw the grid lines on the canvas.
        """
        for i in range(0, cf.W+1, cf.CELL):
            self.canvas.create_line(
                i+cf.TR, 0+cf.TR, i+cf.TR, cf.H+cf.TR, fill=cf.GRID_C)
        for i in range(0, cf.H+1, cf.CELL):
            self.canvas.create_line(
                0+cf.TR, i+cf.TR, cf.W+cf.TR, i+cf.TR, fill=cf.GRID_C)

    def plot_line_segment(self, x0: int, y0: int, x1: int, y1: int, color: str) -> None:
        """
        Plot a line segment on the canvas.

        Parameters:
            x0, y0, x1, y1 (int): Coordinates of the line segment.
            color (str): Color of the line.
        """
        self.canvas.create_line(x0*cf.CELL+cf.TR, y0*cf.CELL+cf.TR,
                                x1*cf.CELL+cf.TR, y1*cf.CELL+cf.TR, fill=color, width=2)

    def plot_node(self, node: tuple[int, int], color: str) -> None:
        """
        Plot a node on the canvas.

        Parameters:
            node (tuple): Coordinates of the node.
            color (str): Color of the node.
        """
        x0: float = node[0]*cf.CELL - (cf.BLOCK_SIZE/2)
        y0: float = node[1]*cf.CELL - (cf.BLOCK_SIZE/2)
        x1: float = x0 + cf.BLOCK_SIZE + 1
        y1: float = y0 + cf.BLOCK_SIZE + 1
        self.canvas.create_rectangle(
            x0+cf.TR, y0+cf.TR, x1+cf.TR, y1+cf.TR, fill=color)

    def make_control_panel(self) -> None:
        """
        Create the control panel with buttons and widgets.
        """
        right_frame: Frame = Frame(self.root)
        right_frame.grid(column=1, row=0, padx=12, pady=12)

        lf1: LabelFrame = LabelFrame(right_frame)
        lf1.grid(column=0, row=0, padx=8, pady=4)
        lf1.grid_rowconfigure(2, minsize=10)

        def start() -> None:
            """
            Start the main program and move the robot.
            """
            global START_FLAG

            if not START_FLAG:
                self.re_plot()

            START_FLAG = False
            mo.move_robot(self, cf.START_POS)

        start_button: Button = Button(
            lf1, text="Start", command=start, width=10)
        start_button.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        def box_update1(event: Event) -> None:
            """
            Update the delay value when the combobox selection changes.
            """
            print('delay is set to:', box1.get())

        lf2: LabelFrame = LabelFrame(right_frame, relief="sunken")
        lf2.grid(column=0, row=1, padx=5, pady=5)

        Label(lf2, text="Delay").grid(column=1, row=1, sticky='w')
        box1: Combobox = Combobox(
            lf2, textvariable=self.delay, state='readonly', width=6)
        box1.grid(column=1, row=2, sticky='w')
        box1['values'] = tuple(str(i) for i in range(5))
        box1.current(1)
        box1.bind("<<ComboboxSelected>>", box_update1)

    def re_plot(self) -> None:
        """
        Redraw the grid and nodes on the canvas.
        """
        self.canvas.delete("all")
        self.make_grid()
        self.plot_node(cf.START_POS, color=cf.START_C)


# Create and start GUI
root: Tk = Tk()
root.title('Mars robot')

# Set the theme
style: Style = Style(root)
style.theme_use('clam')

app: MainApp = MainApp(root)
root.mainloop()
