"insta - manish_aheibam"


import tkinter as tk
from tkinter import ttk, messagebox


class SubjectRow:
    """A single subject row: Subject name, Credit, Grade Point."""

    def __init__(self, parent, index, remove_callback):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="x", pady=2)

        ttk.Label(self.frame, text=f"{index}.", width=3).pack(side="left")

        self.name_var = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.name_var, width=18).pack(side="left", padx=3)

        self.credit_var = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.credit_var, width=8).pack(side="left", padx=3)

        self.grade_var = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.grade_var, width=8).pack(side="left", padx=3)

        self.remove_btn = ttk.Button(
            self.frame, text="✕", width=3, command=lambda: remove_callback(self)
        )
        self.remove_btn.pack(side="left", padx=3)

    def destroy(self):
        self.frame.destroy()

    def get_values(self):
        """Return (credit, grade_point) as floats, or raise ValueError."""
        credit = float(self.credit_var.get())
        grade = float(self.grade_var.get())
        return credit, grade


class SemesterRow:
    """A single semester row: Semester name, SGPA, Credits."""

    def __init__(self, parent, index, remove_callback):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="x", pady=2)

        ttk.Label(self.frame, text=f"{index}.", width=3).pack(side="left")

        self.name_var = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.name_var, width=18).pack(side="left", padx=3)

        self.sgpa_var = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.sgpa_var, width=8).pack(side="left", padx=3)

        self.credit_var = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.credit_var, width=8).pack(side="left", padx=3)

        self.remove_btn = ttk.Button(
            self.frame, text="✕", width=3, command=lambda: remove_callback(self)
        )
        self.remove_btn.pack(side="left", padx=3)

    def destroy(self):
        self.frame.destroy()

    def get_values(self):
        """Return (sgpa, credits) as floats, or raise ValueError."""
        sgpa = float(self.sgpa_var.get())
        credits = float(self.credit_var.get())
        return sgpa, credits


class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CGPA / SGPA Calculator")
        self.geometry("560x600")
        self.minsize(500, 480)

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        self.sgpa_rows = []
        self.cgpa_rows = []

        self._build_ui()


    def _build_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.sgpa_tab = ttk.Frame(notebook)
        self.cgpa_tab = ttk.Frame(notebook)

        notebook.add(self.sgpa_tab, text="SGPA (Single Semester)")
        notebook.add(self.cgpa_tab, text="CGPA (Multiple Semesters)")

        self._build_sgpa_tab()
        self._build_cgpa_tab()

    def _build_sgpa_tab(self):
        container = self.sgpa_tab

        ttk.Label(
            container,
            text="Enter each subject's credit hours and the grade point achieved.",
            wraplength=500,
            justify="left",
        ).pack(anchor="w", padx=10, pady=(10, 5))

        header = ttk.Frame(container)
        header.pack(fill="x", padx=10)
        ttk.Label(header, text="", width=3).pack(side="left")
        ttk.Label(header, text="Subject", width=18, font=("TkDefaultFont", 9, "bold")).pack(side="left", padx=3)
        ttk.Label(header, text="Credit", width=8, font=("TkDefaultFont", 9, "bold")).pack(side="left", padx=3)
        ttk.Label(header, text="Grade Pt", width=8, font=("TkDefaultFont", 9, "bold")).pack(side="left", padx=3)

        canvas_frame = ttk.Frame(container)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.sgpa_rows_frame = ttk.Frame(canvas_frame)
        self.sgpa_rows_frame.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_frame, text="+ Add Subject", command=self.add_sgpa_row).pack(side="left")
        ttk.Button(btn_frame, text="Calculate SGPA", command=self.calculate_sgpa).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_sgpa_rows).pack(side="left")

        self.sgpa_result_var = tk.StringVar(value="SGPA: —")
        ttk.Label(
            container,
            textvariable=self.sgpa_result_var,
            font=("TkDefaultFont", 13, "bold"),
            foreground="#1a6b3c",
        ).pack(pady=10)

        for _ in range(3):
            self.add_sgpa_row()

    def _build_cgpa_tab(self):
        container = self.cgpa_tab

        ttk.Label(
            container,
            text="Enter each semester's SGPA and the total credits for that semester.",
            wraplength=500,
            justify="left",
        ).pack(anchor="w", padx=10, pady=(10, 5))

        header = ttk.Frame(container)
        header.pack(fill="x", padx=10)
        ttk.Label(header, text="", width=3).pack(side="left")
        ttk.Label(header, text="Semester", width=18, font=("TkDefaultFont", 9, "bold")).pack(side="left", padx=3)
        ttk.Label(header, text="SGPA", width=8, font=("TkDefaultFont", 9, "bold")).pack(side="left", padx=3)
        ttk.Label(header, text="Credits", width=8, font=("TkDefaultFont", 9, "bold")).pack(side="left", padx=3)

        canvas_frame = ttk.Frame(container)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.cgpa_rows_frame = ttk.Frame(canvas_frame)
        self.cgpa_rows_frame.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_frame, text="+ Add Semester", command=self.add_cgpa_row).pack(side="left")
        ttk.Button(btn_frame, text="Calculate CGPA", command=self.calculate_cgpa).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_cgpa_rows).pack(side="left")

        self.cgpa_result_var = tk.StringVar(value="CGPA: —")
        ttk.Label(
            container,
            textvariable=self.cgpa_result_var,
            font=("TkDefaultFont", 13, "bold"),
            foreground="#1a3d6b",
        ).pack(pady=10)

        for _ in range(2):
            self.add_cgpa_row()


    def add_sgpa_row(self):
        index = len(self.sgpa_rows) + 1
        row = SubjectRow(self.sgpa_rows_frame, index, self.remove_sgpa_row)
        self.sgpa_rows.append(row)

    def remove_sgpa_row(self, row):
        if row in self.sgpa_rows:
            row.destroy()
            self.sgpa_rows.remove(row)
            self._renumber(self.sgpa_rows)

    def clear_sgpa_rows(self):
        for row in self.sgpa_rows:
            row.destroy()
        self.sgpa_rows = []
        self.sgpa_result_var.set("SGPA: —")

    def add_cgpa_row(self):
        index = len(self.cgpa_rows) + 1
        row = SemesterRow(self.cgpa_rows_frame, index, self.remove_cgpa_row)
        self.cgpa_rows.append(row)

    def remove_cgpa_row(self, row):
        if row in self.cgpa_rows:
            row.destroy()
            self.cgpa_rows.remove(row)
            self._renumber(self.cgpa_rows)

    def clear_cgpa_rows(self):
        for row in self.cgpa_rows:
            row.destroy()
        self.cgpa_rows = []
        self.cgpa_result_var.set("CGPA: —")

    @staticmethod
    def _renumber(rows):
        for i, row in enumerate(rows, start=1):
            children = row.frame.winfo_children()
            if children:
                children[0].config(text=f"{i}.")


    def calculate_sgpa(self):
        if not self.sgpa_rows:
            messagebox.showwarning("No subjects", "Please add at least one subject.")
            return

        total_credits = 0.0
        total_points = 0.0

        for i, row in enumerate(self.sgpa_rows, start=1):
            try:
                credit, grade = row.get_values()
            except ValueError:
                messagebox.showerror(
                    "Invalid input", f"Please enter valid numbers for subject row {i}."
                )
                return
            if credit < 0 or grade < 0 or grade > 10:
                messagebox.showerror(
                    "Invalid input",
                    f"Row {i}: credit must be ≥ 0 and grade point must be between 0 and 10.",
                )
                return
            total_credits += credit
            total_points += credit * grade

        if total_credits == 0:
            messagebox.showerror("Invalid input", "Total credits cannot be zero.")
            return

        sgpa = total_points / total_credits
        self.sgpa_result_var.set(f"SGPA: {sgpa:.2f}   (Total Credits: {total_credits:g})")

    def calculate_cgpa(self):
        if not self.cgpa_rows:
            messagebox.showwarning("No semesters", "Please add at least one semester.")
            return

        total_credits = 0.0
        total_points = 0.0

        for i, row in enumerate(self.cgpa_rows, start=1):
            try:
                sgpa, credits = row.get_values()
            except ValueError:
                messagebox.showerror(
                    "Invalid input", f"Please enter valid numbers for semester row {i}."
                )
                return
            if credits < 0 or sgpa < 0 or sgpa > 10:
                messagebox.showerror(
                    "Invalid input",
                    f"Row {i}: credits must be ≥ 0 and SGPA must be between 0 and 10.",
                )
                return
            total_credits += credits
            total_points += sgpa * credits

        if total_credits == 0:
            messagebox.showerror("Invalid input", "Total credits cannot be zero.")
            return

        cgpa = total_points / total_credits
        self.cgpa_result_var.set(f"CGPA: {cgpa:.2f}   (Total Credits: {total_credits:g})")


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()