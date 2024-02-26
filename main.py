# script below is developed to look at Health Weigh calibration certificate
# pattern match to find asset no, serial no, calibration date, model, brand.
# As the info on the pdf is not structured,
# a small percent of pattern will not pick the right info,
#  here page no and filename is recorded do a manual find.

# TODO offload the gui to a seperate class
# TODO catch error for when folder doesn't have a pdf file in it
# TODO catch when folder has pdf but not the right pdf for pattern search to work.

import re
import shutil
import os
import csv
import threading
import tkinter as tk
from tkinter import filedialog, messagebox


from pdfminer.high_level import extract_text, extract_pages

CONTENT = {
        "asset": [],
        "serial_no": [],
        "brand": [],
        "model": [],
        "calibration_date": [],
        "page": [],
        "filename": []
        }


def main():

    def get_pdf_file(source: str):

        """Takes source directory, gets pdf files
        and feeds to funct to extract text """
        for filename in os.listdir(source):
            if filename.endswith(".pdf") or filename.endswith(".PDF"):
                file_path = os.path.join(source, filename)
                pdf_base, pdf_ext = os.path.splitext(filename)

                txt_from_pdf(path=file_path, file_name=filename)

    def txt_from_pdf(path: str, file_name: str) -> dict:
        """
        takes path to PDF file, skips first page, searches pdf for pattern
        and writes to CONTENT dictionary
        """
        with open(path, "rb") as f:
            page_no = len(list(extract_pages(path)))

            asset_pattern = r'Asset №: (\S+)'
            calibration_pattern = r'CALIBRATION DATE: (\d{2}/\d{2}/\d{4})'
            scale_pattern = r'SCALE TYPE (\w+) (\S+)'
            sn_pattern = r'ECCENTRICITY TEST (\S+)'

            for page in range(1, page_no):
                text = extract_text(pdf_file=f, page_numbers=[page])
                pdf_txt = re.sub(r'\s+', ' ', text)
                print(pdf_txt)
                asset_match = re.search(asset_pattern, pdf_txt)
                calibration_match = re.search(calibration_pattern, pdf_txt)
                scale_match = re.search(scale_pattern, pdf_txt)
                sn_match = re.search(sn_pattern, pdf_txt)

                CONTENT["page"].append(page)
                CONTENT["filename"].append(file_name)

                if asset_match:
                    CONTENT["asset"].append(asset_match.group(1))
                if calibration_match:
                    CONTENT["calibration_date"].append(calibration_match.group(1))
                if scale_match:
                    CONTENT["brand"].append(scale_match.group(1))
                    CONTENT["model"].append(scale_match.group(2))
                if sn_match:
                    sn_match = sn_match.group(1).rstrip("-")
                    CONTENT["serial_no"].append(sn_match)

    def dict_to_csv(data: dict, file_name: str) -> None:
        """Takes dictionary data type and writes it to CSV File"""
        keys = list(data.keys())
        values = list(data.values())
        with open(file_name, 'w', newline="", encoding="utf-8") as file:
            w = csv.writer(file)
            w.writerow(keys)
            w.writerows(zip(*values)) # transpose the values 

    def source_folder(location):
        file_path = filedialog.askdirectory()
        location.delete(0, tk.END)
        location.insert(0, file_path)

        return file_path

    def save_file(location):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        location.delete(0, tk.END)
        location.insert(0, file_path)

        return file_path

    def begin_process(source_folder, destination_file_name):
        folder = source_folder.get()
        dest_file = destination_file_name.get()

        if not (folder and dest_file):
            messagebox.showwarning("Error", "All fields are mandatory")
        else:
            get_pdf_file(folder)
            dict_to_csv(CONTENT, dest_file)
            messagebox.showinfo(
                "Process Commplete",
                f""" Extraction Complete, Please check folder:\
                {os.path.dirname(dest_file)}"""
                )

    window = tk.Tk()
    window.title("Extract text from PDF and Save to CSV")
    window.geometry("655x150")
    window.resizable(False, False)

    font_style = ("Arial", 12)

    label1 = tk.Label(
        window, text="Source folder:", font=font_style)
    label1.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

    src_entry = tk.Entry(window, width=60)
    src_entry.grid(row=0, column=1, padx=10, pady=5)

    src_btn = tk.Button(
        window, font=font_style, text="Browse", width=9,
        command=lambda: source_folder(src_entry))
    src_btn.grid(row=0, column=2, padx=10, pady=5)

    label2 = tk.Label(
        window, text="File Destination:", font=font_style)
    label2.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

    dest_entry = tk.Entry(window, width=60)
    dest_entry.grid(row=1, column=1, padx=10, pady=5)

    dest_btn = tk.Button(
        window, font=font_style,  text="Browse", width=9,
        command=lambda: save_file(dest_entry))
    dest_btn.grid(row=1, column=2, padx=10, pady=5)

    begin_btn = tk.Button(
        window, text="Start", font=("Arial", 14), width=9, height=1,
        command=lambda: begin_process(src_entry, dest_entry))

    begin_btn.grid(
        row=3, column=0, padx=10, pady=5,sticky=tk.S, columnspan=2)

    window.mainloop()


if __name__ == "__main__":
    main()
