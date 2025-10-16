import tkinter as tk
from tkinter import scrolledtext
import os
import shlex

class TerminalEmulator:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_gui()
        
    def setup_gui(self):
        """Настройка графического интерфейса"""
        username = os.getenv('USERNAME') or os.getenv('USER')
        hostname = os.getenv('COMPUTERNAME') or 'localhost'
        
        self.root.title(f"Эмулятор - [{username}@{hostname}]")
        self.root.geometry("800x600")
        
        # Область вывода
        self.output_area = scrolledtext.ScrolledText(
            self.root, 
            wrap=tk.WORD,
            bg='black',
            fg='white',
            font=('Courier New', 10)
        )
        self.output_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.output_area.config(state=tk.DISABLED)
        
        # Поле ввода
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.prompt_label = tk.Label(
            input_frame, 
            text=f"{username}@{hostname}:~$ ",
            bg='black',
            fg='green',
            font=('Courier New', 10)
        )
        self.prompt_label.pack(side=tk.LEFT)
        
        self.input_entry = tk.Entry(
            input_frame,
            bg='black',
            fg='white',
            font=('Courier New', 10)
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_entry.bind('<Return>', self.execute_command)
        self.input_entry.focus()
        
        self.print_output("Добро пожаловать в эмулятор терминала!\n")
        self.print_output("Доступные команды: ls, cd, exit\n")
        
    def print_output(self, text):
        """Вывод текста в область вывода"""
        self.output_area.config(state=tk.NORMAL)
        self.output_area.insert(tk.END, text)
        self.output_area.see(tk.END)
        self.output_area.config(state=tk.DISABLED)
        
    def execute_command(self, event=None):
        """Выполнение команды"""
        command = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)
        
        self.print_output(f"\n{self.prompt_label.cget('text')}{command}\n")
        
        if not command:
            return
            
        try:
            parts = shlex.split(command)
            cmd = parts[0]
            args = parts[1:] if len(parts) > 1 else []
            
            if cmd == "exit":
                self.root.quit()
            elif cmd == "ls":
                self.print_output(f"ls команда с аргументами: {args}\n")
            elif cmd == "cd":
                self.print_output(f"cd команда с аргументами: {args}\n")
            else:
                self.print_output(f"Команда '{cmd}' не найдена\n")
                
        except Exception as e:
            self.print_output(f"Ошибка: {str(e)}\n")
            
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

if __name__ == "__main__":
    app = TerminalEmulator()
    app.run()