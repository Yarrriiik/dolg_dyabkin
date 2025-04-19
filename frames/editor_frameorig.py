import re
import tkinter as tk
from tkinter import messagebox as mb
from PIL import Image, ImageTk, ImageFilter, ImageDraw


class EditorFrame(tk.Frame):
    """
    Фрейм для отображения и редактирования изображения.
    """

    def __init__(self, parent):
        """
        Инициализация фрейма и кнопок.
        """

        super().__init__(parent)
        self.parent = parent

        self.image_label = tk.Label(self)
        self.image_label.pack()
        self.original = parent.image.copy().convert('RGB')
        image = self.original.copy()
        image.load()
        self.image = image

        original_button = tk.Button(self, text='Оригинал', command=self.revert)
        original_button.pack()

        channels_frame = tk.Frame(self)
        red_button = tk.Button(channels_frame, text='Красный канал', command=lambda: self.channel('R'))
        green_button = tk.Button(channels_frame, text='Зелёный канал', command=lambda: self.channel('G'))
        blue_button = tk.Button(channels_frame, text='Синий канал', command=lambda: self.channel('B'))
        red_button.pack(side='left')
        green_button.pack(side='left')
        blue_button.pack(side='left')
        channels_frame.pack()

        grayscale_button = tk.Button(self, text='Оттенки серого', command=self.grayscale)
        grayscale_button.pack()

        averaging_frame = tk.Frame(self)
        averaging_label = tk.Label(averaging_frame, text='Размер усреднения')
        self.averaging_scale = tk.Scale(averaging_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        averaging_button = tk.Button(averaging_frame, text='Усреднить', command=self.average)
        averaging_label.pack(side='left')
        self.averaging_scale.pack(side='left')
        averaging_button.pack(side='left')
        averaging_frame.pack()

        width, height = self.original.width, self.original.height
        self.rect_entry = tk.Entry(self)
        rect_label = tk.Label(self, text='Координаты прямоугольника: x1,y1,x2,y2')
        rect_otherlabel = tk.Label(self, text=f'x - [0; {width}], y - [0; {height}]')
        self.rect_entry.pack()
        rect_label.pack()
        rect_otherlabel.pack()

        draw_button = tk.Button(self, text='Нарисовать', command=self.draw_rect)
        draw_button.pack()

        close_button = tk.Button(self, text='Закрыть окно', command=self.parent.destroy)
        close_button.pack()

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
        Показать указанный цветовой канал.
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
        Перевести изображение в градации серого.
        """

        self.image = self.original.convert('L')
        self.redraw_image()

    def average(self):
        """
        Применить усреднение (блюр).
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
