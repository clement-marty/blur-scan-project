import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image

from scripts import fourier_transform as ft
from . import custom_frames as cf



class BlankFrame(cf.CustomFrame):

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
            borderwidth=1,
            command=self.upload_btn_command
        )
        button.place(relx=.3, rely=.65, relwidth=.4, relheight=.2)

    def update(self):
        self.master.master.selected_image_path = None
        self.master.master.header_title.config(text='')
        self.master.master.header_image_path.config(text='')
        self.tkraise()

    def upload_btn_command(self):
        image_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png *.jpg *.jpeg *.tif')])
        app = self.master.master
        if image_path:
            app.selected_image_path = image_path

            app.frames['ImageFrame'].update(app.selected_image_path)
            app.header_image_path.config(text=self._image_path_formatter(app.selected_image_path))
    
    def _image_path_formatter(self, image_path: str, max_length = 80) -> str:
        l = image_path.split('/')
        res = ''
        
        i = len(l) - 1
        while i >= 0 and len(res) + len(l[i]) <= max_length:
            res = l[i] + '/' + res
            i -= 1
        return res[:-1]



class ImageFrame(cf.CustomFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

    def update(self, image_path):
        self.master.master.header_title.config(text='Selected Image')
        self.tkraise()

        image_widget = self.get_image_widget(image_path=image_path, relwidth=.9, relheight=.9, grayscale=False)
        image_widget.place(relx=.05, rely=.05, relwidth=.9, relheight=.9)




class FFTFrame(cf.DoubleImageDisplay):

    def __init__(self, parent, controller):
        super().__init__(parent, controller,
            btn1_label='Inverse FFT', btn1_command=self.inverse_fft_btn_command,
            slider_label='Gamma:', slider_range=(1, 2, .05, 1),
            inputs_command=lambda *_: self.update(self.master.master.selected_image_path)
        )

    def update(self, image_path):
        self.master.master.header_title.config(text='Foourier Transform (FFT)')
        self.tkraise()

        self.dft = ft.dft(image_path, gamma=self.slider.get())[1]

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

    def inverse_fft_btn_command(self):
        self.master.master.frames['MaskFrame'].update(self.dft)




class MaskFrame(cf.SingleImageDisplay):

    def __init__(self, parent, controller):
        super().__init__(parent, controller,
            btn1_label='Confirm', btn1_command=self.confirm_btn_command,
            btn2_label='Back', btn2_command=self.back_btn_command,
            slider_label='Mask radius (%):', slider_range=(.1, 30, .1, 30),
            sliders_command=lambda _: self.update(self.dft)
        )
        self.dft: np.ndarray = None

    def update(self, dft: np.ndarray):
        self.master.master.header_title.config(text='Inverse Fourier Transform (IFFT) - Mask Selection')
        self.tkraise()

        self.dft = dft

        empty_widget = tk.Label(self, bg=self.color_palette['background'])
        empty_widget.place(relx=.05, rely=.05, relwidth=.9, relheight=.7)

        self.mask_radius = self.slider.get()
        if self.mask_radius != 0:
            # self.masked_dft = mask.apply_mask(dft, mask.gaussian_mask(*dft.shape, self.mask_radius))
            self.masked_dft = ft.apply_circular_mask(dft, self.mask_radius)
        else:
            self.masked_dft = dft
        
        widget = self.get_image_widget(image=self.masked_dft, relwidth=.9, relheight=.7, zoom=self.zoom_slider.get())
        widget.place(relx=.05, rely=.05, relwidth=.9, relheight=.7)

    def confirm_btn_command(self):
        self.master.master.frames['IFFTFrame'].update(self.masked_dft, self.mask_radius)
    
    def back_btn_command(self):
        self.master.master.frames['FFTFrame'].update(self.master.master.selected_image_path)




class IFFTFrame(cf.ResultImageDisplay):
    
    def __init__(self, parent, controller):
        super().__init__(parent, controller,
            back_btn_command=self.back_btn_command,
            save_btn_command=self.save_btn_command
        )

    def update(self, dft: np.ndarray, mask_radius: int):
        self.master.master.header_title.config(text='Inverse Fourier Transform (IFFT)')
        self.tkraise()

        self.mask_radius = mask_radius

        empty_widget = tk.Label(self, bg=self.color_palette['background'])
        empty_widget.place(relx=.05, rely=.05, relwidth=.9, relheight=.7)

        radius_px = int(mask_radius * min(dft.shape) / 100)
        self.idft = ft.wiener_deconvolution(self.master.master.selected_image_path, ft.gaussian_psf(radius_px, 1))

        widget = self.get_image_widget(image=self.idft, relwidth=.9, relheight=.7)
        widget.place(relx=.05, rely=.05, relwidth=.9, relheight=.7)

    def back_btn_command(self):
        self.master.master.frames['MaskFrame'].update(
            dft=self.master.master.frames['FFTFrame'].dft
        )

    def save_btn_command(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('Image Files', '*.png')])
        if file_path:
            image = Image.fromarray(self.idft).convert('RGB')
            image.save(file_path)