import configparser
import tkinter as tk
from tkinter import ttk


from .frames import *
from .button_handler import *


class Application(tk.Tk):

    def __init__(self, config: configparser.ConfigParser) -> None:
        tk.Tk.__init__(self)

        title = config.get('application', 'title')
        subtitle = config.get('application', 'subtitle')
        icon_file = config.get('application', 'icon')
        self.color_palette = {
            'background': config.get('application.color_palette', 'background'),
            'sidebar': config.get('application.color_palette', 'sidebar'),
            'header': config.get('application.color_palette', 'header'),
            'popup': config.get('application.color_palette', 'popup')
        }

        self.title(title)
        self.geometry("1200x800")
        self.resizable(False, False)
        self.config(bg=self.color_palette['background'])


        self.selected_image_path = None

        
        icon = tk.PhotoImage(file=icon_file)
        self.iconphoto(True, icon)

        # Header
        self.header = tk.Frame(self, bg=self.color_palette['header'])
        self.header.place(relx=.2, rely=0, relwidth=.8, relheight=.1)
        self.header_title = tk.Label(
            self.header,
            text='',
            bg=self.color_palette['header'],
            font=('', 20, 'bold'),
            fg='#ffffff'
        )
        self.header_image_path = tk.Label(
            self.header,
            text='',
            bg=self.color_palette['header'],
            font=('', 15),
            fg='#ffffff'
        )
        self.header_title.place(relx=.05, rely=.3, anchor='w')
        self.header_image_path.place(relx=.05, rely=.7, anchor='w')

        # Sidebar
        self.sidebar = tk.Frame(self, bg=self.color_palette['sidebar'])
        self.sidebar.place(relx=0, rely=0, relwidth=.2, relheight=1)

        # Logo
        self.logo_frame = tk.Frame(self.sidebar, bg=self.color_palette['sidebar'])
        self.logo_frame.place(relx=0, rely=0, relwidth=1, relheight=.15)
        self.logo_image = icon.subsample(9)
        logo = tk.Label(self.logo_frame, image=self.logo_image, bg=self.color_palette['sidebar'])
        logo.place(x=5, y=20)

        # Title
        tk.Label(
            self.logo_frame,
            text=title,
            bg=self.color_palette['sidebar'],
            font=('', 15, 'bold'),
            fg='#ffffff'
        ).place(x=55, y=30, anchor='w')
        # Subtitle
        tk.Label(
            self.logo_frame,
            text=subtitle,
            bg=self.color_palette['sidebar'],
            font=('', 12, 'bold'),
            fg='#ffffff'
        ).place(x=55, y=55, anchor='w')


        # SUBMENUS

        self.submenu_frame = tk.Frame(self.sidebar, bg=self.color_palette['sidebar'])
        self.submenu_frame.place(relx=0, rely=.15, relwidth=1, relheight=.85)

        image_submenu = SidebarSubMenu(
            self.submenu_frame,
            'Image',
            ['Show', 'Close Image'],
            self.color_palette['sidebar']
        )
        image_submenu.options['Show'].config(command=lambda: image_show_btn(self))
        image_submenu.options['Close Image'].config(command=lambda: image_close_btn(self))
        image_submenu.place(x=0, y=0, relwidth=1, relheight=.3)


        processing_submenu = SidebarSubMenu(
            self.submenu_frame,
            'Processing',
            ['Fourier Transform (FFT)'],
            self.color_palette['sidebar']
        )
        processing_submenu.options['Fourier Transform (FFT)'].config(command=lambda: processing_fft_btn(self))
        processing_submenu.place(x=0, y=150, relwidth=1, relheight=.3)


        # Page frames
        container = tk.Frame(self)
        container.config(bg=self.color_palette['background'])
        container.place(relx=.2, rely=.1, relwidth=.8, relheight=.9)

        self.frames = {}

        for frame in CustomFrame.__subclasses__():
            self.frames[frame.__name__] = frame(container, self)
            self.frames[frame.__name__].place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_frame('BlankFrame')


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



class SidebarSubMenu(tk.Frame):

    def __init__(self, parent, sub_menu_heading, sub_menu_options, bg_color):

        tk.Frame.__init__(self, parent)
        self.config(bg=bg_color)
        self.sub_menu_heading_label = tk.Label(
            self,
            text=sub_menu_heading,
            bg=bg_color,
            font=('', 12, 'bold'),
            fg='#ffffff'
        )
        self.sub_menu_heading_label.place(x=30, y=10, anchor='w')

        sub_menu_sep = ttk.Separator(self, orient='horizontal')
        sub_menu_sep.place(x=30, y=30, relwidth=.8, anchor='w')

        self.options = {}
        for i in range(len(sub_menu_options)):
            option = sub_menu_options[i]

            self.options[option] = tk.Button(
                self,
                text=option,
                bg=bg_color,
                font=('', 10),
                bd=0,
                cursor='hand2',
                activebackground='#ffffff',
                fg='#ffffff',
                width=20,
                borderwidth=1,
            )
            self.options[option].place(x=30, y=60 + 30*i, anchor='w')