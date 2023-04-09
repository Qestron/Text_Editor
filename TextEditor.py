import tkinter as tk
from tkinter import Tk, scrolledtext, Menu, messagebox, filedialog, simpledialog


class TextEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Text Editor")
        self.file = None


        # Create a frame to hold the line number number display and the text area
        frame = tk.Frame(self.master)
        frame.pack(fill=tk.BOTH, expand=1)

        # Create line number display
        self.line_numbers = tk.Text(frame, width=4, padx=3, takefocus=0, background='lightgray', state='disabled')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        
        # Create Text area
        self.text_area = tk.Text(frame, undo=True)
        self.text_area.pack(side=tk.LEFT, expand=1 , fill=tk.BOTH)

        # Bind the scrollbar to the text area and line number display
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=self.scroll_text)
        self.text_area.config(yscrollcommand=scrollbar.set)
        self.line_numbers.config(yscrollcommand=scrollbar.set)

        # Bind the text area to the update_line_numbers method
        self.text_area.bind("<Any-KeyPress>", self.update_line_numbers)
        
        # Create Menu Bar
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)
        
        # Add File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New",  command=self.new_file)
        self.file_menu.add_command(label="Open",  command=self.open_file)
        self.file_menu.add_command(label="Save",  command=self.save_file)
        self.file_menu.add_command(label="Save as", command=self.save_file_as)
        

        # Add Edit Menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Find", accelerator="Ctrl+F", command=self.search)

        # Bind keyboard shortcuts to the text area
        self.text_area.bind_all("<Control-s>", self.save_file)
        self.text_area.bind_all("<Control-o>", self.open_file)
        self.text_area.bind_all("<Control-n>", self.new_file)
        self.text_area.bind_all("<Control-a>", self.select_all)
        self.text_area.bind_all("<Control-x>", self.cut_text)
        self.text_area.bind_all("<Control-c>", self.copy_text)
        self.text_area.bind_all("<Control-v>", self.paste_text)
        self.text_area.bind_all("<Control-S>", self.save_file_as)
        self.text_area.bind_all("<Control-f>", self.search)
        self.text_area.bind_all("<Control-z>", self.undo)


    
    def update_line_numbers(self, event=None):
        # Clear the line number display
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)

        # Get the number of lines in the text area
        num_lines = self.text_area.index(tk.END).split('.')[0]

        # Add the line numbers to the display
        for line_num in range(1, int(num_lines)):
            self.line_numbers.insert(tk.END, f"{line_num}\n")

        # Disable the line number display
        self.line_numbers.config(state='disabled')
    
    def scroll_text(self, *args):
        self.text_area.yview_moveto(args[0])
        self.line_numbers.yview_moveto(args[0])


    def new_file(self, event=None):
        self.file = None
        self.text_area.delete("1.0", tk.END)
        
    def open_file(self, event=None):
        self.text_area.bind_all("<")
        self.file = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if self.file:
            with open(self.file, "r") as f:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, f.read())
        
    def save_file(self, event=None):
        if self.file:
            try:
                text = self.text_area.get(1.0, tk.END)
                with open(self.file, 'w') as f:
                    f.write(text)
            except Exception as e:
                messagebox.showerror("Error", e)
        else:
            self.save_file_as()


    def save_file_as(self, event=None):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
            except Exception as e:
                messagebox.showerror("Error", e)
    

    def cut_text(self, event=None):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self, event = None):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self, event= None):
        self.text_area.event_generate("<<Paste>>")

    def select_all(self, event=None):
        self.text_area.tag_add(tk.SEL, 1.0, tk.END)
        self.text_area.mark_set(tk.INSERT, 1.0)
        self.text_area.see(tk.INSERT)

    def undo(self, event=None):
        self.text_area.edit_undo()

    
    def search(self, event=None):
        # Prompt the user to enter a search string
        search_string = simpledialog.askstring("Search", "Enter search string:")

        # Return if the user clicked Cancel or entered an empty string
        if search_string is None or search_string == "":
            return

        # Remove any previous search highlighting
        self.text_area.tag_remove("search", "1.0", "end")

        # Find all instances of the search string in the text area
        start_pos = "1.0"
        while True:
            # Find the next instance of the search string
            start_pos = self.text_area.search(search_string, start_pos, "end")
            if start_pos == "":
                break

            # Calculate the end position of the found text
            end_pos = f"{start_pos}+{len(search_string)}c"

            # Highlight the found text
            self.text_area.tag_add("search", start_pos, end_pos)
            start_pos = end_pos

        # Configure the search tag to highlight the text
        self.text_area.tag_config("search", background="yellow")


if __name__ == '__main__':
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()
