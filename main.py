import tkinter as tk
import json
import random
import time

class VocabularyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1920x1080')
        self.root.attributes('-fullscreen', True)
        
        # Load data
        self.load_data()
        
        # Initialize variables
        self.current_lesson = None
        self.current_data = []
        self.i = 0
        self.start_time = time.time()  # Start timer immediately
        
        # Create frames
        self.lesson_frame = tk.Frame(self.root)
        self.practice_frame = tk.Frame(self.root)
        
        # Create global timer label that will be visible on all pages
        self.timer_label = tk.Label(self.root, text="Zeit: 00:00", font=('Arial', 25))
        self.timer_label.place(relx=0, rely=0, anchor='nw')
        
        # Start the timer
        self.update_timer()
        
        # Show lesson selection first
        self.show_lesson_selection()
        
    def load_data(self):
        """Load vocabulary data from the new structured format"""
        try:
            data_path = 'data/b1_en_vocab_new.json'
            with open(data_path, 'r', encoding='utf-8') as f:
                self.lessons_data = json.load(f)
        except FileNotFoundError:
            # Fallback to old format if new file doesn't exist
            data_path = 'data/b1_en_vocab.json'
            with open(data_path, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
                # Convert old format to new format
                self.lessons_data = [{
                    "lecture": "Alle Vokabeln",
                    "vocabulary": old_data
                }]
    
    def show_lesson_selection(self):
        """Show the lesson selection page"""
        self.lesson_frame.pack(fill='both', expand=True)
        self.practice_frame.pack_forget()
        
        # Clear previous widgets
        for widget in self.lesson_frame.winfo_children():
            widget.destroy()
        
        # Title
        title_label = tk.Label(self.lesson_frame, text="Wähle eine Lektion", 
                              font=('Arial', 50), pady=50)
        title_label.pack()
        
        # Create a frame for the scrollable content
        scroll_frame = tk.Frame(self.lesson_frame)
        scroll_frame.pack(fill='both', expand=True, padx=50, pady=20)
        
        # Create a canvas and scrollbar
        canvas = tk.Canvas(scroll_frame, highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create lesson buttons in the scrollable frame
        for i, lesson in enumerate(self.lessons_data):
            lesson_name = lesson['lecture']
            vocab_count = len(lesson['vocabulary'])
            
            button_text = f"{lesson_name} ({vocab_count} Vokabeln)"
            lesson_button = tk.Button(
                scrollable_frame, 
                text=button_text,
                font=('Arial', 25),
                command=lambda l=lesson: self.start_lesson(l),
                width=30,
                height=2,
                pady=10
            )
            lesson_button.pack(pady=10)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Exit button
        exit_button = tk.Button(
            self.lesson_frame,
            text="EXIT",
            font=('Arial', 15),
            command=self.root.destroy
        )
        exit_button.place(relx=1, rely=0, anchor='ne')
    
    def start_lesson(self, lesson):
        """Start practicing a specific lesson"""
        self.current_lesson = lesson
        self.current_data = lesson['vocabulary'].copy()
        random.shuffle(self.current_data)
        self.i = 0
        
        self.show_practice_page()
    
    def show_practice_page(self):
        """Show the practice page"""
        self.lesson_frame.pack_forget()
        self.practice_frame.pack(fill='both', expand=True)
        
        # Clear previous widgets
        for widget in self.practice_frame.winfo_children():
            widget.destroy()
        
        # Create practice widgets
        self.label = tk.Label(self.practice_frame, text='', font=('Arial', 50*3))
        self.label.place(relx=0.5, rely=0.35, anchor='center')
        
        self.label2 = tk.Label(self.practice_frame, text='', font=('Arial', 30*3), fg='green')
        self.label2.place(relx=0.5, rely=0.6, anchor='center')
        
        self.label3 = tk.Label(self.practice_frame, text=f"{self.i}/{len(self.current_data)}", font=('Arial', 30))
        self.label3.place(relx=0.5, rely=0, anchor='n')
        
        self.button = tk.Button(self.practice_frame, text='Mehr', font=('Arial', 30), command=self.mehr)
        self.button.place(relx=0.5, rely=0.9, anchor='center')
        
        self.zuruck_button = tk.Button(self.practice_frame, text='zurück', font=('Arial', 20), command=self.zuruck)
        self.zuruck_button.place(relx=0.2, rely=0.9, anchor='center')
        
        # Menu button to go back to lesson selection
        menu_button = tk.Button(self.practice_frame, text='Menu', font=('Arial', 20), command=self.show_lesson_selection)
        menu_button.place(relx=0.8, rely=0.9, anchor='center')
        
        exit_button = tk.Button(self.practice_frame, text='EXIT', font=('Arial', 15), command=self.root.destroy)
        exit_button.place(relx=1, rely=0, anchor='ne')
        
        # Show first word
        self.mehr()
    
    def update_timer(self):
        """Update the timer display"""
        elapsed_time = time.time() - self.start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        self.timer_label.config(text=f"Zeit: {minutes:02d}:{seconds:02d}")
        self.root.after(1000, self.update_timer)
    
    def mehr(self):
        """Show the next German word"""
        if self.i < len(self.current_data):
            text = self.current_data[self.i]['de']
            num = min(int(1920/len(text)), 100)  # Limit font size
            
            self.label.config(font=('Helvetica', num))
            self.label.config(text=text)
            self.label2.config(text='')
            self.button.config(text='Offenbaren')
            self.button.config(command=self.offenbaren)
            self.label3.config(text=f"{self.i + 1}/{len(self.current_data)}")
        else:
            # End of lesson
            self.label.config(text="Lektion beendet!", font=('Arial', 50))
            self.label2.config(text="")
            self.button.config(text="Zurück zum Menu")
            self.button.config(command=self.show_lesson_selection)
    
    def offenbaren(self):
        """Show the English translation"""
        if self.i < len(self.current_data):
            self.label2.config(text=self.current_data[self.i]['en'])
            self.button.config(text='Mehr')
            self.button.config(command=self.mehr)
            self.i += 1
    
    def zuruck(self):
        """Go back to previous word"""
        if self.i > 0:
            self.i -= 1
            self.mehr()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = VocabularyApp()
    app.run()