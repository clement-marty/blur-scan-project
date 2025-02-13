import tkinter as tk
from tkinter import filedialog
from PIL import Image



def _image_path_display(image_path: str, max_length = 80) -> str:
    l = image_path.split('/')
    res = ''
    
    i = len(l) - 1
    while i >= 0 and len(res) + len(l[i]) <= max_length:
        res = l[i] + '/' + res
        i -= 1
    return res[:-1]



def blank_frame_file_dialog(app: tk.Tk):
    image_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png *.jpg *.jpeg *.tif')])
    if image_path:
        app.selected_image_path = image_path
        image_show_btn(app)



def image_show_btn(app: tk.Tk):
    if app.selected_image_path is None:
        return
    
    app.frames['ImageFrame'].update(app.selected_image_path)
    app.show_frame('ImageFrame')
    app.header_title.config(text='Selected Image')
    app.header_image_path.config(text=_image_path_display(app.selected_image_path))

def image_close_btn(app: tk.Tk):
    app.selected_image_path = None
    app.show_frame('BlankFrame')
    app.header_title.config(text='')
    app.header_image_path.config(text='')



def processing_fft_btn(app: tk.Tk):
    if app.selected_image_path is None:
        return

    app.frames['FFTFrame'].gamma_slider.set(1)
    app.frames['FFTFrame'].output_only_btn.deselect()
    app.frames['FFTFrame'].zoom_slider.set(1)
    app.header_title.config(text='Fourier Transform (FFT)')
    app.show_frame('FFTFrame')
    processing_fft_update_btn(app)

def processing_fft_update_btn(app: tk.Tk):
    app.frames['FFTFrame'].update(app.selected_image_path)

def processing_fft_mask_btn(app: tk.Tk):
    dft = app.frames['FFTFrame'].dft
    app.frames['MaskFrame'].radius_slider.set(30)
    app.header_title.config(text='Inverse Fourier Transform (IFFT) - Mask Selection')
    app.show_frame('MaskFrame')
    app.frames['MaskFrame'].update(dft)

def processing_fft_ifft_btn(app: tk.Tk):
    dft = app.frames['MaskFrame'].masked_dft
    mask_radius = app.frames['MaskFrame'].mask_radius
    app.header_title.config(text='Inverse Fourier Transform (IFFT)')
    app.show_frame('IFFTFrame')
    app.frames['IFFTFrame'].update(dft, mask_radius)

def processing_fft_save_btn(app: tk.Tk):
    file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('Image Files', '*.png')])
    if file_path:
        idft = app.frames['IFFTFrame'].idft
        image = Image.fromarray(idft).convert('RGB')
        image.save(file_path)