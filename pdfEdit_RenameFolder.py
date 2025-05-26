import os
import io
import fitz
import tkinter as tk
from tkinter import filedialog,messagebox
import zipfile
import threading


def extract_pdf(folder_path):
    path = os.path.join(folder_path,"extractedPdf")
    os.mkdir(path)
    for zip_file in os.listdir(folder_path):
        if not zip_file.endswith(".zip"):
            continue
        zipfilepath = os.path.join(folder_path,zip_file)
        with zipfile.ZipFile(zipfilepath,'r') as zf:
            for file in zf.namelist():
                if file.endswith(".pdf") and not file.endswith("/"):
                    filename_only = os.path.basename(file)
                    if not filename_only:
                        continue
                    with zf.open(file) as source, open(os.path.join(path,filename_only),"wb") as target:
                        target.write(source.read())
    #messagebox.showinfo("Success", "All PDF files have been extracted.")
    extractedpdf_file_path = path
    return extractedpdf_file_path

def save_pdf(folder_path):
    pdf_files= os.listdir(folder_path)
    zip_filepath = os.path.abspath(os.path.join(folder_path,"..",".."))
    for file in pdf_files:
        if not file.endswith(".pdf"):
            continue
        filepath = os.path.join(folder_path,file)
        filename = os.path.basename(filepath)
        filename_only = filename.split("-")[0].strip()
        for zip_file in os.listdir(zip_filepath):
            if not zip_file.endswith(".zip"):
                continue
            
            zipfilepath =os.path.join(zip_filepath,zip_file)
            zipfilename = os.path.basename(zipfilepath).split(".zip")[0]
            if zipfilename == filename_only :
                with zipfile.ZipFile(zipfilepath, "a") as zf:
                    folder = zf.namelist()
                    arcname = os.path.join(folder[0],filename)
                    zf.write(filepath,arcname=arcname, compress_type=zipfile.ZIP_DEFLATED)
                break
    #messagebox.showinfo("Success", "All PDF files have been saved in the zip folder.")
    saved_file_path = zip_filepath
    return saved_file_path

def recheck_for_Reviewed_pdffile(folder_path):
    zip_files = os.listdir(folder_path)
    for zip_file in zip_files:
        if not zip_file.endswith(".zip"):
            continue
        zipfilepath = os.path.join(folder_path,zip_file)
        with zipfile.ZipFile(zipfilepath,'r') as zf:
            for file in zf.namelist():
                if file.endswith(".pdf") and "Edited" in file:
                    return True
    return False
        


def edit_pdf(folder_path):
    path = os.path.join(folder_path,"edited_pdfs")
    os.mkdir(path)
    replacements = {
        " Test Step(s) Pending":"None",
        "Pending Verification" : "None",
        "Pending" : "Pass"
    }         
    font_path = r"C:\Windows\Fonts\times.ttf"
    doc = fitz.open()
    font_name = 'Times New Roman Regular' 
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            filepath = os.path.join(folder_path, file)
            output_filename = file.split(".pdf")[0]+"_Edited.pdf"
            output_pdf_path = os.path.join(path,output_filename)
            absolute_pdf_path = os.path.abspath(output_pdf_path)
            zip_folder_path = os.path.abspath(os.path.join(absolute_pdf_path,"..","..",".."))
            doc = fitz.open(filepath)
            if not file.endswith(".pdf"):
                messagebox.showerror("Incorrect file type", f"The file {file} is not a valid PDF file. Please make sure you are using the correct file type.")
            else:
                for page in doc:
                    for search_text, replace_text in replacements.items():
                        areas = page.search_for(search_text)
                        if not areas:
                            continue
                        else:
                            if search_text == " Test Step(s) Pending":
                                for rect in areas:
                                    redaction_rect = fitz.Rect(rect.x0-1, rect.y0,rect.x1,rect.y1)
                                page.add_redact_annot(redaction_rect,fill=(1,1,1))
                                page.apply_redactions()
                                insert_point = (redaction_rect.x0,redaction_rect.y0+9)
                                page.insert_text(insert_point, replacements[" Test Step(s) Pending"], fontsize=7.5, color=(0,0,0), fontfile=font_path)
                            else:
                                for area in areas:
                                    page.add_redact_annot(area, fill=(1,1,1))
                                page.apply_redactions()
                                for rect in areas:
                                    x,y = rect.tl
                                    new_y = y+rect.height + 0.001
                                    page.insert_text((x,new_y), replace_text, fontsize=7.5, color=(0,0,0), fontfile=font_path)
            doc.save(output_pdf_path)
            doc.close()
    #messagebox.showinfo("Success", "All PDF files have been edited.")
    editedpdf_file_path = path
    return editedpdf_file_path

def rename_file(folder_path):
    files = os.listdir(folder_path)
    for file in files:
        if file.endswith(".zip") and "-" in file:
            try:
                new_filename = file.split("-")[0]+".zip"
                old_filepath = os.path.join(folder_path,file)
                new_filepath = os.path.join(folder_path,new_filename)
                if not os.path.exists(new_filepath):
                    os.rename(old_filepath,new_filepath)
                else:
                    messagebox.showerror("File exists",f"File {new_filename} already exists")
            except:
                messagebox.showerror("File error",f"Skipped file: {file}. Please check the file name and try again")
        else:
            messagebox.showerror("Incorrect file type",f"Skipped file: {file} is not a zip file. Please check the file name and try again")
    renamed_folder_path = folder_path
    return renamed_folder_path

def select_path():
    folder = filedialog.askdirectory()
    if folder:
        renamed_path = rename_file(folder)
        extractedpdf_path = extract_pdf(renamed_path)
        editedpdf_path = edit_pdf(extractedpdf_path)
        saved_path = save_pdf(editedpdf_path)
        recheck= recheck_for_Reviewed_pdffile(saved_path)
        if recheck:
            messagebox.showinfo("Success", "Reviewed Pdf files are saved to the zip folder.")
        else:
            messagebox.showerror("Error", "No Reviewed Pdf files found in the zip folder. Please check the folder and try again")   
        root.destroy()
    else:
        messagebox.showerror("Error", "No folder selected")

root = tk.Tk()
root.title("Edit Pdf files")
root.geometry("300x200")
frame = tk.Frame()
frame.pack(padx =30, pady=30)
btn1 = tk.Button(frame,text="Edit pdf files", command = select_path, width=20, height=2, font=("Arial", 12))
btn1.pack()
root.mainloop()