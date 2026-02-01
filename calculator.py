"""
Colorful Calculator App (Tkinter)

Run: python3 calculator.py

Features:
- Basic operations (+, -, *, /, % and parentheses)
- Clear (C), Backspace (⌫), Evaluate (=)
- Keyboard input, Enter to evaluate, Esc to clear
- Colorful theme, hover & press effects, responsive layout
- Safe expression evaluation using ast (no eval of arbitrary code)
"""

import tkinter as tk
from tkinter import font as tkfont
import ast
import operator
import math

# --- Safe evaluator ---------------------------------------------------------

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Allowed functions for safe calls
ALLOWED_FUNCTIONS = {
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log,  # log(x) or log(x, base)
    'abs': abs,
}


def safe_eval(expr: str) -> float:
    """Evaluate a math expression safely using ast.

    Supports: + - * / % ** unary +/- and parentheses.
    """
    # replace friendly symbols
    expr = expr.replace("×", "*").replace("÷", "/").replace('^', '**')

    try:
        node = ast.parse(expr, mode="eval")
    except Exception as exc:
        raise ValueError("Invalid expression") from exc

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):  # python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Invalid constant")
        NumNode = getattr(ast, 'Num', None)
        if NumNode is not None and isinstance(node, NumNode):  # older nodes
            return node.n
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in ALLOWED_OPERATORS:
                try:
                    return ALLOWED_OPERATORS[op_type](left, right)
                except ZeroDivisionError:
                    raise ValueError("Division by zero")
            raise ValueError("Unsupported operator")
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in ALLOWED_OPERATORS:
                return ALLOWED_OPERATORS[op_type](operand)
            raise ValueError("Unsupported unary operator")
        # function calls like sqrt(9), sin(0)
        if isinstance(node, ast.Call):
            # only allow simple name calls: e.g., sqrt(x)
            if isinstance(node.func, ast.Name) and node.func.id in ALLOWED_FUNCTIONS:
                func = ALLOWED_FUNCTIONS[node.func.id]
                args = [_eval(a) for a in node.args]
                try:
                    return func(*args)
                except TypeError:
                    raise ValueError("Invalid function arguments")
            raise ValueError("Unsupported function call")
        raise ValueError(f"Unsupported expression: {type(node)}")

    result = _eval(node)
    return result


# --- UI --------------------------------------------------------------------

class ColorButton(tk.Button):
    def __init__(self, master=None, bg="#ffffff", activebg="#dddddd", **kwargs):
        super().__init__(master, bg=bg, activebackground=activebg, bd=0, highlightthickness=0, **kwargs)
        self._bg = bg
        self._activebg = activebg
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

    def on_enter(self, _e):
        self.configure(bg=self._activebg)

    def on_leave(self, _e):
        self.configure(bg=self._bg)

    def on_press(self, _e):
        self.configure(relief="sunken")

    def on_release(self, _e):
        self.configure(relief="flat")


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vibe Calculator ✨")
        self.geometry("380x560")
        self.minsize(320, 480)
        self.configure(bg="#2b2b2b")

        # Fonts
        self.display_font = tkfont.Font(family="Helvetica", size=28, weight="bold")
        self.expr_font = tkfont.Font(family="Helvetica", size=14)
        self.button_font = tkfont.Font(family="Helvetica", size=16, weight="bold")

        # Themes
        self.themes = {
            "vibe": {
                "top_color": (94, 58, 255),
                "bottom_color": (0, 224, 208),
                "num_bg": "#ffffff",
                "num_active": "#f3f3f3",
                "op_bg": "#94f3ed",
                "op_active": "#c4fff7",
                "acc_bg": "#7c5cff",
                "acc_active": "#9c86ff",
                "clear_bg": "#ff6b6b",
                "clear_active": "#ff8787",
                "special_bg": "#ffd166",
                "special_active": "#ffe29a",
                "expr_fg": "#f1f1f1",
                "result_fg": "#ffffff",
                "button_fg": "#111111",
            },
            "dark": {
                "top_color": (30, 30, 40),
                "bottom_color": (10, 10, 20),
                "num_bg": "#2b2b2b",
                "num_active": "#3b3b3b",
                "op_bg": "#44475a",
                "op_active": "#565867",
                "acc_bg": "#ffb86c",
                "acc_active": "#ffd29f",
                "clear_bg": "#ff5555",
                "clear_active": "#ff7777",
                "special_bg": "#6272a4",
                "special_active": "#7080c1",
                "expr_fg": "#dfe6f3",
                "result_fg": "#f8f8f2",
                "button_fg": "#ffffff",
            },
        }
        self.theme_name = "vibe"
        self.theme = self.themes[self.theme_name]

        # Gradient background (draw on canvas)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._draw_gradient)

        # Overlay frame for controls
        self.frame = tk.Frame(self.canvas, bg=self['bg'], bd=0)
        self.frame_window = self.canvas.create_window((0, 0), window=self.frame, anchor="nw", width=self.winfo_width())

        # State
        self.expression = ""

        self._build_ui()
        self._bind_keys()

        # Make grid expand
        for i in range(6):
            self.btn_frame.rowconfigure(i, weight=1)
        for j in range(4):
            self.btn_frame.columnconfigure(j, weight=1)

    def _draw_gradient(self, event=None):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.canvas.delete("_grad")

        # vertical gradient between theme colors
        top_color = self.theme["top_color"]
        bottom_color = self.theme["bottom_color"]
        steps = h if h > 0 else 100
        r1, g1, b1 = top_color
        r2, g2, b2 = bottom_color

        for i in range(steps):
            r = int(r1 + (r2 - r1) * (i / steps))
            g = int(g1 + (g2 - g1) * (i / steps))
            b = int(b1 + (b2 - b1) * (i / steps))
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, w, i, fill=color, tags=("_grad",))

        # reposition frame to fill canvas
        if hasattr(self, 'frame_window'):
            self.canvas.coords(self.frame_window, 0, 0)
            self.canvas.itemconfig(self.frame_window, width=w)
        else:
            # fallback for older behavior
            self.canvas.coords(self.frame, 0, 0)
            self.canvas.itemconfig(self.frame, width=w)

    def _build_ui(self):
        # Display
        disp_pad = 12
        self.display_frame = tk.Frame(self.frame, bg=self['bg'], pady=20)
        self.display_frame.pack(fill="x", padx=14, pady=(22, 6))

        # top row for theme toggle and optional title
        top_row = tk.Frame(self.display_frame, bg=self.display_frame['bg'])
        top_row.pack(fill="x")

        self.theme_btn = ColorButton(top_row, text=self._theme_icon(), bg=self.theme["special_bg"], activebg=self.theme["special_active"],
                                     font=tkfont.Font(size=12, weight="bold"), fg=self.theme["button_fg"], command=self._toggle_theme)
        self.theme_btn.pack(side="left")

        # quick sqrt button on the right
        sqrt_btn = ColorButton(top_row, text="√", bg=self.theme["special_bg"], activebg=self.theme["special_active"],
                               font=tkfont.Font(size=12, weight="bold"), fg=self.theme["button_fg"], command=lambda: self._on_button('√'))
        sqrt_btn.pack(side="right")

        # Expression and result
        self.expr_label = tk.Label(self.display_frame, text=self.expression, anchor="e",
                                   font=self.expr_font, fg=self.theme["expr_fg"], bg=self.display_frame['bg'], padx=10)
        self.expr_label.pack(fill="x")

        self.result_label = tk.Label(self.display_frame, text="0", anchor="e",
                                     font=self.display_font, fg=self.theme["result_fg"], bg=self.display_frame['bg'], padx=10)
        self.result_label.pack(fill="x", pady=(6, 0))

        # Buttons frame
        self.btn_frame = tk.Frame(self.frame, bg=self['bg'], padx=12, pady=12)
        self.btn_frame.pack(fill="both", expand=True)

        self._build_buttons()

    def _build_buttons(self):
        # remove existing
        for w in list(self.btn_frame.winfo_children()):
            w.destroy()

        # Button factory
        A = lambda t, bg, abg: (t, bg, abg)
        t = self.theme
        buttons = [
            [A("C", t["clear_bg"], t["clear_active"]), A("( )", t["special_bg"], t["special_active"]), A("^", t["special_bg"], t["special_active"]), A("⌫", t["clear_bg"], t["clear_active"])],
            [A("7", t["num_bg"], t["num_active"]), A("8", t["num_bg"], t["num_active"]), A("9", t["num_bg"], t["num_active"]), A("÷", t["op_bg"], t["op_active"])],
            [A("4", t["num_bg"], t["num_active"]), A("5", t["num_bg"], t["num_active"]), A("6", t["num_bg"], t["num_active"]), A("×", t["op_bg"], t["op_active"])],
            [A("1", t["num_bg"], t["num_active"]), A("2", t["num_bg"], t["num_active"]), A("3", t["num_bg"], t["num_active"]), A("-", t["op_bg"], t["op_active"])],
            [A("0", t["num_bg"], t["num_active"]), A(".", t["num_bg"], t["num_active"]), A("=", t["acc_bg"], t["acc_active"]), A("+", t["op_bg"], t["op_active"])],
        ]

        for r, row in enumerate(buttons):
            for c, (text, bg, abg) in enumerate(row):
                btn = ColorButton(self.btn_frame, text=text, bg=bg, activebg=abg,
                                  font=self.button_font, fg=self.theme["button_fg"],
                                  command=lambda t=text: self._on_button(t))
                btn.grid(row=r, column=c, sticky="nsew", padx=8, pady=8, ipadx=6, ipady=6)

                if text == "0":
                    btn.grid_configure(columnspan=1)

    def _bind_keys(self):
        self.bind_all("<Key>", self._on_key)
        self.bind_all("<Return>", lambda e: self._on_button('='))
        self.bind_all("=", lambda e: self._on_button('='))
        self.bind_all("<BackSpace>", lambda e: self._on_button('⌫'))
        self.bind_all("<Escape>", lambda e: self._on_button('C'))
        self.bind_all("t", lambda e: self._toggle_theme())

    def _theme_icon(self):
        return "🌙" if self.theme_name == "vibe" else "☀️"

    def _toggle_theme(self):
        self.theme_name = "dark" if self.theme_name == "vibe" else "vibe"
        self.theme = self.themes[self.theme_name]
        # update visuals
        self.theme_btn.configure(text=self._theme_icon(), bg=self.theme["special_bg"], activebackground=self.theme["special_active"], fg=self.theme["button_fg"])
        self.expr_label.configure(fg=self.theme["expr_fg"])
        self.result_label.configure(fg=self.theme["result_fg"])
        self._build_buttons()
        self._draw_gradient()

    def _on_key(self, event):
        char = event.char
        if char.isdigit() or char in ".()+-*/%":
            # map * and / to display characters × ÷ for consistency
            if char == '*':
                self._append('×')
            elif char == '/':
                self._append('÷')
            else:
                self._append(char)
        elif char == '\r':
            self._on_button('=')

    def _append(self, s):
        self.expression += s
        self._update_display()

    def _on_button(self, label: str):
        if label == 'C':
            self.expression = ""
            self.result_label.config(text="0")
            self._update_display()
            return
        if label == '⌫':
            self.expression = self.expression[:-1]
            self._update_display()
            return
        if label == '( )':
            # smart parentheses: add '(' if not present or last char is operator, else ')'
            if not self.expression or self.expression[-1] in '+-×÷*/%^':
                self._append('(')
            else:
                self._append(')')
            return
        if label == '^':
            self._append('^')
            return
        if label == '√':
            # insert sqrt( for convenience
            self._append('sqrt(')
            return
        if label == '=':
            self._evaluate()
            return

        # normal button
        self._append(label)

    def _update_display(self):
        # trim long expressions for small screen
        expr_shown = self.expression if len(self.expression) <= 32 else '...' + self.expression[-32:]
        self.expr_label.config(text=expr_shown)

        # attempt to show running result
        try:
            if self.expression and self.expression[-1] not in '+-×÷*/%(':
                val = safe_eval(self._normalize_expr(self.expression))
                # show integer without decimal when possible
                if isinstance(val, float) and val.is_integer():
                    val_str = str(int(val))
                else:
                    val_str = str(round(val, 10)).rstrip('0').rstrip('.')
                self.result_label.config(text=val_str)
            else:
                self.result_label.config(text="0")
        except Exception:
            self.result_label.config(text="Error")

    def _normalize_expr(self, expr: str) -> str:
        # Map display operators to python syntax (×, ÷, ^)
        return expr.replace('×', '*').replace('÷', '/').replace('^', '**')

    def _evaluate(self):
        try:
            result = safe_eval(self._normalize_expr(self.expression))
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.expression = str(result)
            self._update_display()
        except Exception as exc:
            self.result_label.config(text="Error")

if __name__ == '__main__':
    app = Calculator()
    app.mainloop()
