import tkinter as tk
import frames


class App(tk.Tk):
    """
    Главное окно приложения.

    Атрибуты:
        current_frame: текущий отображаемый фрейм
        edited_image: редактируемое изображение
    """

    def __init__(self):
        """Инициализация окна."""
        super().__init__()
        self.title('Редактор')

        self.current_frame = None
        self.edited_image = None

        self.show_menu()
        self.recenter()

    def recenter(self):
        """Центрирует окно на экране."""
        width, height = self.get_required_size()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')

    def resize(self):
        """Изменяет размер окна."""
        width, height = self.get_required_size()
        self.geometry(f'{width}x{height}')

    def get_required_size(self):
        """Возвращает нужный размер окна."""
        self.update_idletasks()
        if self.current_frame is None:
            width = self.winfo_width()
            height = self.winfo_height()
        else:
            width = self.current_frame.winfo_reqwidth()
            height = self.current_frame.winfo_reqheight()
        return (width, height)

    def show_menu(self):
        """Показать главное меню."""
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frames.MenuFrame(self)
        self.current_frame.pack()
        self.recenter()

    def show_camera(self):
        """Показать камеру."""
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frames.CameraFrame(self)
        self.current_frame.pack()
        self.recenter()

    def show_editor(self):
        """Показать редактор."""
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frames.EditorFrame(self)
        self.current_frame.pack()
        self.recenter()


