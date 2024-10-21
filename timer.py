import tkinter as tk
from time import time

class NeonStopwatch:
    def __init__(self, root):
        self.root = root
        self.root.title("Neon Stopwatch")
        self.root.geometry("500x300")
        self.root.config(bg="#1d1f21")
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        
        # Create a canvas for dynamic gradient background
        self.bg_canvas = tk.Canvas(root, width=500, height=300, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        
        # Gradient colors for the background motion
        self.gradient_colors = [
            ["#ff00ff", "#ff00cc", "#cc00ff"],
            ["#ff00cc", "#cc00ff", "#9900ff"],
            ["#cc00ff", "#9900ff", "#6600ff"],
            ["#9900ff", "#6600ff", "#0033ff"],
            ["#6600ff", "#0033ff", "#00ffff"],
            ["#0033ff", "#00ffff", "#00ffcc"],
        ]
        self.motion_step = 0
        self.animate_background()
        
        # Neon time display
        self.time_label = tk.Label(root, text="00:00:00.000", font=("Helvetica", 50, "bold"), bg="#1d1f21", fg="#0ff", padx=20)
        self.time_label.place(relx=0.5, rely=0.3, anchor="center")
        self.add_neon_effect(self.time_label)

        # Neon Button Styles
        self.button_style = {
            "font": ("Helvetica", 14, "bold"), 
            "bg": "#0ff", 
            "fg": "#1d1f21", 
            "activebackground": "#0cf", 
            "bd": 0, 
            "relief": "flat", 
            "highlightthickness": 0, 
            "padx": 15, 
            "pady": 5
        }
        
        # Buttons with Neon Effects
        self.start_button = tk.Button(root, text="Start", command=self.start, **self.button_style)
        self.start_button.place(relx=0.2, rely=0.7, anchor="center")

        self.stop_button = tk.Button(root, text="Stop", state="disabled", command=self.stop, **self.button_style)
        self.stop_button.place(relx=0.5, rely=0.7, anchor="center")

        self.reset_button = tk.Button(root, text="Reset", state="disabled", command=self.reset, **self.button_style)
        self.reset_button.place(relx=0.8, rely=0.7, anchor="center")

    def animate_background(self):
        """Creates an animated neon gradient background that changes over time."""
        # Clear the previous gradient
        self.bg_canvas.delete("all")
        
        # Get the current gradient colors based on the step
        current_gradient = self.gradient_colors[self.motion_step]
        
        # Draw gradient rectangles with changing colors
        canvas_width = 500
        canvas_height = 300
        steps = len(current_gradient)
        for i, color in enumerate(current_gradient):
            step_height = canvas_height // steps
            self.bg_canvas.create_rectangle(
                0, i * step_height, canvas_width, (i + 1) * step_height,
                outline="", fill=color
            )

        # Cycle through the color sets for motion
        self.motion_step = (self.motion_step + 1) % len(self.gradient_colors)
        self.root.after(150, self.animate_background)  # Update every 150 milliseconds for motion

    def add_neon_effect(self, widget):
        """Adds hover effect to give a neon glow to widgets."""
        widget.config(fg="#0ff")
        widget.bind("<Enter>", lambda e: widget.config(fg="#0cf"))
        widget.bind("<Leave>", lambda e: widget.config(fg="#0ff"))

    def update_time(self):
        if self.running:
            self.elapsed_time = time() - self.start_time
            minutes, seconds = divmod(self.elapsed_time, 60)
            hours, minutes = divmod(minutes, 60)
            milliseconds = int((self.elapsed_time - int(self.elapsed_time)) * 1000)
            formatted_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{milliseconds:03}"
            self.time_label.config(text=formatted_time)
            self.root.after(10, self.update_time)  # Update every 10 milliseconds for accuracy

    def start(self):
        if not self.running:
            self.start_time = time() - self.elapsed_time
            self.running = True
            self.update_time()
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.reset_button.config(state="normal")

    def stop(self):
        if self.running:
            self.running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")

    def reset(self):
        self.running = False
        self.elapsed_time = 0
        self.time_label.config(text="00:00:00.000")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.reset_button.config(state="disabled")

# Run the neon stopwatch
root = tk.Tk()
app = NeonStopwatch(root)
root.mainloop()
