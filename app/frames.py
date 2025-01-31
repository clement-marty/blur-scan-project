import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

from scripts import fft
from .button_handler import blank_frame_file_dialog, processing_fft_update_btn



class CustomFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.color_palette = self.master.master.color_palette
        self.config(bg=self.color_palette['background'])

    def get_image_widget(self, image_path=None, image: np.ndarray=None, relwidth=1, relheight=1, zoom=1, grayscale=True):
        if image_path:
            im = Image.open(image_path)
        elif image is not None:
            im = Image.fromarray(image)
        if grayscale:
            im = im.convert('L')
        
        # Apply zoom
        w, h = im.size
        im = im.resize((int(im.width*zoom), int(im.height*zoom)), resample=Image.Resampling.NEAREST)
        new_w, new_h = im.size
        im = im.crop((new_w//2-w//2, new_h//2-h//2, new_w//2+w//2, new_h//2+h//2))

        scale_w = self.winfo_width()*relwidth/im.width
        scale_h = self.winfo_height()*relheight/im.height

        if zoom == 1:
            scaling_factor = min(scale_w, scale_h)
            im = im.resize((int(im.width*scaling_factor), int(im.height*scaling_factor)), resample=Image.Resampling.NEAREST)
        else:
            im = im.resize((int(im.width*scale_w), int(im.height*scale_h)), resample=Image.Resampling.NEAREST)

        imtk = ImageTk.PhotoImage(im)
        widget = tk.Label(self, image=imtk, bg=self.color_palette['background'])
        widget.image = imtk
        return widget



class BlankFrame(CustomFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        popup_frame = tk.Frame(self, bg=self.color_palette['popup'])
        popup_frame.place(relx=.25, rely=.2, relwidth=.5, relheight=.3)

        label1 = tk.Label(popup_frame, text='Welcome!', font=("Arial", 20, 'bold'), bg=self.color_palette['popup'], anchor='w')
        label2 = tk.Label(popup_frame, text='Start by uploading an image with the button below.', font=("Arial", 12), bg=self.color_palette['popup'], anchor='w')
        label1.place(relx=.1, rely=.1, relwidth=.8, relheight=.2)
        label2.place(relx=.1, rely=.3, relwidth=.8, relheight=.2)

        button = tk.Button(
            popup_frame,
            text='Upload Image',
            font=("Arial", 15, "bold"),
            bd=0,
            bg=self.color_palette['popup'],
            cursor='hand2',
            activebackground=self.color_palette['header'],
            command=lambda: blank_frame_file_dialog(self.master.master)
        )
        button.place(relx=.3, rely=.65, relwidth=.4, relheight=.2)



class ImageFrame(CustomFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

    def update(self, image_path):
        image_widget = self.get_image_widget(image_path=image_path, relwidth=.9, relheight=.9, grayscale=False)
        image_widget.place(relx=.05, rely=.05, relwidth=.9, relheight=.9)



class FFTFrame(CustomFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.settings_menu = tk.Frame(self, bg=self.color_palette['popup'])
        self.settings_menu.place(relx=0, rely=.8, relwidth=1, relheight=.2)

        gamma_label = tk.Label(self.settings_menu, text='Gamma:', font=("Arial", 12), bg=self.color_palette['popup'])
        gamma_label.place(relx=.05, rely=.3, anchor='w')
        self.gamma_slider = tk.Scale(
            self.settings_menu,
            from_=.5,
            to=1,
            resolution=.05,
            orient='horizontal',
            bg=self.color_palette['popup'],
            bd=0,
            cursor='hand2',
            activebackground=self.color_palette['header'],
            highlightthickness=0,
            troughcolor=self.color_palette['header']
        )
        self.gamma_slider.set(1)
        self.gamma_slider.place(relx=.2, rely=.1, relwidth=.5, relheight=.4)

        self.output_only_value = tk.BooleanVar()
        self.output_only_btn = tk.Checkbutton(
            self.settings_menu,
            text='Output only',
            variable=self.output_only_value,
            command=lambda: processing_fft_update_btn(self.master.master),
            font=("Arial", 12),
            bg=self.color_palette['popup'],
            selectcolor=self.color_palette['header'],
            highlightthickness=0
        )
        self.output_only_btn.place(relx=.05, rely=.6, anchor='w')

        zoom_label = tk.Label(self.settings_menu, text='Zoom:', font=("Arial", 12), bg=self.color_palette['popup'])
        zoom_label.place(relx=.05, rely=.8, anchor='w')
        self.zoom_slider = tk.Scale(
            self.settings_menu,
            from_=1,
            to=10,
            resolution=.5,
            orient='horizontal',
            bg=self.color_palette['popup'],
            bd=0,
            cursor='hand2',
            activebackground=self.color_palette['header'],
            highlightthickness=0,
        )
        self.zoom_slider.set(1)
        self.zoom_slider.config(state='disabled', troughcolor=self.color_palette['background'])
        self.zoom_slider.place(relx=.2, rely=.6, relwidth=.5, relheight=.4)

        update_btn = tk.Button(self.settings_menu, text='Update', font=("Arial", 12), bd=0, bg=self.color_palette['popup'], cursor='hand2', activebackground=self.color_palette['header'])
        update_btn.config(command=lambda: processing_fft_update_btn(self.master.master))
        update_btn.place(relx=.75, rely=.1, relwidth=.2, relheight=.35)

        inverse_btn = tk.Button(self.settings_menu, text='Inverse FFT', font=("Arial", 12), bd=0, bg=self.color_palette['popup'], cursor='hand2', activebackground=self.color_palette['header'])
        inverse_btn.place(relx=.75, rely=.55, relwidth=.2, relheight=.35)


    def update(self, image_path):

        self.dft = fft.dft(image_path, gamma=self.gamma_slider.get())

        empty_widget = tk.Label(self, bg=self.color_palette['background'])
        empty_widget.place(relx=.05, rely=.05, relwidth=.9, relheight=.7)

        if not self.output_only_value.get():
            self.zoom_slider.set(1)
            self.zoom_slider.config(state='disabled', troughcolor=self.color_palette['background'])

            image_widget = self.get_image_widget(image_path=image_path, relwidth=.425, relheight=.7)
            dft_widget = self.get_image_widget(image=self.dft, relwidth=.425, relheight=.7, zoom=self.zoom_slider.get())

            image_widget.place(relx=.05, rely=.05, relwidth=.425, relheight=.7)
            dft_widget.place(relx=.525, rely=.05, relwidth=.425, relheight=.7)

        else:
            self.zoom_slider.config(state='normal', troughcolor=self.color_palette['header'])

            dft_widget = self.get_image_widget(image=self.dft, relwidth=.9, relheight=.7, zoom=self.zoom_slider.get())
            dft_widget.place(relx=.05, rely=.05, relwidth=.9, relheight=.7)