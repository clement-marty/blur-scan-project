import numpy as np
import tkinter as tk
from PIL import Image, ImageTk



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

        
        scale_w = self.winfo_width()*relwidth/im.width
        scale_h = self.winfo_height()*relheight/im.height

        scaling_factor = min(scale_w, scale_h)
        im = im.resize((int(im.width*scaling_factor*zoom), int(im.height*scaling_factor*zoom)), resample=Image.Resampling.NEAREST)

        crop_box = (
            im.width//2-self.winfo_width()*relwidth//2,
            im.height//2-self.winfo_height()*relheight//2,
            im.width//2+self.winfo_width()*relwidth//2,
            im.height//2+self.winfo_height()*relheight//2
        )
        # Prevent cropping outside of image bounds
        if crop_box[0] < 0:
            crop_box = (0, crop_box[1], im.width, crop_box[3])
        if crop_box[1] < 0:
            crop_box = (crop_box[0], 0, crop_box[2], im.height)
        im = im.crop(crop_box)

        imtk = ImageTk.PhotoImage(im)
        widget = tk.Label(self, image=imtk, bg=self.color_palette['background'])
        widget.image = imtk
        return widget
    
    def update(self, *args, **kwargs):
        raise NotImplementedError('This method must be implemented in the subclass.')




class ResultImageDisplay(CustomFrame):

    def __init__(self, parent, controller, back_btn_command, save_btn_command):
        super().__init__(parent, controller)

        self.settings_menu = tk.Frame(self, bg=self.color_palette['background'])
        self.settings_menu.place(relx=0, rely=.8, relwidth=1, relheight=.2)

        back_btn = tk.Button(self.settings_menu, text='Back', font=("Arial", 12), bd=0, bg=self.color_palette['popup'], cursor='hand2', activebackground=self.color_palette['header'])
        back_btn.config(command=back_btn_command)
        back_btn.place(relx=.25, rely=.3, relwidth=.2, relheight=.4)

        save_btn = tk.Button(self.settings_menu, text='Save', font=("Arial", 12), bd=0, bg=self.color_palette['popup'], cursor='hand2', activebackground=self.color_palette['header'])
        save_btn.config(command=save_btn_command)
        save_btn.place(relx=.55, rely=.3, relwidth=.2, relheight=.4)


class SingleImageDisplay(CustomFrame):

    def __init__(self, parent, controller, 
                 btn1_label: str, btn1_command: callable,
                 btn2_label: str, btn2_command: callable,
                 slider_label: str = None, slider_range: tuple[int, int, int, int] = None,
                 sliders_command: callable = None):
        super().__init__(parent, controller)

        self.settings_menu = tk.Frame(self, bg=self.color_palette['popup'])
        self.settings_menu.place(relx=0, rely=.8, relwidth=1, relheight=.2)

        if slider_label and slider_range:
            slider_label = tk.Label(self.settings_menu, text=slider_label, font=("Arial", 12), bg=self.color_palette['popup'])
            slider_label.place(relx=.05, rely=.3, anchor='w')
            self.slider = tk.Scale(
                self.settings_menu,
                from_=slider_range[0],
                to=slider_range[1],
                resolution=slider_range[2],
                orient='horizontal',
                bg=self.color_palette['popup'],
                bd=0,
                cursor='hand2',
                activebackground=self.color_palette['header'],
                highlightthickness=0,
                troughcolor=self.color_palette['header']
            )
            self.slider.set(slider_range[3])
            self.slider.place(relx=.2, rely=.1, relwidth=.5, relheight=.4)
            self.slider.bind("<ButtonRelease-1>", sliders_command)

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
            troughcolor=self.color_palette['header']
        )
        self.zoom_slider.set(1)
        self.zoom_slider.place(relx=.2, rely=.6, relwidth=.5, relheight=.4)

        self.zoom_slider.bind("<ButtonRelease-1>", sliders_command)

        btn1 = tk.Button(self.settings_menu, text=btn1_label, font=("Arial", 12), bd=0, bg=self.color_palette['popup'], cursor='hand2', activebackground=self.color_palette['header'], borderwidth=1)
        btn1.config(command=btn1_command)
        btn1.place(relx=.75, rely=.1, relwidth=.2, relheight=.35)

        btn2 = tk.Button(self.settings_menu, text=btn2_label, font=("Arial", 12), bd=0, bg=self.color_palette['popup'], cursor='hand2', activebackground=self.color_palette['header'], borderwidth=1)
        btn2.config(command=btn2_command)
        btn2.place(relx=.75, rely=.55, relwidth=.2, relheight=.35)



class DoubleImageDisplay(CustomFrame):

    def __init__(self, parent, controller,
                 btn1_label: str, btn1_command: callable,
                 btn2_label: str = None, btn2_command: callable = None,
                 slider_label: str = None, slider_range: tuple[int, int, int, int] = None,
                 inputs_command: callable = None):
        super().__init__(parent, controller)

        self.settings_menu = tk.Frame(self, bg=self.color_palette['popup'])
        self.settings_menu.place(relx=0, rely=.8, relwidth=1, relheight=.2)

        if slider_label and slider_range:
            slider_label = tk.Label(self.settings_menu, text=slider_label, font=("Arial", 12), bg=self.color_palette['popup'])
            slider_label.place(relx=.05, rely=.3, anchor='w')
            self.slider = tk.Scale(
                self.settings_menu,
                from_=slider_range[0],
                to=slider_range[1],
                resolution=slider_range[2],
                orient='horizontal',
                bg=self.color_palette['popup'],
                bd=0,
                cursor='hand2',
                activebackground=self.color_palette['header'],
                highlightthickness=0,
                troughcolor=self.color_palette['header']
            )
            self.slider.set(slider_range[3])
            self.slider.place(relx=.2, rely=.1, relwidth=.5, relheight=.4)
            self.slider.bind("<ButtonRelease-1>", inputs_command)

        self.output_only_value = tk.BooleanVar()
        self.output_only_btn = tk.Checkbutton(
            self.settings_menu,
            text='Output only',
            variable=self.output_only_value,
            command=inputs_command,
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
        self.zoom_slider.bind("<ButtonRelease-1>", inputs_command)

        btn1 = tk.Button(self.settings_menu, text=btn1_label, font=("Arial", 12), bd=0, bg=self.color_palette['popup'], cursor='hand2', activebackground=self.color_palette['header'], borderwidth=1)
        btn1.config(command=btn1_command)
        btn1.place(relx=.75, rely=.1, relwidth=.2, relheight=.35)

        if btn2_label and btn2_command:
            btn2 = tk.Button(self.settings_menu, text=btn2_label, font=("Arial", 12), bd=0, bg=self.color_palette['popup'], cursor='hand2', activebackground=self.color_palette['header'], borderwidth=1)
            btn2.config(command=btn2_command)
            btn2.place(relx=.75, rely=.55, relwidth=.2, relheight=.35)
