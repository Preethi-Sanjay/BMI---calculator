import tkinter as tk
from tkinter import ttk, font
import time
import threading

class NatureBMIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BOMOO-BMI Calculator")
        self.root.geometry("500x700")
        self.root.configure(bg="#F5F5DC")  # Beige background
        
        # Color palette
        self.colors = {
            "primary": "#6B8E23",    # Olive green
            "secondary": "#F5F5DC",  # Beige
            "accent": "#C4A484",     # Light brown
            "text": "#333333",       # Dark gray
            "light_text": "#F5F5DC",
            "highlight": "#8FBC8F",  # Light olive
            "error": "#B22222"       # Earthy red
        }
        
        # Font setup
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.main_font = font.Font(family="Helvetica", size=12)
        self.result_font = font.Font(family="Helvetica", size=14, weight="bold")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors["secondary"], padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header with nature theme
        header_frame = tk.Frame(main_frame, bg=self.colors["primary"])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame, 
            text="BAMBOO(❁´◡`❁)", 
            font=self.title_font, 
            bg=self.colors["primary"], 
            fg=self.colors["light_text"],
            pady=15
        ).pack()
        
        tk.Label(
            header_frame, 
            text="Find your BMI ", 
            font=self.main_font, 
            bg=self.colors["primary"], 
            fg=self.colors["light_text"]
        ).pack(pady=(0, 15))
        
        # Input card
        input_card = tk.Frame(
            main_frame,
            bg=self.colors["highlight"],
            padx=20,
            pady=20,
            relief=tk.RAISED,
            bd=2
        )
        input_card.pack(fill=tk.X, pady=10)
        
        # Weight input
        tk.Label(
            input_card,
            text="Your Weight (kg):",
            font=self.main_font,
            bg=self.colors["highlight"],
            fg=self.colors["text"]
        ).grid(row=0, column=0, sticky="w", pady=5)
        
        self.weight_entry = tk.Entry(
            input_card,
            font=self.main_font,
            bg="BEIGE",
            relief=tk.FLAT
        )
        self.weight_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Height input
        tk.Label(
            input_card,
            text="Your Height (cm):",
            font=self.main_font,
            bg=self.colors["highlight"],
            fg=self.colors["text"]
        ).grid(row=1, column=0, sticky="w", pady=5)
        
        self.height_entry = tk.Entry(
            input_card,
            font=self.main_font,
            bg="beige",
            relief=tk.FLAT
        )
        self.height_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Calculate button
        self.calc_button = tk.Button(
            main_frame,
            text="Calculate My BMI 🌱",
            font=self.main_font,
            bg=self.colors["primary"],
            fg=self.colors["light_text"],
            command=self.start_calculation,
            padx=20,
            pady=10,
            relief=tk.FLAT
        )
        self.calc_button.pack(pady=20)
        
        # Loading animation
        self.loading_frame = tk.Frame(main_frame, bg=self.colors["secondary"])
        
        self.loading_label = tk.Label(
            self.loading_frame,
            text="🌱 Growing your results...",
            font=self.main_font,
            bg=self.colors["secondary"],
            fg=self.colors["text"]
        )
        self.loading_label.pack(pady=(0, 10))
        
        # Custom progress bar style
        style = ttk.Style()
        style.configure("Nature.Horizontal.TProgressbar", 
                      background=self.colors["primary"],
                      troughcolor=self.colors["secondary"])
        
        self.progress = ttk.Progressbar(
            self.loading_frame,
            orient="horizontal",
            mode="indeterminate",
            length=200,
            style="Nature.Horizontal.TProgressbar"
        )
        self.progress.pack()
        
        # Results frame
        self.result_frame = tk.Frame(
            main_frame,
            bg=self.colors["highlight"],
            padx=20,
            pady=20
        )
        
        self.bmi_value = tk.Label(
            self.result_frame,
            text="BMI: --",
            font=self.result_font,
            bg=self.colors["highlight"],
            fg=self.colors["text"]
        )
        self.bmi_value.pack(anchor="w", pady=(0, 10))
        
        self.status_label = tk.Label(
            self.result_frame,
            text="Status: --",
            font=self.result_font,
            bg=self.colors["highlight"],
            fg=self.colors["primary"]
        )
        self.status_label.pack(anchor="w", pady=(0, 10))
        
        self.message_text = tk.StringVar()
        self.message_text.set("Enter your details to check your balance")
        
        self.message = tk.Label(
            self.result_frame,
            textvariable=self.message_text,
            font=self.main_font,
            bg=self.colors["highlight"],
            fg=self.colors["text"],
            wraplength=400,
            justify=tk.LEFT
        )
        self.message.pack(anchor="w", pady=(0, 10))
        
        # Footer
        tk.Label(
            main_frame,
            text="BOMOO- THE BMI CALCULATOR ",
            font=self.main_font,
            bg=self.colors["secondary"],
            fg=self.colors["primary"]
        ).pack(side=tk.BOTTOM, pady=20)
    
    def start_calculation(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            
            if weight <= 0 or height <= 0:
                raise ValueError("Please enter positive values")
                
            # Show loading
            self.loading_frame.pack(pady=20)
            self.result_frame.pack_forget()
            self.progress.start()
            
            # Start calculation in thread
            threading.Thread(
                target=self.calculate_bmi,
                args=(weight, height),
                daemon=True
            ).start()
            
        except ValueError as e:
            self.show_error(str(e))
    
    def calculate_bmi(self, weight, height):
        # Simulate processing time
        for i in range(3):
            time.sleep(0.7)
            self.update_loading_message(i)
        
        # Calculate BMI (height in meters)
        bmi = weight / ((height / 100) ** 2)        
        # Determine results
        if bmi < 18.5:
            status = "Underweight"
            color = "#DAA520"  # Golden
            message = ("Your natural balance is a bit light. Consider nourishing "
                      "yourself with wholesome foods and maybe consult a nutritionist "
                      "to help you grow stronger.")
        elif 18.5 <= bmi < 25:
            status = "Healthy Balance"
            color = self.colors["primary"]  # Olive green
            message = ("Wonderful! Your body is  great . Keep enjoying "
                      "fresh foods, clean water, and joyful movement!")
        elif 25 <= bmi < 30:
            status = "Overweight"
            color = "#CD853F"  # Earthy brown
            message = ("Your natural balance could use some adjustment. Small changes "
                      "like walking after a meal and choosing whole foods can help.")
        else:
            status = "Obese"
            color = self.colors["error"]  # Earthy red
            message = ("Your body is carrying more weight than is natural. Please be "
                      "kind to yourself and consider talking with a healthcare provider.")
        
        # Update UI
        self.root.after(0, self.show_results, bmi, status, color, message)
    
    def update_loading_message(self, step):
        messages = [
            "🌿 Gently calculating...",
            "🍃 Analyzing your weight...",
            "🌱 Almost there..."
        ]
        self.loading_label.config(text=messages[step % len(messages)])
    
    def show_results(self, bmi, status, color, message):
        # Stop loading animation
        self.progress.stop()
        self.loading_frame.pack_forget()
        
        # Update results
        self.bmi_value.config(text=f"BMI: {bmi:.1f}")
        self.status_label.config(text=f"Status: {status}", fg=color)
        self.message_text.set(message)
        
        # Show results frame
        self.result_frame.pack(fill=tk.X, pady=20)
    
    def show_error(self, message):
        self.progress.stop()
        self.loading_frame.pack_forget()
        
        self.bmi_value.config(text="BMI: --")
        self.status_label.config(text="Error!", fg=self.colors["error"])
        self.message_text.set(message)
        
        self.result_frame.pack(fill=tk.X, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = NatureBMIApp(root)
    root.mainloop()