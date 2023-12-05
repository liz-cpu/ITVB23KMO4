import tkinter as tk
from tkinter import ttk


class PercentageCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Percentage Calculator")

        style = ttk.Style()
        style.theme_use("clam")

        self.frame = ttk.Frame(root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.entry_x = ttk.Entry(self.frame, width=10, font=('Arial', 12))
        self.entry_x.grid(row=0, column=0, padx=10, pady=10)

        self.label_percent = ttk.Label(
            self.frame, text="%", font=('Arial', 12))
        self.label_percent.grid(row=0, column=1)

        self.entry_y = ttk.Entry(self.frame, width=10, font=('Arial', 12))
        self.entry_y.grid(row=0, column=2, padx=10, pady=10)

        self.operation_var = tk.StringVar()
        self.operation_var.set("Percentage of")

        self.operation_menu = ttk.Combobox(self.frame, values=["Percentage of", "Percent of Total", "Percentage Change"],
                                           textvariable=self.operation_var, font=('Arial', 12))
        self.operation_menu.grid(row=1, column=0, columnspan=3, pady=10)
        self.operation_menu.config(state="readonly")

        self.calculate_button = ttk.Button(self.frame, text="Calculate", command=self.calculate_percentage,
                                           style="TButton", cursor="hand2")
        self.calculate_button.grid(row=2, column=0, columnspan=3, pady=15)

        self.result_label = ttk.Label(self.frame, text="", font=('Arial', 14))
        self.result_label.grid(row=3, column=0, columnspan=3)

    def calculate_percentage(self):
        try:
            x = float(self.entry_x.get())
            y = float(self.entry_y.get())

            self.result_label.config(text="")

            if self.operation_var.get() == "Percentage of":
                result = (x / 100) * y
                self.result_label.config(text=f"{x}% of {y} is {result:.2f}")

            elif self.operation_var.get() == "Percent of Total":
                result = (x / y) * 100
                self.result_label.config(text=f"{x} is {result:.2f}% of {y}")

            elif self.operation_var.get() == "Percentage Change":
                change = y - x
                percentage_change = (change / abs(x)) * 100

                if change > 0:
                    self.result_label.config(
                        text=f"The percentage increase from {x} to {y} is {percentage_change:.2f}%")
                elif change < 0:
                    self.result_label.config(
                        text=f"The percentage decrease from {x} to {y} is {percentage_change:.2f}%")
                else:
                    self.result_label.config(
                        text="There is no percentage change.")

        except ValueError:
            self.result_label.config(
                text="Please enter valid numerical values.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PercentageCalculator(root)
    root.mainloop()
