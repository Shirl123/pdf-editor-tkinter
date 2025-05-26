Objective:
1. Rename a zipfile
2. Copy a pdf from the zipfile without extracting the zip file into another folder.
3. Edit the pdf by searching for required text, redacting and replacing with the required text.
4. Save the edited pdf with a different name into the originl renamed zip folder
   

Tasks performed:
This .py file contains methods to rename a zip folder, copy the pdf file from the zip folder without extracting the whole zip folder into a new folder.
The pdfs in the new folder (extractedPdfs) are edited for required text changes by searching for the text, redacting the text and replacing the text with the required text.
These edited pdfs are placed in a differnt folder and saved to the zip folder with a different name.
These zip folders are again checked if the edited pdf is available.
Developed the UI using Tkinter python library for Desktop applications.
NOTE:
The .exe for this file is not attached in the repository.

How to run:
THe user gets a .exe file of the .py file

What happens when run:
1. When the user runs the .exe file for pdfEdit_RenameFolder.py, the tkinter desktop application named "PDF Editor" opens up.
2. The UI application contains a button labelled "Edit Pdf files" which when the user clicks prompts the user to select a system directory.
3. Once the user selects a directory with all the zip folders, the code executes and the above mentioned actions are performed on the zip folder and the pdf files of each zip folder.
4. The user receives a message ""Success", "Edited Pdf files are saved to the zip folder.""
5. Corner cases such as if the "_Edited.pdf" file does not exist, zip file does not exist and other crucial cases for failures are considered.
6. The user can check the selected path zip folders with the format expected.
   
