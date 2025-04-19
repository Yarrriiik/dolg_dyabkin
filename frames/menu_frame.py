import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import PIL
from PIL import Image


class MenuFrame(tk.Frame):
    """
    Меню выбора изображения.
    """

    FILE_TYPES = (
        ('файлы png', '*.png'),
        ('файлы jpg', '*.jpg')
    )

    def __init__(self, parent):
        """
        Создаёт меню с кнопками.
        """
        super().__init__(parent)
        self.parent = parent

        file_button = tk.Button(self, text='Выбрать файл с изображением',
                                command=self.pick_file)
        camera_button = tk.Button(self, text='Использовать камеру',
                                  command=parent.show_camera)
        close_button = tk.Button(self, text='Закрыть окно', command=self.parent.destroy)
        file_button.pack()
        camera_button.pack()
        close_button.pack()

    def pick_file(self):
        """
        Открывает диалог выбора файла.
        """
        filename = fd.askopenfilename(filetypes=MenuFrame.FILE_TYPES)
        if not filename.strip():
            return

        try:
            image = Image.open(filename)
            self.parent.image = image
            self.parent.show_editor()
        except (FileNotFoundError, PIL.UnidentifiedImageError):
            mb.showerror(title='Ошибка', message='Не удалось найти файл или содержимое файла повреждено.')
