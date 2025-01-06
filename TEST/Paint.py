import tkinter as tk
from tkinter import colorchooser, messagebox
import matplotlib.pyplot as plt
import numpy as np

class Paint:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint Application")
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack()

        self.points = []
        self.current_color = "black"
        self.last_point = None

        self.canvas.bind("<Button-1>", self.draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)
        self.canvas.bind("<Button-3>", self.right_click)

    def draw(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        if self.last_point:
            self.canvas.create_line(self.last_point[0], self.last_point[1], x, y, fill=self.current_color)
        self.last_point = (x, y)

    def end_draw(self, event):
        self.last_point = None

    def right_click(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Change Color", command=self.change_color)
        menu.add_command(label="Clear", command=self.clear_canvas)
        menu.add_command(label="Convert to Parametric Curve", command=self.convert_to_parametric_curve)
        menu.post(event.x_root, event.y_root)

    def change_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.current_color = color

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points = []
        self.last_point = None

    def convert_to_parametric_curve(self):
        if not self.points:
            messagebox.showinfo("Info", "No points to convert.")
            return

        degree = 6  # You can adjust this value for the degree of the polynomial
        converter = Convertisseur(self.points, degree)
        converter.plot_curves()
        converter.print_equations()

class Convertisseur:
    def __init__(self, points, degree):
        self.points = points
        self.degree = degree
        self.x_coords, self.y_coords = zip(*self.points)
        self.x_coords = np.array(self.x_coords)
        self.y_coords = np.array(self.y_coords)

        # Normalize the parameter t
        self.t = np.linspace(0, 1, len(self.points))

        # Fit polynomials to x(t) and y(t)
        self.x_poly_coeffs = np.polyfit(self.t, self.x_coords, self.degree)
        self.y_poly_coeffs = np.polyfit(self.t, self.y_coords, self.degree)
        self.x_poly = np.poly1d(self.x_poly_coeffs)
        self.y_poly = np.poly1d(self.y_poly_coeffs)

        # Calculate the first and second derivatives
        self.x_poly_deriv = self.x_poly.deriv()
        self.y_poly_deriv = self.y_poly.deriv()
        self.x_poly_deriv2 = self.x_poly_deriv.deriv()
        self.y_poly_deriv2 = self.y_poly_deriv.deriv()

    def plot_curves(self):
        t_fine = np.linspace(0, 1, 1000)
        x_fine = self.x_poly(t_fine)
        y_fine = self.y_poly(t_fine)
        dy_fine = self.y_poly_deriv(t_fine)
        d2y_fine = self.y_poly_deriv2(t_fine)

        plt.figure(figsize=(12, 8))

        # Plot the original curve
        plt.subplot(3, 1, 1)
        plt.plot(x_fine, y_fine, label='Parametric Curve')
        plt.title("Parametric Curve")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()

        # Plot the first derivative
        plt.subplot(3, 1, 2)
        plt.plot(t_fine, dy_fine, label='First Derivative', linestyle='--')
        plt.title("First Derivative")
        plt.xlabel("t")
        plt.ylabel("dy/dt")
        plt.legend()

        # Plot the second derivative
        plt.subplot(3, 1, 3)
        plt.plot(t_fine, d2y_fine, label='Second Derivative', linestyle='-.')
        plt.title("Second Derivative")
        plt.xlabel("t")
        plt.ylabel("d2y/dt2")
        plt.legend()

        plt.tight_layout()
        plt.show()

    def print_equations(self):
        print("Parametric Equations:")
        print(f"x(t) = {self.x_poly}")
        print(f"y(t) = {self.y_poly}")

        print("\nFirst Derivatives:")
        print(f"dx/dt = {self.x_poly_deriv}")
        print(f"dy/dt = {self.y_poly_deriv}")

        print("\nSecond Derivatives:")
        print(f"d2x/dt2 = {self.x_poly_deriv2}")
        print(f"d2y/dt2 = {self.y_poly_deriv2}")

if __name__ == "__main__":
    root = tk.Tk()
    paint_app = Paint(root)
    root.mainloop()
