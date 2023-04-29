import os
import pythoncom

from win32com.client import constants
from win32com.client.gencache import EnsureDispatch
from fitz import open as open_pdf
from django.conf import settings as django_settings

# root directory for the uploaded files
UPLOAD_ROOT = django_settings.MEDIA_ROOT / 'presentation_files'


# Class to convert PowerPoint files to PDFs
class PowerPointApplication:
    def __init__(self):
        pythoncom.CoInitialize()
        self.powerpoint = EnsureDispatch('Powerpoint.Application')
        self.presentation = None
        try:
            self.powerpoint.Visible = False
        except:
            pass
        self.powerpoint.DisplayAlerts = False

    # Convert the PowerPoint file to PDF
    def powerpoint_to_pdf(self, filename: str, save_filename: str = "") -> str:
        # If the save_filename is not provided, use the filename
        if not save_filename:
            save_filename = os.path.splitext(filename)[0] + '.pdf'
        saved_filename = save_filename

        # Convert the relative path to an absolute path
        filename = os.path.abspath(filename)
        save_filename = os.path.abspath(save_filename)

        # Force the save_filename to have a pdf extension.
        split = os.path.splitext(save_filename)
        if split[-1].lower() != '.pdf':
            save_filename = split[0] + '.pdf'

        self.presentation = self.powerpoint.Presentations.Open(filename, WithWindow=False)
        self.presentation.SaveAs(save_filename, constants.ppSaveAsPDF)
        return saved_filename

    def close(self):
        if self.presentation:
            self.presentation.Close()
        if self.powerpoint:
            self.powerpoint.Quit()
        pythoncom.CoUninitialize()
        self.presentation = None
        self.powerpoint = None

    def __del__(self):
        self.close()


# Handle the uploaded file
def handle_uploaded_file(file, filename):
    # get the number of folders in the upload folder
    folders = os.listdir(UPLOAD_ROOT)
    num_folders = len(folders) if ".gitkeep" not in folders else (len(folders) - folders.count('.gitkeep'))

    # Create a folder for the uploaded file
    folder = UPLOAD_ROOT / f"presentation_{num_folders + 1}"
    os.makedirs(folder, exist_ok=True)

    # Save the file
    with open(folder / filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return folder


# Convert the PowerPoint file to PDF
def powerpoint_to_pdf(filename: str, save_filename: str = "") -> str:
    powerpoint_application = PowerPointApplication()
    saved_filename = powerpoint_application.powerpoint_to_pdf(filename, save_filename)
    powerpoint_application.close()
    return saved_filename


# Convert the PDF to PNGs
def pdf_to_png(pdf_file, output_folder: str = "images"):
    # Open the PDF file
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)
    document = open_pdf(pdf_file)
    # Save the PDF to images
    for page in document:  # iterate through the pages
        # Save the images as PNG files in the output folder
        pixmap = page.get_pixmap(dpi=300)  # render page to an image
        pixmap.save(os.path.join(output_folder, f"page_{page.number + 1}.png"))  # store image as a PNG
    return output_folder


# get the number of images in the images folder
def get_num_pages(presentation_path: str):
    images_folder = UPLOAD_ROOT / presentation_path / "images"
    return len(os.listdir(images_folder))