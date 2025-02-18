import tkinter as tk



class MenuButtonsHandler:

    def __init__(self, app: tk.Tk) -> None:
        self.app = app


    # --- IMAGE SUBMENU ---

    def image_show(self):
        if self.app.selected_image_path:
            self.app.frames['ImageFrame'].update(self.app.selected_image_path)

    def image_close(self):
        self.app.frames['BlankFrame'].update()


    # --- PROCESSING SUBMENU ---

    def processing_fft(self):
        if self.app.selected_image_path:

            fft_frame = self.app.frames['FFTFrame']
            fft_frame.slider.set(1)
            fft_frame.output_only_btn.deselect()
            fft_frame.zoom_slider.set(1)

            mask_frame = self.app.frames['MaskFrame']
            mask_frame.slider.set(30)

            fft_frame.update(self.app.selected_image_path)