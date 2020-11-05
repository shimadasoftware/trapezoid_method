"""
Created on Thu Sep 29 18:07:07 2020

@author: Juana Valentina Mendoza Santamaría
         (juana.mendoza@usantoto.edu.co)
"""

import numpy as np
import matplotlib.pyplot as plt
import parser
import tkinter as tk
import tkinter.font as font
from collections import defaultdict
import sympy

class GenerateSymbols(defaultdict):
    def __missing__(self, key):
        self[key] = sympy.Symbol(key)
        return self[key]


class TrapezoidMethod():
    ''' Trapezoid method class '''

#%%
    def __init__(self, formula='1 / (1 + x ** 2)', a=0, b=5, N=10):
        '''
        Default constructor.

        Parameters
        ----------
        formula : String
             Formula string with python mathematical instructions.
        a : float
             Lower limit of range
        b : float
             Upper limit of range
        N : int
             Number of subintervals (trapezoids)
        Returns
        -------
        '''
        self.formula = formula
        self.a       = a
        self.b       = b
        self.N       = N

#%%
    def f(self, x):
        '''
        Solve the formula.

        Parameters
        ----------
        x : float
            Independent variable of the function.
        Returns
        -------
        Formula solution for x.
        '''
        return eval(self.code)

#%%
    def trapz(self):
        '''
        Approximate the integral of f(x) from a to b by the trapezoid rule.
        (https://www.math.ubc.ca/~pwalls/math-python/integration/trapezoid-rule/)

        The trapezoid rule approximates the integral \int_a^b f(x) dx by the sum:
        (dx / 2) \sum_{k = 1}^N (f(x_k) + f(x_{k - 1}))
        where x_k = a + k * dx and dx = (b - a) / N.
        Returns
        -------
        float
            Approximation of the integral of f(x) from a to b using the
            trapezoid rule with N subintervals of equal length.
        '''
        x = np.linspace(self.a, self.b, self.N + 1) # N + 1 points make N subintervals
        y = self.f(x)
        y_right = y[1:]                             # Right endpoints
        y_left = y[:-1]                             # Left endpoints
        dx = (self.b - self.a) / self.N
        T = (dx / 2) * np.sum(y_right + y_left)

        return T

#%%
    def graphClicked(self):
        '''
        Show the graph.
        '''
        pyFormula = self.formulaTxt.get()

        try:
            d = GenerateSymbols()
            formula = sympy.latex(sympy.simplify(eval(pyFormula, d)))
        except Exception:
            formula = pyFormula

        self.code = parser.expr(pyFormula).compile()

        self.a = float(self.intervalMinTxt.get())
        self.b = float(self.intervalMaxTxt.get())
        self.N = int(self.nTxt.get())
    
        # x and y values for the trapezoid rule
        x = np.linspace(self.a, self.b, self.N + 1)
        y = self.f(x)

        # X and Y values for plotting y = f(x)
        X = np.linspace(self.a, self.b, 1000)
        Y = self.f(X)
        plt.plot(X, Y)      # Draw the line function

        ymax = 0
        for i in range(self.N):
            xs = [x[i], x[i], x[i + 1], x[i + 1]]
            ys = [0, y[i], y[i + 1], 0]
            plt.fill(xs, ys, 'b', edgecolor='b', alpha=0.2) # Draw the trapezoids
            if max(ys) > ymax:
                ymax = max(ys)

        # Calculate the area and errors
        tAprox = self.trapz()
        tReal = np.trapz(Y, x=X, dx=2)
        ae = np.abs(tReal - tAprox)
        re = np.abs((tReal - tAprox) / tReal)

        plt.title('Trapezoid Rule')         # Info box
        textstr = '\n'.join((
            'f(x) = $%s$'%formula,
            'interval = [{0}, {1}]'.format(self.a, self.b),
            'N = {0}'.format(self.N),
            'Area = ' + '%.5f' % tAprox,
            'Absolute error: ' + '%.5f' % ae,
            'Relative error: ' + '%.5f' % re
        ))
        # These are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

        # Place a text box in upper left in axes coords
        # Build a rectangle in axes coords
        left, width = 0, self.b
        bottom, height = 0, ymax
        right = left + width
        top = bottom + height
        plt.text(
            right, top, textstr, fontsize=10, 
            horizontalalignment='right', verticalalignment='top', 
            bbox=props
        )

        plt.grid(True)
        plt.show()

#%%
    def closeAboutClicked(self):
        '''
        Close the credits window.
        '''
        self.aboutWindow.destroy()

#%%
    def aboutClicked(self):
        '''
        Show the credits window.
        '''
        self.aboutWindow = tk.Toplevel(self.window)
        self.aboutWindow.title('About')
        self.aboutWindow.geometry("360x300")
        tk.Label(self.aboutWindow, text='Trapezoid Rule')

        # define font
        titleFont = font.Font(family="helvetica", size=12, weight="bold") 
        myFont = font.Font(family="helvetica", size=12)

        titleLbl = tk.Label(self.aboutWindow, text = 'Application: Trapezoid Rule', font=titleFont)
        titleLbl.grid(column=0, row=0, pady=(20, 5))

        versionLbl = tk.Label(self.aboutWindow, text = 'Version: 0.1', font=myFont)
        versionLbl.grid(column=0, row=1, pady=(5, 5))

        dateLbl = tk.Label(self.aboutWindow, text = 'Date: 20200930', font=myFont)
        dateLbl.grid(column=0, row=2, pady=(5, 5))

        authorLbl = tk.Label(self.aboutWindow, text = 'Author: Juana Valentina Mendoza Santamaría', font=myFont)
        authorLbl.grid(column=0, row=3, pady=(5, 5))

        emailLbl = tk.Label(self.aboutWindow, text = 'juana.mendoza@usantoto.edu.co', font=myFont)
        emailLbl.grid(column=0, row=4, pady=(5, 5))

        companyLbl = tk.Label(self.aboutWindow, text = 'Shimada Software (c)', font=myFont)
        companyLbl.grid(column=0, row=5, pady=(5, 5))

        universityLbl = tk.Label(self.aboutWindow, text = 'USTA Tunja - Facultad Ingeriería de Sistemas', font=myFont)
        universityLbl.grid(column=0, row=6, pady=(5, 5))

        teacherLbl = tk.Label(self.aboutWindow, text = 'Métodos numéricos: Ing. Martha Yolanda Díaz Sánchez', font=myFont)
        teacherLbl.grid(column=0, row=7, pady=(5, 5))

        closeBtn = tk.Button(self.aboutWindow, text='Close', command=self.closeAboutClicked, font=myFont)
        closeBtn.grid(column=0, row=8, pady=(10, 10))

        self.window.eval(f'tk::PlaceWindow {str(self.aboutWindow)} center')

#%%
    def closeClicked(self):
        '''
        Close the app.
        '''
        self.window.destroy()

#%%
    def showWindow(self):
        '''
        Show the app window.
        '''
        self.window = tk.Tk()
        self.window.title('Trapezoid Rule')
        self.window.geometry('640x240')
        self.window.eval('tk::PlaceWindow . center')

        # define font
        myFont = font.Font(family="helvetica", size=12)

        # Formula GUI
        formulaLbl = tk.Label(self.window, text = 'Formula', font=myFont)
        formulaLbl.grid(column=0, row=0, pady=(10, 10))

        self.formulaTxt = tk.Entry(self.window, width=60, font=myFont)
        self.formulaTxt.grid(column=1, row=0, pady=(10, 10))

        # Interval Min
        intervalMinLbl = tk.Label(self.window, text = 'Interval Min.', font=myFont)
        intervalMinLbl.grid(column=0, row=1, pady=(10, 10))

        self.intervalMinTxt = tk.Entry(self.window, width=20, font=myFont)
        self.intervalMinTxt.grid(sticky='W', column=1, row=1, pady=(10, 10))

        # Interval Max
        intervalMaxLbl = tk.Label(self.window, text = 'Interval Max.', font=myFont)
        intervalMaxLbl.grid(column=0, row=2, pady=(10, 10))

        self.intervalMaxTxt = tk.Entry(self.window, width=20, font=myFont)
        self.intervalMaxTxt.grid(sticky='W', column=1, row=2, pady=(10, 10))

        # N
        nLbl = tk.Label(self.window, text = 'N', font=myFont)
        nLbl.grid(column=0, row=3, pady=(10, 10))

        self.nTxt = tk.Entry(self.window, width=5, font=myFont)
        self.nTxt.grid(sticky='W', column=1, row=3, pady=(10, 10))

        # Show Graph Button
        graphBtn = tk.Button(self.window, text='Graph', command=self.graphClicked, font=myFont)
        graphBtn.grid(column=0, row=4, pady=(10, 10))

        # About Button
        aboutBtn = tk.Button(self.window, text='About', command=self.aboutClicked, font=myFont)
        aboutBtn.grid(column=1, row=4, pady=(10, 10))

        # Close Button
        closeBtn = tk.Button(self.window, text='Close', command=self.closeClicked, font=myFont)
        closeBtn.grid(column=2, row=4, pady=(10, 10))

        # Show window
        self.formulaTxt.focus()
        self.window.mainloop()

#%%
# '1 / (1 + x ** 2)' [0, 5] n=10
# 'np.exp(-x**2)' [0, 1] n=4
# 'np.sin(x)', [0, np.pi / 2 (1.570796327)], n=100
# '1/x**2', [1, 2], n=5
# Tkinter https://likegeeks.com/es/ejemplos-de-la-gui-de-python/
if __name__ == "__main__":
    TrapezoidMethod().showWindow()
