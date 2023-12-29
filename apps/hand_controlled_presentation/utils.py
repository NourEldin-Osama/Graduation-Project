import os
import platform
import subprocess
import time

from django.conf import settings as django_settings
from fitz import open as open_pdf

is_windows = platform.system() == 'Windows'
is_linux = platform.system() == 'Linux'
if is_windows:
    import pythoncom
    from win32com.client import constants
    from win32com.client.gencache import EnsureDispatch

# root directory for the uploaded files
UPLOAD_ROOT = django_settings.MEDIA_ROOT / 'presentation_files'

# Check if the UPLOAD_ROOT directory exists, if not create it
if not os.path.exists(UPLOAD_ROOT):
    os.makedirs(UPLOAD_ROOT, exist_ok=True)


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


def convert_powerpoint_to_pdf_libreoffice(filename: str, save_filename: str = ""):
    # If the save_filename is not provided, use the filename
    if not save_filename:
        save_filename = os.path.splitext(filename)[0] + '.pdf'
    saved_filename = save_filename

    # Convert the relative path to an absolute path
    filename = os.path.abspath(filename)

    # Construct the command
    command = ["libreoffice", "--headless", "--convert-to", "pdf", filename, "--outdir", os.path.dirname(filename)]

    # Run the command
    subprocess.run(command, check=True)
    return saved_filename


def is_libreoffice_installed():
    try:
        # Try to call libreoffice
        command = "libreoffice --version"
        subprocess.run(command.split(), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        # If the call fails, libreoffice is not installed
        return False


def install_libreoffice():
    try:
        print('Installing LibreOffice...')
        start = time.time()
        # Define the command to install libreoffice-impress in linux
        command = "apt-get -qq install libreoffice-impress"

        # Run the command without printing the output to the console
        subprocess.run(command.split(), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        end = time.time()
        print('Successfully installed LibreOffice.')
        print(f'Time taken: {end - start:.2f}s')

    except subprocess.CalledProcessError as e:
        print(f'Failed to install LibreOffice. Error: {e}')


# Install libreoffice if it's not already installed
def check_libreoffice():
    if is_linux and not is_libreoffice_installed():
        install_libreoffice()
    elif is_libreoffice_installed():
        print('LibreOffice is already installed.')


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
    if is_windows:
        powerpoint_application = PowerPointApplication()
        saved_filename = powerpoint_application.powerpoint_to_pdf(filename, save_filename)
        powerpoint_application.close()
        return saved_filename
    elif is_linux:
        check_libreoffice()
        return convert_powerpoint_to_pdf_libreoffice(filename, save_filename)
    else:
        raise NotImplementedError(f"Conversion from PowerPoint to PDF is not supported on {platform.system()}")


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
