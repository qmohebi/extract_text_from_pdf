
class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Extract text from PDF and Save to CSV")
        self.window.geometry("630x160")
        self.window.resizable(False, False)

        font_style = ("Arial", 12)

        self.label1 = tk.Label(
            self.window, text="Source folder:", font=font_style)
        self.label1.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

        self.src_entry = tk.Entry(self.window, width=60)
        self.src_entry.grid(row=0, column=1, padx=10, pady=5)

        self.src_btn = tk.Button(
            self.window, font=font_style, text="Browse...",
            command=lambda: self.source_folder())
        self.src_btn.grid(row=0, column=2, padx=10, pady=5)

        self.label2 = tk.Label(
            self.window, text="File Destination:", font=font_style)
        self.label2.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

        self.dest_entry = tk.Entry(self.window, width=60)
        self.dest_entry.grid(row=1, column=1, padx=10, pady=5)

        self.dest_btn = tk.Button(
            self.window, font=font_style,  text="Browse...",
            command=lambda: self.save_file())
        self.dest_btn.grid(row=1, column=2, padx=10, pady=5)

        self.begin_btn = tk.Button(
            self.window, text="Start...", font=("Arial", 14), width=9, height=1)
            
        self.begin_btn.grid(row=3, column=0, padx=10, pady=5,
                            sticky=tk.S, columnspan=2)
        self.window.mainloop()

    def source_folder(self):
        file_path = filedialog.askdirectory()
        self.src_entry.delete(0, tk.END)
        self.src_entry.insert(0, file_path)

        return file_path

    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        self.dest_entry.delete(0, tk.END)
        self.dest_entry.insert(0, file_path)

        return file_path