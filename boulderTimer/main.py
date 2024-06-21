import tkinter as tk
from tkinter import ttk
import winsound
from datetime import datetime, timedelta

# Функция для воспроизведения звукового файла
def play_sound(sound_name):
    winsound.PlaySound(sound_name, winsound.SND_ASYNC)

# Функция для обновления таймера
def update_timer():
    global minutes, seconds
    if minutes == 1 and seconds == 2:
        play_sound('1min.wav')
    if minutes == 0 and seconds == 12:
        play_sound('ready.wav')
    #if minutes == 0 and seconds == 2:
        #play_sound('gong1.wav')
    #if minutes == 0 and seconds <= 7 and seconds >= 2:
        #play_sound('tic.wav')
    if seconds == 0:
        if minutes == 0:
            minutes = initial_minutes  # Перезадаем минуты
            seconds = initial_seconds  # Перезадаем секунды
            play_sound('gong.wav')
        else:
            minutes -= 1
            seconds = 59
    else:
        seconds -= 1

    timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))
    root.after(1000, update_timer)

# Функция для вычисления оставшегося времени до заданного момента
def start_loop_time(start_hour, start_minute):
    now = datetime.now()
    target_time = now.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)
    if target_time < now:
        target_time += timedelta(days=1)
    remaining_time = target_time - now
    return divmod(remaining_time.seconds, 60)


# Функция для запуска таймера
def start_timer():
    global minutes, seconds, initial_minutes, initial_seconds
    try:
        start_hour = int(hour_time.get())
        start_minute = int(minute_time.get())
        minutes, seconds = start_loop_time(start_hour, start_minute)
        initial_minutes = int(minutes_entry.get())
        initial_seconds = int(seconds_entry.get())
    except ValueError:
        minutes = 5
        seconds = 0
        initial_minutes = 5
        initial_seconds = 0
    color_scheme = color_var.get()
    if color_scheme == "Black on white":
        timer_label.config(fg="black", bg="white")
        root.config(bg="white")
    else:
        timer_label.config(fg="white", bg="black")
        root.config(bg="black")

    start_window.destroy()
    root.deiconify()
    update_timer()


# Обработчик для включения/выключения полноэкранного режима
def toggle_fullscreen(event=None):
    is_fullscreen = root.attributes("-fullscreen")
    root.attributes("-fullscreen", not is_fullscreen)

# Инициализация переменных для времени
minutes = 0
seconds = 0
initial_minutes = 0
initial_seconds = 0

# Создание главного окна
root = tk.Tk()
root.title("Таймер")

# Установка размеров окна в соответствии с разрешением монитора
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("{}x{}".format(screen_width, screen_height))

# Изначально скрываем главное окно
root.withdraw()

# Создание стартового окна
start_window = tk.Toplevel(root)
start_window.title("Настройки таймера")
start_window.geometry("250x200")

# Метки и поля ввода для минут и секунд
tk.Label(start_window, text="Минуты:").grid(row=0, column=0)
minutes_entry = tk.Entry(start_window)
minutes_entry.grid(row=0, column=1)

tk.Label(start_window, text="Секунды:").grid(row=1, column=0)
seconds_entry = tk.Entry(start_window)
seconds_entry.grid(row=1, column=1)

tk.Label(start_window, text="Время начала отсчета").grid(row=2, column=0, columnspan=2)

# Метки и поля ввода для часов и минут начала отсчета
tk.Label(start_window, text="Часы:").grid(row=3, column=0)
hour_time = tk.Entry(start_window)
hour_time.grid(row=3, column=1)

tk.Label(start_window, text="Минуты:").grid(row=4, column=0)
minute_time = tk.Entry(start_window)
minute_time.grid(row=4, column=1)

# Выпадающий список для выбора цветовой схемы
tk.Label(start_window, text="Цветовая схема:").grid(row=5, column=0)
color_var = tk.StringVar()
color_combobox = ttk.Combobox(start_window, textvariable=color_var)
color_combobox['values'] = ("Black on white", "White on black")
color_combobox.current(0)
color_combobox.grid(row=5, column=1)

# Кнопка для запуска таймера
start_button = tk.Button(start_window, text="Старт", command=start_timer)
start_button.grid(row=6, columnspan=2)


# Метка таймера
timer_label = tk.Label(root, text="{}:{}".format(minutes, seconds), font=("Helvetica", screen_width // 4), bg="white")
timer_label.pack(expand=True)



# Установка фонового цвета
root.configure(bg="white")
root.attributes("-fullscreen", True)

# Привязка события нажатия клавиши Escape для переключения полноэкранного режима
root.bind("<Escape>", toggle_fullscreen)


# Запуск главного цикла приложения
root.mainloop()
