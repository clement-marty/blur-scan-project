import tkinter as tk
from tkinter import filedialog



def blank_frame_file_dialog(app: tk.Tk):
    image_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png *.jpg *.jpeg')])
    if image_path:
        app.selected_image_path = image_path
        image_show_btn(app)



def image_show_btn(app: tk.Tk):
    if app.selected_image_path is None:
        return
    
    app.frames['ImageFrame'].update(app.selected_image_path)
    app.show_frame('ImageFrame')
    app.header_title.config(text='Selected Image')
    app.header_image_path.config(text=app.selected_image_path)

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