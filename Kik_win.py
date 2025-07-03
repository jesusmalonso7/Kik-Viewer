from Kik_Functions import *
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
import platform
import sys
import os


def main():
    app = Application()
    app.mainloop()


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # Do not show a window title. Only the Kik Icon will be displayed
        self.title(" ")

        # Show Kik icon. Use platform-specific filepath to the Kik icon.
        if platform.system().lower() == 'windows':
            self.iconphoto(False, tk.PhotoImage(file=r'images/kik.png'))
        elif platform.system().lower() == 'Linux':
            image_folder = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__),
                                                                     r'images/kik.png')))
            p1 = tk.PhotoImage(file=image_folder.replace('\\', '/'))
            self.iconphoto(False, p1)

        # Default application window size.
        self.geometry("1024x768")

        # Configure application columns and rows
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Displays "Kik View" in green letters centered at the top of the window.
        frame_header = FrameHeader(self)
        frame_header.grid(column=0, row=0, sticky=tk.EW, padx=5, pady=5, columnspan=1)

        # Displays the button, "Usernames" label, TreeView, and Listbox
        frame = InputForm(self)
        frame.grid(column=0, row=1, sticky=tk.NSEW, padx=5, pady=5)


class FrameHeader(ttk.Frame):
    """
        Display the Kik Message Viewer label in green letters
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.label = ttk.Label(self, text="Kik Viewer", font=("Arial", 20), background="White",
                               foreground="Green")
        self.label.grid(column=0, row=0)


class InputForm(ttk.Frame):
    """
        @param: ttk.Frame
        @return: None
    """
    def __init__(self, parent):
        super().__init__(parent)
        # Instance variables
        self.output_filepath = ' '

        # Set the number of columns and rows for the Frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # Set ttk style that will be used with the TreeView, button, and Scrollbars
        style = ttk.Style()
        style.theme_use('winnative')

        # The button is used to open a dialog window so the user can select the Kik CSV file.
        self.entry_btn = ttk.Button(self, text="Open Kik CSV File", command=self.browse)
        self.entry_btn.grid(row=1, column=0,  sticky=tk.W, padx=5, pady=5)
        style.configure("TButton", foreground="Green", font=("Arial", 12))

        # Checkbox to acknowledge a desire to print the chat thread.
        self.print_chkbox = ttk.Checkbutton(self, text="Save Chat")
        self.print_chkbox.state(['!selected', '!alternate'])
        self.print_chkbox.grid(row=1, column=0, sticky=tk.W, padx=200)

        # Adds the "Processing..." and "Usernames" labels
        self.label_processing = ttk.Label(self, text='', font=("Arial", 14), foreground="white")
        self.label_processing.grid(row=1, column=0, sticky=tk.W, padx=300)
        self.label_users = ttk.Label(self, text="Usernames", font=("Arial", 14))
        self.label_users.grid(row=1, column=1)

        # Create the list box to hold usernames
        self.text_list_users = tk.Listbox(self, font=("Arial", 14), borderwidth=2, relief="sunken")
        self.text_list_users.grid(row=2, column=1, sticky=tk.NSEW)

        # Create a vertical and horizontal scrollbars for text_list_users
        self.yScroll = ttk.Scrollbar(self, orient="vertical", command=self.text_list_users.yview)
        self.xScroll = ttk.Scrollbar(self, orient="horizontal", command=self.text_list_users.xview)
        self.yScroll.grid(row=2, column=1, sticky=tk.N + tk.S + tk.E)
        self.xScroll.grid(row=2, column=1, rowspan=2, sticky=tk.EW + tk.S)
        self.text_list_users.configure(yscrollcommand=self.yScroll.set, xscrollcommand=self.xScroll.set)

        # Create the TreeView to hold user chat logs
        style.configure('Treeview.Heading', font=("Arial", 14), foreground="White", background="Green")
        self.messages_treeview = ttk.Treeview(self, columns=(0, 1, 2, 3), show="headings")
        self.messages_treeview.grid(row=2, column=0, columnspan=1, sticky=tk.NSEW)

        # Define column headings
        self.messages_treeview.heading(0, text="Sender", anchor="w")
        self.messages_treeview.heading(1, text="Recipient", anchor="w")
        self.messages_treeview.heading(2, text="Date/Time", anchor="w")
        self.messages_treeview.heading(3, text="Message", anchor="w")

        # Define column
        self.messages_treeview.column(0, width=120, stretch=False)
        self.messages_treeview.column(1, width=120, stretch=False)
        self.messages_treeview.column(2, width=200, stretch=False)
        self.messages_treeview.column(3, width=5120, stretch=False)

        # Create horizontal and vertical scrollbars for message_treeview
        self.yScroll = ttk.Scrollbar(self, orient="vertical", command=self.messages_treeview.yview)
        self.yScroll.grid(row=2, column=0, sticky=tk.NS + tk.E)
        self.xScroll = ttk.Scrollbar(self, orient="horizontal", command=self.messages_treeview.xview)
        self.xScroll.grid(row=3, column=0, sticky=tk.EW+tk.S)
        self.messages_treeview.configure(xscrollcommand=self.xScroll.set, yscrollcommand=self.yScroll.set)

    def clear_list(self):
        """
           When the clear button is pressed, delete the messages displayed in the text_list_messages List box.
        """
        self.messages_treeview.delete(*self.messages_treeview.get_children())

    def browse(self, _event=None):
        """
            When the Open CSV file button is pressed, open a filedialog window. If the user closes the window without
            selecting a file, exit the program. Otherwise, open the file selected and processes it.
        """

        # This disables the double click event for the text_list_users box until the Browse() function inserts the
        # usernames. This prevents an out of index error in the on_double_click() function when using cursor selection.
        self.text_list_users.bind('<Double-1>', self.on_double_click)

        try:
            input_filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Octet-Stream", "*.octet-stream")])
        except FileNotFoundError:
            sys.exit(-1)

        # Create a class object for KikProcessing using the CSV file as input
        my_process = KikProcessing(input_filepath)
        # Remove the legend in the CSV file.
        self.output_filepath = my_process.remove_kik_legend_from_csv_file(input_filepath)
        # Get all the user in the CSV file and store them in a list.
        users = my_process.get_users(self.output_filepath)
        # Step through the elements in users, then add the users to the text_list_users List Box
        self.text_list_users.insert(0, *users)

    def on_double_click(self, event):
        my_process = KikProcessing(self.output_filepath)
        # Make sure the new treeview is cleared before creating a new one. To clear it, immediately
        # execute the update() function
        self.messages_treeview.delete(*self.messages_treeview.get_children())
        self.messages_treeview.update()

        # The Value variable contains the username selected from the "usernames" list box.
        cs = event.widget.curselection()
        index = cs[0]
        value = event.widget.get(index)

        # Print the chat to a text file if the print checkbox is selected.
        if self.print_chkbox.instate(['selected']):
            # The message label was empty. Change it to "Processing..." to show something is happening. Update the
            # treeview so "Processing..." shows up immediately.
            self.label_processing.configure(text="Processing...", font=("Arial", 14), foreground="red")
            self.messages_treeview.update()
            my_process.print_chats(value, self.output_filepath)

        # The message label was empty. Change it to "Processing..." to show something is happening. Update the
        # treeview so "Processing..." shows up immediately.
        self.label_processing.configure(text="Processing...", font=("Arial", 14), foreground="red")
        self.messages_treeview.update()

        # Process all the chats for the selected user. Remove the header located at chats[0]. The header is not needed
        # with TreeView.
        chats = my_process.get_chat(value, self.output_filepath)
        chats.pop(0)

        # Clear "Processing..." from row.
        self.label_processing.configure(text=" ", font=("Arial", 14))
        self.messages_treeview.update()

        for chat in chats:
            # chat[1] == sender username, chat[2] == recipient username
            # chat[7] == timestamp, chat[4] == text
            self.messages_treeview.insert('', "end", values=(chat[1], chat[2], chat[7], chat[4]))


if __name__ == "__main__":
    main()