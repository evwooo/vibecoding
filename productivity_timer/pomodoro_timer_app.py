import tkinter as tk
from tkinter import font

# --- Constants ---
DARK_OLIVE = "#3D4127"
LIGHT_OLIVE = "#636B2F"
SAGE = "#BAC095"
LIME = "#D4DE95"
LIME_DARKER = "#b9c281" # For button press effect
FONT_NAME = "Courier"
TIMER_FONT_SIZE = 40
BREAK_TIMER_FONT_SIZE = 20
LABEL_FONT_SIZE = 45
BUTTON_FONT_SIZE = 12
ARROW_FONT_SIZE = 16

# --- Timer State ---
reps = 0
timer = None
is_paused = False
work_minutes = 25
break_minutes = 5

# --- Custom Rounded Button ---
class RoundedButton(tk.Canvas):
    def __init__(self, parent, width, height, cornerradius, padding, color, text, text_color, command):
        super().__init__(parent, width=width, height=height, bg=SAGE, highlightthickness=0)
        self.command = command
        self.color = color
        self.text = text
        self.text_color = text_color
        self.width = width
        self.height = height
        self.cornerradius = cornerradius
        self.padding = padding
        self.state = "normal"

        self.button_bg = self.create_rounded_rect(0, 0, width, height, radius=cornerradius, fill=color)
        self.button_text = self.create_text(width/2, height/2, text=text, fill=text_color, font=(FONT_NAME, BUTTON_FONT_SIZE))

        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

    def _on_press(self, event):
        if self.state == "normal":
            self.itemconfig(self.button_bg, fill=LIME_DARKER)

    def _on_release(self, event):
        if self.state == "normal":
            self.itemconfig(self.button_bg, fill=self.color)
            if self.command:
                self.command()
    
    def config(self, **kwargs):
        if 'state' in kwargs:
            self.state = kwargs.pop('state')
            if self.state == "disabled":
                self.itemconfig(self.button_bg, fill="grey")
                self.itemconfig(self.button_text, fill="#A9A9A9")
            else:
                self.itemconfig(self.button_bg, fill=self.color)
                self.itemconfig(self.button_text, fill=self.text_color)
        if 'text' in kwargs:
             self.itemconfig(self.button_text, text=kwargs.pop('text'))
        super().config(**kwargs)


# --- Functions ---
def adjust_time(timer_type, delta):
    """Adjusts the work or break time."""
    global work_minutes, break_minutes
    if timer_type == 'work':
        work_minutes = max(1, min(99, work_minutes + delta))
        work_time_label.config(text=f"{work_minutes:02d}:00")
        if start_button.state == 'normal':
             main_timer_label.config(text=f"{work_minutes:02d}:00")
    elif timer_type == 'break':
        break_minutes = max(1, min(30, break_minutes + delta))
        break_time_label.config(text=f"{break_minutes:02d}:00")

def set_adjustment_buttons_state(state):
    """Enables or disables all time adjustment buttons."""
    for button in [work_up_button, work_down_button, break_up_button, break_down_button]:
        button.config(state=state)

def pause_timer():
    """Pauses or continues the timer."""
    global is_paused
    is_paused = not is_paused
    if is_paused:
        pause_button.config(text="Continue")
        if timer:
            window.after_cancel(timer)
    else:
        pause_button.config(text="Pause")
        current_time_str = main_timer_label.cget('text')
        try:
            mins, secs = map(int, current_time_str.split(':'))
            total_seconds = mins * 60 + secs
            if total_seconds > 0:
                count_down(total_seconds)
        except ValueError:
            pass

def start_timer():
    """Starts the timer countdown."""
    global reps, is_paused
    is_paused = False
    pause_button.config(text="Pause", state="normal")
    start_button.config(state="disabled")
    set_adjustment_buttons_state("disabled")
    reps += 1

    if reps % 8 == 0:
        count_down(break_minutes * 3 * 60)
        title_label.config(text="Pomodoro Break", fg=LIGHT_OLIVE)
    elif reps % 2 == 0:
        count_down(break_minutes * 60)
        title_label.config(text="Break", fg=LIGHT_OLIVE)
    else:
        count_down(work_minutes * 60)
        title_label.config(text="Work", fg=DARK_OLIVE)

def reset_timer():
    """Resets the timer to the initial state."""
    global reps, timer, is_paused
    if timer:
        window.after_cancel(timer)
    reps = 0
    timer = None
    is_paused = False

    title_label.config(text="Timer", fg=DARK_OLIVE)
    main_timer_label.config(text=f"{work_minutes:02d}:00")
    check_marks.config(text="")
    start_button.config(state="normal")
    pause_button.config(text="Pause", state="disabled")
    set_adjustment_buttons_state("normal")

def count_down(count):
    """Handles the countdown mechanism and updates the display."""
    global timer
    count_min, count_sec = divmod(count, 60)
    main_timer_label.config(text=f"{count_min:02d}:{count_sec:02d}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        if reps % 8 != 0:
            marks = "✔" * (reps // 2)
            check_marks.config(text=marks)
        else:
            check_marks.config(text="")


# --- UI Setup ---
window = tk.Tk()
window.title("Pomodoro Timer")
window.config(bg=SAGE)
window.minsize(450, 350)

# --- Font Definitions ---
timer_font = font.Font(family=FONT_NAME, size=TIMER_FONT_SIZE, weight="bold")
break_timer_font = font.Font(family=FONT_NAME, size=BREAK_TIMER_FONT_SIZE, weight="bold")
label_font = font.Font(family=FONT_NAME, size=LABEL_FONT_SIZE, weight="bold")
arrow_font = font.Font(family=FONT_NAME, size=ARROW_FONT_SIZE)

# --- Grid Configuration ---
window.grid_rowconfigure(0, weight=2)
window.grid_rowconfigure(1, weight=2)
window.grid_rowconfigure(2, weight=1)
window.grid_rowconfigure(3, weight=1)
window.grid_rowconfigure(4, weight=1)
window.grid_columnconfigure(0, weight=1)

# Title Label
title_label = tk.Label(window, text="Timer", fg=DARK_OLIVE, bg=SAGE, font=label_font)
title_label.grid(row=0, column=0, sticky="nsew")

# Main Timer Display
main_timer_label = tk.Label(window, text=f"{work_minutes:02d}:00", fg=DARK_OLIVE, bg=SAGE, font=timer_font)
main_timer_label.grid(row=1, column=0, sticky="nsew")

# --- Time Adjustment UI ---
adjustment_frame = tk.Frame(window, bg=SAGE)
adjustment_frame.grid(row=2, column=0, sticky="nsew")
adjustment_frame.grid_columnconfigure(0, weight=1) # Center the inner frame

inner_adjustment_frame = tk.Frame(adjustment_frame, bg=SAGE)
inner_adjustment_frame.grid(row=0, column=0)

# Work Time Adjustment
work_down_button = tk.Button(inner_adjustment_frame, text="‹", font=arrow_font, command=lambda: adjust_time('work', -1), relief="flat", bg=SAGE, fg=DARK_OLIVE)
work_down_button.grid(row=0, column=0, padx=(0, 5))
work_time_label = tk.Label(inner_adjustment_frame, text=f"{work_minutes:02d}:00", font=break_timer_font, bg=SAGE, fg=DARK_OLIVE)
work_time_label.grid(row=0, column=1)
work_up_button = tk.Button(inner_adjustment_frame, text="›", font=arrow_font, command=lambda: adjust_time('work', 1), relief="flat", bg=SAGE, fg=DARK_OLIVE)
work_up_button.grid(row=0, column=2, padx=(5, 20))

# Break Time Adjustment
break_down_button = tk.Button(inner_adjustment_frame, text="‹", font=arrow_font, command=lambda: adjust_time('break', -1), relief="flat", bg=SAGE, fg=LIGHT_OLIVE)
break_down_button.grid(row=0, column=3, padx=(0, 5))
break_time_label = tk.Label(inner_adjustment_frame, text=f"{break_minutes:02d}:00", font=break_timer_font, bg=SAGE, fg=LIGHT_OLIVE)
break_time_label.grid(row=0, column=4)
break_up_button = tk.Button(inner_adjustment_frame, text="›", font=arrow_font, command=lambda: adjust_time('break', 1), relief="flat", bg=SAGE, fg=LIGHT_OLIVE)
break_up_button.grid(row=0, column=5, padx=(5, 0))

# --- Control Buttons ---
button_frame = tk.Frame(window, bg=SAGE)
button_frame.grid(row=3, column=0, sticky="nsew")
button_frame.grid_columnconfigure((0, 1, 2), weight=1)

start_button = RoundedButton(button_frame, width=80, height=35, cornerradius=15, padding=5, color=LIME, text="Start", text_color=DARK_OLIVE, command=start_timer)
start_button.grid(row=0, column=0, pady=5)
pause_button = RoundedButton(button_frame, width=80, height=35, cornerradius=15, padding=5, color=LIME, text="Pause", text_color=DARK_OLIVE, command=pause_timer)
pause_button.config(state="disabled")
pause_button.grid(row=0, column=1, pady=5)
reset_button = RoundedButton(button_frame, width=80, height=35, cornerradius=15, padding=5, color=LIME, text="Reset", text_color=DARK_OLIVE, command=reset_timer)
reset_button.grid(row=0, column=2, pady=5)

# Checkmarks
check_marks = tk.Label(window, text="", fg=DARK_OLIVE, bg=SAGE, font=(FONT_NAME, 15, "bold"))
check_marks.grid(row=4, column=0, sticky="nsew", pady=10)

window.mainloop()
