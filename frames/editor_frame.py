import re
import tkinter as tk
from tkinter import messagebox as mb
from PIL import Image, ImageTk, ImageFilter, ImageDraw


class EditorFrame(tk.Frame):
    """
    Фрейм для отображения изображения и инструментов редактирования.
    """

    def __init__(self, parent):
        """
        Инициализация интерфейса редактирования.
        """
        super().__init__(parent)
        self.parent = parent

        # Фреймы слева и справа
        left_frame = tk.Frame(self)
        left_frame.pack(side='left', padx=10, pady=10)

        right_frame = tk.Frame(self)
        right_frame.pack(side='left', padx=10, pady=10, fill='y')

        # Левый — изображение
        self.image_label = tk.Label(left_frame)
        self.image_label.pack()
        self.original = parent.image.copy().convert('RGB')
        image = self.original.copy()
        image.load()
        self.image = image

        # Правый — кнопки
        original_button = tk.Button(right_frame, text='Оригинал', command=self.revert)
        original_button.pack(pady=4)

        # Каналы
        channels_frame = tk.LabelFrame(right_frame, text='Цветовые каналы')
        channels_frame.pack(pady=4)
        tk.Button(channels_frame, text='Красный', command=lambda: self.channel('R')).pack(fill='x')
        tk.Button(channels_frame, text='Зелёный', command=lambda: self.channel('G')).pack(fill='x')
        tk.Button(channels_frame, text='Синий', command=lambda: self.channel('B')).pack(fill='x')

        # Оттенки серого
        grayscale_button = tk.Button(right_frame, text='Оттенки серого', command=self.grayscale)
        grayscale_button.pack(pady=4, fill='x')

        # Усреднение
        averaging_frame = tk.LabelFrame(right_frame, text='Усреднение')
        averaging_frame.pack(pady=4, fill='x')
        tk.Label(averaging_frame, text='Размер').pack()
        self.averaging_scale = tk.Scale(averaging_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.averaging_scale.pack()
        tk.Button(averaging_frame, text='Усреднить', command=self.average).pack()

        # Прямоугольник
        rect_frame = tk.LabelFrame(right_frame, text='Прямоугольник')
        rect_frame.pack(pady=4, fill='x')
        width, height = self.original.width, self.original.height
        tk.Label(rect_frame, text='x1,y1,x2,y2').pack()
        self.rect_entry = tk.Entry(rect_frame)
        self.rect_entry.pack()
        tk.Label(rect_frame, text=f'x - [0; {width}], y - [0; {height}]').pack()
        tk.Button(rect_frame, text='Нарисовать', command=self.draw_rect).pack(pady=4)

        # Кнопка закрытия
        close_button = tk.Button(right_frame, text='Закрыть окно', command=self.parent.destroy)
        close_button.pack(pady=10)

        # Отображение изображения
        self.redraw_image()

    def redraw_image(self):
        """
        Обновить изображение на экране.
        """
        safe_width = int(self.parent.winfo_screenwidth() * 0.5)
        safe_height = int(self.parent.winfo_screenheight() * 0.5)

        resized_image = self.image.copy()
        resized_image.thumbnail((safe_width, safe_height))
        tk_image = ImageTk.PhotoImage(resized_image)
        self.image_label.image = tk_image
        self.image_label.configure(image=tk_image)

    def channel(self, channel_name):
        """
        Показать выбранный канал ('R', 'G' или 'B').
        """
        blank = Image.new('L', self.original.size, 0)
        red = self.original.getchannel('R') if channel_name == 'R' else blank
        green = self.original.getchannel('G') if channel_name == 'G' else blank
        blue = self.original.getchannel('B') if channel_name == 'B' else blank

        self.image = Image.merge('RGB', (red, green, blue))
        self.redraw_image()

    def revert(self):
        """
        Вернуть оригинал изображения.
        """
        self.image = self.original.copy()
        self.redraw_image()

    def grayscale(self):
        """
        Преобразовать в оттенки серого.
        """
        self.image = self.original.convert('L')
        self.redraw_image()

    def average(self):
        """
        Применить фильтр усреднения.
        """
        self.image = self.original.filter(ImageFilter.BoxBlur(radius=self.averaging_scale.get()))
        self.redraw_image()

    def draw_rect(self):
        """
        Нарисовать синий прямоугольник по координатам.
        """
        pattern = r'^(\d+),(\d+),(\d+),(\d+)$'
        match = re.match(pattern, self.rect_entry.get())
        is_good = True
        if not match:
            is_good = False
        else:
            x1 = int(match.group(1))
            y1 = int(match.group(2))
            x2 = int(match.group(3))
            y2 = int(match.group(4))

            if not 0 <= x1 <= self.image.width or not 0 <= x2 <= self.image.width or \
                    not 0 <= y1 <= self.image.height or not 0 <= y2 <= self.image.height:
                is_good = False
            if x1 >= x2 or y1 >= y2:
                is_good = False

        if not is_good:
            mb.showerror(title='Ошибка', message='Значения введены неверно')
            return

        self.image = self.original.copy()
        draw = ImageDraw.Draw(self.image)

        draw.rectangle((x1, y1, x2, y2), fill='blue')
        self.redraw_image()
