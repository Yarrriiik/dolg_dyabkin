import tkinter as tk
from tkinter import messagebox as mb
import cv2
from PIL import Image, ImageTk


class CameraFrame(tk.Frame):
    """
    Фрейм с камерой.

    Атрибуты:
        parent — главное окно
        video_capture — объект камеры
        video_label — метка для вывода видео
    """

    def __init__(self, parent):
        """Инициализация фрейма и камеры."""
        super().__init__(parent)
        self.parent = parent

        for i in range(2, -1, -1):
            capture = cv2.VideoCapture(i)
            if capture.isOpened():
                self.video_capture = capture
                break
        else:
            mb.showerror(title='Ошибка', message='Не удалось определить камеру')
            self.parent.show_menu()

        self.video_label = tk.Label(self)
        self.video_label.pack()

        button_frame = tk.Frame(self)
        cancel_button = tk.Button(button_frame, text='Назад', command=self.parent.show_menu)
        cancel_button.pack(side='left')
        submit_button = tk.Button(button_frame, text='Сделать снимок', command=self.take_photo)
        submit_button.pack(side='left')
        button_frame.pack()

        close_button = tk.Button(self, text='Закрыть окно', command=self.parent.destroy)
        close_button.pack()

        self.update_camera()

    def get_image(self):
        """Сделать снимок с камеры."""
        _, frame = self.video_capture.read()
        cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        image = Image.fromarray(cv_image)
        return image

    def update_camera(self):
        """Обновить изображение с камеры."""
        image = self.get_image()
        tk_image = ImageTk.PhotoImage(image)
        self.video_label.image = tk_image
        self.video_label.configure(image=tk_image)
        self.video_label.after(10, self.update_camera)

    def take_photo(self):
        """Сделать фото и перейти в редактор."""
        image = self.get_image()
        self.parent.image = image
        self.parent.show_editor()

    def destroy(self):
        """Освободить камеру и закрыть фрейм."""
        self.video_capture.release()
        super().destroy()
