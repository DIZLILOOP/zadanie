import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
import sys
import shlex
import subprocess
import argparse

class TerminalEmulator:
    def __init__(self, vfs_path=None, startup_script=None):
        self.vfs_path = vfs_path or os.getcwd()
        self.startup_script = startup_script
        self.current_dir = self.vfs_path
        
        # Создаем главное окно
        self.root = tk.Tk()
        self.setup_gui()
        
        # Отладочный вывод параметров
        self.debug_output(f"VFS Path: {self.vfs_path}")
        self.debug_output(f"Startup Script: {self.startup_script}")
        self.debug_output(f"Current Directory: {self.current_dir}")
        
        # Если указан стартовый скрипт, выполняем его
        if self.startup_script and os.path.exists(self.startup_script):
            self.execute_startup_script()
        
    def setup_gui(self):
        """Настройка графического интерфейса"""
        # Получаем данные ОС для заголовка
        username = os.getenv('USERNAME') or os.getenv('USER')
        hostname = os.getenv('COMPUTERNAME') or os.uname().nodename
        
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
            insertbackground='white',
            font=('Courier New', 10)
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_entry.bind('<Return>', self.execute_command)
        self.input_entry.focus()
        
        # Выводим приветственное сообщение
        self.print_output("Добро пожаловать в эмулятор терминала!\n")
        self.print_output("Доступные команды: ls, cd, exit\n")
        
    def debug_output(self, message):
        """Вывод отладочной информации"""
        print(f"[DEBUG] {message}")
        
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
        
        # Показываем введенную команду
        self.print_output(f"\n{self.prompt_label.cget('text')}{command}\n")
        
        if not command:
            return
            
        try:
            # Парсим команду с учетом кавычек
            parts = shlex.split(command)
            cmd = parts[0]
            args = parts[1:] if len(parts) > 1 else []
            
            if cmd == "exit":
                self.root.quit()
                
            elif cmd == "ls":
                self.cmd_ls(args)
                
            elif cmd == "cd":
                self.cmd_cd(args)
                
            else:
                self.print_output(f"Команда '{cmd}' не найдена\n")
                
        except Exception as e:
            self.print_output(f"Ошибка: {str(e)}\n")
            
    def cmd_ls(self, args):
        """Команда ls - заглушка"""
        self.print_output(f"Команда: ls\n")
        self.print_output(f"Аргументы: {args}\n")
        self.print_output("file1.txt  file2.txt  directory1/\n")
        
    def cmd_cd(self, args):
        """Команда cd - заглушка"""
        self.print_output(f"Команда: cd\n")
        self.print_output(f"Аргументы: {args}\n")
        
        if not args:
            # Возврат в домашнюю директорию
            self.current_dir = self.vfs_path
        else:
            # Смена директории
            new_dir = args[0]
            if new_dir == "..":
                # Переход на уровень выше
                self.current_dir = os.path.dirname(self.current_dir)
            else:
                # Переход в указанную директорию
                self.current_dir = os.path.join(self.current_dir, new_dir)
                
        self.print_output(f"Текущая директория: {self.current_dir}\n")
        
    def execute_startup_script(self):
        """Выполнение стартового скрипта"""
        self.print_output(f"\n=== Выполнение стартового скрипта: {self.startup_script} ===\n")
        
        try:
            with open(self.startup_script, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
            for line_num, line in enumerate(lines, 1):
                command = line.strip()
                if command and not command.startswith('#'):
                    # Показываем команду из скрипта
                    self.print_output(f"[Скрипт строка {line_num}] {command}\n")
                    
                    # Имитируем выполнение команды
                    parts = shlex.split(command)
                    cmd = parts[0]
                    args = parts[1:] if len(parts) > 1 else []
                    
                    if cmd == "exit":
                        self.print_output("Выход из эмулятора\n")
                        return
                    elif cmd == "ls":
                        self.cmd_ls(args)
                    elif cmd == "cd":
                        self.cmd_cd(args)
                    else:
                        self.print_output(f"Ошибка: команда '{cmd}' не найдена\n")
                        break
                        
        except Exception as e:
            self.print_output(f"Ошибка выполнения скрипта: {str(e)}\n")
            
        self.print_output("=== Завершение выполнения стартового скрипта ===\n")
        
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

def create_test_scripts():
    """Создание тестовых скриптов"""
    scripts_dir = "test_scripts"
    os.makedirs(scripts_dir, exist_ok=True)
    
    # Скрипт 1: Базовое тестирование
    script1_content = """# Тестовый скрипт 1 - Базовые команды
ls
cd test_directory
ls
cd ..
ls
"""
    
    # Скрипт 2: Тестирование с кавычками
    script2_content = """# Тестовый скрипт 2 - Команды с кавычками
ls -l
cd "directory with spaces"
ls
cd ..
"""
    
    # Скрипт 3: Тестирование ошибок
    script3_content = """# Тестовый скрипт 3 - Обработка ошибок
ls
unknown_command
ls  # Эта команда не выполнится из-за предыдущей ошибки
"""
    
    scripts = {
        "test_basic.txt": script1_content,
        "test_quotes.txt": script2_content,
        "test_errors.txt": script3_content
    }
    
    for filename, content in scripts.items():
        filepath = os.path.join(scripts_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Создан скрипт: {filepath}")
    
    return scripts_dir

def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(description='Эмулятор терминала')
    parser.add_argument('--vfs-path', help='Путь к физическому расположению VFS')
    parser.add_argument('--startup-script', help='Путь к стартовому скрипту')
    
    args = parser.parse_args()
    
    # Создаем тестовые скрипты
    scripts_dir = create_test_scripts()
    
    # Запускаем эмулятор
    app = TerminalEmulator(
        vfs_path=args.vfs_path,
        startup_script=args.startup_script
    )
    app.run()

if __name__ == "__main__":
    main()