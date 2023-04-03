import tkinter
import customtkinter
from datetime import date
from time import strftime

theme_color = ""
customtkinter.set_default_color_theme("green")


def add_spaces(number_of_spaces: int):
    string_with_spaces = ''
    number_counter = 0
    while number_counter < number_of_spaces:
        string_with_spaces = string_with_spaces + ' '
        number_counter += 1
    return string_with_spaces


def launch_application():
    app = App()
    # Set main window as non-resizeable
    app.resizable(False, False)
    app.mainloop()


class App(customtkinter.CTk):
    def __init__(self):

        def set_line_height():
            line_height = 22
            return line_height

        window_height = 630 + (14 * (set_line_height() - 20))
        window_width = 900

        description_placeholder = "Description of the change..."

        def add_placeholder(placeholder_value):
            if self.description.get("1.0", tkinter.END) == "\n" \
                    or self.description.get("1.0", tkinter.END) == f"{placeholder_value}\n":
                self.description.delete("1.0", tkinter.END)
                self.description.insert("0.0", placeholder_value)
                self.description.configure(text_color="grey")

        def remove_placeholder(placeholder_value):
            if self.description.get("1.0", tkinter.END) == f"{placeholder_value}\n":
                self.description.configure(text_color=get_text_color())
                self.description.delete("0.0", tkinter.END)

        def get_text_color():
            return "white" if self.appearance_mode_option_menu.get() in ["System", "Dark"] else "black"

        def copy_text_to_clipboard(event):
            field_value = event.widget.get("1.0", 'end-1c')  # get field value from event, but remove line return at end
            self.clipboard_clear()  # clear clipboard contents
            self.clipboard_append(field_value)  # append new value to clipboard

        def change_appearance_mode_event(new_appearance_mode: str):
            self.description.configure(text_color=get_text_color())
            add_placeholder(description_placeholder)
            customtkinter.set_appearance_mode(new_appearance_mode)

        def change_theme_color_event(new_theme_color: str):
            global theme_color
            if new_theme_color != theme_color:
                new_theme_color_label = new_theme_color
                new_theme_color = new_theme_color.lower().replace(" ", "-")
                self.destroy()
                customtkinter.set_default_color_theme(new_theme_color)
                theme_color = new_theme_color_label
                launch_application()

        def change_scaling_event(new_scaling: str):
            new_scaling_float = float(new_scaling.replace("%", "")) / 100
            self.geometry('%dx%d+%d+%d' % (window_width * new_scaling_float, window_height * new_scaling_float,
                                           screen_x_axis, screen_y_axis))
            customtkinter.set_widget_scaling(new_scaling_float)

        def get_time():
            time_string = strftime('%H:%M:%S')
            return time_string

        def run_time_clock():
            self.time_value.configure(text=get_time())
            self.time_value.after(1000, run_time_clock)

        def get_date():
            # TODO: make it so it will be able to change dates
            date_string = strftime("%d.%m.%Y")
            return date_string

        def generate_comments():
            comment_line_stars = '*----------------------------------------------------------------------*'
            inc_tbd = 'INC-TBD'.strip()

            description_value_conv = ''
            text = self.description.get('1.0', tkinter.END).splitlines()
            text = list(filter(lambda list_element: list_element != '', text)) if len(text) > 1 else text

            for idx, line in enumerate(text):
                if idx == 0:
                    description_value_conv = f'{line}{add_spaces(56 - len(line))}*\n'
                else:
                    description_value_conv = description_value_conv + \
                                             f'*{add_spaces(14)}{line}{add_spaces(56 - len(line))}*\n'

            case_id_value = self.case_id.get() if self.case_id.get().strip() else inc_tbd
            date_plain = self.date_value.get().replace(".", "")

            # TODO: write an API that will retrieve the data based on user name
            name_and_surname = 'Tomasz Grabarczyk'

            changed_by_num_of_chars = len(
                f'{name_and_surname} - ({self.user_name.get()}) - '
                f'{self.user_name.get()}{date_plain}')

            header_comment_value = f'{comment_line_stars}\n' \
                                   f'* Changed by : {name_and_surname} - ({self.user_name.get()}) - ' \
                                   f'{self.user_name.get()}{date_plain}' \
                                   f'{add_spaces(56 - changed_by_num_of_chars)}*\n' \
                                   f'* Changed on : {self.date_value.get()}' \
                                   f'{add_spaces(46)}*\n' \
                                   f'* Case ID    : {case_id_value}' \
                                   f'{add_spaces(56 - len(case_id_value))}*\n' \
                                   f'* Description: {description_value_conv}' \
                                   f'{comment_line_stars}'

            multiple_line_comment_value = f'* >>> {self.user_name.get()} {date_plain}' + ' - ' + case_id_value + '\n' \
                                          f'* <<< {self.user_name.get()} {date_plain}' + ' - ' + case_id_value

            single_line_comment_value = f'" >>> {self.user_name.get()} {date_plain}' + ' - ' + case_id_value

            dynamic_ctk_textbox = [self.header_comment, self.multiple_line_comment, self.single_line_comment]

            for ctk_textbox_element in dynamic_ctk_textbox:
                if ctk_textbox_element == self.header_comment:
                    text = header_comment_value
                elif ctk_textbox_element == self.multiple_line_comment:
                    text = multiple_line_comment_value
                elif ctk_textbox_element == self.single_line_comment:
                    text = single_line_comment_value

                ctk_textbox_element.configure(state="normal")
                ctk_textbox_element.delete('1.0', tkinter.END)
                ctk_textbox_element.insert(1.0, text)
                ctk_textbox_element.configure(state="disabled")
                ctk_textbox_element.bind("<Button-1>", copy_text_to_clipboard)

        def clear_comments():
            self.case_id.delete(0, tkinter.END)

            # Clear description CTkTextbox
            self.description.delete("1.0", tkinter.END)
            add_placeholder(description_placeholder)

            dynamic_ctk_textbox = [self.header_comment, self.multiple_line_comment, self.single_line_comment]

            for ctk_textbox_element in dynamic_ctk_textbox:
                ctk_textbox_element.configure(state="normal")
                ctk_textbox_element.delete("1.0", tkinter.END)
                ctk_textbox_element.configure(state="disabled")

        super().__init__()

        # configure window
        self.title("ABAP Tools")

        # calculate x and y coordinates for the Tk root window
        screen_x_axis = (self.winfo_screenwidth() / 2) - (window_width / 2)
        screen_y_axis = (self.winfo_screenheight() / 2) - (window_height / 2)

        # Set the dimensions of the screen and where it is placed
        self.geometry('%dx%d+%d+%d' % (window_width, window_height, screen_x_axis, screen_y_axis))

        # TODO: change columnconfigure to proper loop
        # for element in [1, 2, 3]:
        #     self.grid_columnconfigure(element, weight=1)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)

        for element in [9]:
            self.grid_rowconfigure(element, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=12, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.date_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                 font=customtkinter.CTkFont(weight="bold"),
                                                 text="Date:",
                                                 anchor="w")
        self.date_label.grid(row=0, column=0, padx=20, pady=(10, 0))

        self.date_value = customtkinter.CTkLabel(self.sidebar_frame,
                                                 anchor="w")
        self.date_value.grid(row=1, column=0, padx=20)
        self.date_value.configure(text=get_date())

        self.time_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                 font=customtkinter.CTkFont(weight="bold"),
                                                 text="Time:",
                                                 anchor="w")
        self.time_label.grid(row=2, column=0, padx=20, pady=(10, 0))

        self.time_value = customtkinter.CTkLabel(self.sidebar_frame,
                                                 anchor="w")
        self.time_value.grid(row=3, column=0, padx=20)

        run_time_clock()

        self.week_number_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                        font=customtkinter.CTkFont(weight="bold"),
                                                        text="Week Number:",
                                                        anchor="w")
        self.week_number_label.grid(row=4, column=0, padx=20, pady=(10, 0))

        self.week_number_value = customtkinter.CTkLabel(self.sidebar_frame,
                                                        text=str(date.today().isocalendar()[1]),
                                                        anchor="w")
        self.week_number_value.grid(row=5, column=0, padx=20)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                            text="Appearance Mode:",
                                                            anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=8, column=0, padx=20, pady=(10, 10))

        self.theme_color_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                        text="Theme Color:",
                                                        anchor="w")
        self.theme_color_label.grid(row=9, column=0, padx=20, pady=(10, 0))

        self.theme_color_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                   values=["Green", "Blue", "Dark Blue"],
                                                                   command=change_theme_color_event)
        self.theme_color_option_menu.grid(row=10, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=11, column=0, padx=20, pady=(10, 0))

        self.scaling_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["50%", "60%", "70%", "80%", "90%", "100%"],
                                                               command=change_scaling_event)
        self.scaling_option_menu.grid(row=12, column=0, padx=20, pady=(10, 30))

        # Create tabview
        self.tabview = customtkinter.CTkTabview(self, width=window_width)
        self.tabview.grid(row=0, column=1, columnspan=2, padx=20, pady=20)

        # Configure grid for individual tabs
        for tab_view_element in ["ABAP Comments", "ABAP Transport", "GitHub Pull Request"]:
            self.tabview.add(tab_view_element)
            self.tabview.tab(tab_view_element).grid_columnconfigure(0, weight=1)

        # TODO: add option to select different date with calendar
        self.case_id = customtkinter.CTkEntry(master=self.tabview.tab("ABAP Comments"),
                                              placeholder_text="Case ID",
                                              font=customtkinter.CTkFont(family="Consolas", size=14),
                                              justify=tkinter.CENTER)
        # command=show_calendar
        self.case_id.grid(row=1, column=0, padx=(90, 0), pady=10)

        self.user_name = customtkinter.CTkEntry(master=self.tabview.tab("ABAP Comments"),
                                                placeholder_text="SAP User",
                                                font=customtkinter.CTkFont(family="Consolas", size=14),
                                                justify=tkinter.CENTER)
        self.user_name.insert(0, "GRABATMA")
        self.user_name.grid(row=1, column=1, padx=(0, 265), pady=10)

        self.date_value = customtkinter.CTkEntry(master=self.tabview.tab("ABAP Comments"),
                                                 placeholder_text="Date",
                                                 font=customtkinter.CTkFont(family="Consolas", size=14),
                                                 justify=tkinter.CENTER)
        self.date_value.insert(0, get_date())
        self.date_value.grid(row=1, column=1, padx=(50, 0), pady=10)

        self.description = customtkinter.CTkTextbox(master=self.tabview.tab("ABAP Comments"),
                                                    font=customtkinter.CTkFont(family="Consolas", size=14),
                                                    width=465,
                                                    height=set_line_height() * 4)
        add_placeholder(description_placeholder)
        self.description.bind("<FocusIn>", lambda event: remove_placeholder(description_placeholder))
        self.description.bind("<FocusOut>", lambda event: add_placeholder(description_placeholder))
        self.description.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.generate_comment = customtkinter.CTkButton(master=self.tabview.tab("ABAP Comments"),
                                                        text="Generate comment",
                                                        command=generate_comments)
        self.generate_comment.grid(row=4, column=0, columnspan=2, padx=(0, 160), pady=10)

        self.clear_comment = customtkinter.CTkButton(master=self.tabview.tab("ABAP Comments"),
                                                     text="Clear",
                                                     command=clear_comments)
        self.clear_comment.grid(row=4, column=1, padx=(0, 100), pady=10)

        self.header_comment_label = customtkinter.CTkLabel(master=self.tabview.tab("ABAP Comments"),
                                                           font=customtkinter.CTkFont(weight="bold"),
                                                           text="Header comment:",
                                                           justify=tkinter.LEFT)
        self.header_comment_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.multiple_line_comment_label = customtkinter.CTkLabel(master=self.tabview.tab("ABAP Comments"),
                                                                  font=customtkinter.CTkFont(weight="bold"),
                                                                  text="Multiple line comment:",
                                                                  justify=tkinter.LEFT)
        self.multiple_line_comment_label.grid(row=8, column=0, columnspan=2, padx=(0, 330), pady=10)

        self.single_line_comment_label = customtkinter.CTkLabel(master=self.tabview.tab("ABAP Comments"),
                                                                font=customtkinter.CTkFont(weight="bold"),
                                                                text="Single line comment:",
                                                                justify=tkinter.LEFT)
        self.single_line_comment_label.grid(row=8, column=1, padx=(60, 0), pady=10)

        self.header_comment = customtkinter.CTkTextbox(master=self.tabview.tab("ABAP Comments"),
                                                       font=customtkinter.CTkFont(family="Consolas", size=14),
                                                       width=600,
                                                       height=set_line_height() * 8)
        self.header_comment.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        self.header_comment.configure(state="disabled")

        self.multiple_line_comment = customtkinter.CTkTextbox(master=self.tabview.tab("ABAP Comments"),
                                                              font=customtkinter.CTkFont(family="Consolas", size=14),
                                                              width=300,
                                                              height=set_line_height() * 2 + 7)
        self.multiple_line_comment.grid(row=9, column=0, columnspan=2, padx=(0, 330), pady=10)
        self.multiple_line_comment.configure(state="disabled")

        self.single_line_comment = customtkinter.CTkTextbox(master=self.tabview.tab("ABAP Comments"),
                                                            font=customtkinter.CTkFont(family="Consolas", size=14),
                                                            width=300,
                                                            height=set_line_height() * 1 - 4)
        self.single_line_comment.grid(row=9, column=1, padx=(60, 0), pady=10)
        self.single_line_comment.configure(state="disabled")

        # set default values
        self.appearance_mode_option_menu.set("System")
        self.scaling_option_menu.set("100%")
        global theme_color
        self.theme_color_option_menu.set(theme_color if theme_color != "" else "Green")


if __name__ == "__main__":
    launch_application()
