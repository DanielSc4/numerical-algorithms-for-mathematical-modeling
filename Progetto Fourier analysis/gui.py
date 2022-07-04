from fileinput import filename
import PySimpleGUI as sg
import os.path
from PIL import Image, ImageTk


# first the windown layout in 2 columns

file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size = (25, 1), enable_events=True, key = '-FOLDER-', expand_x=True, expand_y=True),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values = [], enable_events=True, size = (40, 20), key = "-FILE LIST-", expand_x=True, expand_y=True
        ),
    ],
]


# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-", size = (30, 30), expand_x=True, expand_y=True)],
]


# Full layout
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeparator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Image viewer", layout=layout, resizable=True, finalize=True)

# Evento loop:
while True:
    event, values = window.read()
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break

    # folder name was filled in, make a list of files in the folder 
    if event == '-FOLDER-':
        folder = values['-FOLDER-']
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []
            print(f'[X] Error while reading files from {folder}')

        fnames = [
            f for f in file_list 
            if os.path.isfile(os.path.join(folder, f)) 
            and f.lower().endswith(('.png', '.gif', '.bpm'))
        ]
        window['-FILE LIST-'].update(fnames)

    # when a file is chosen from the list block
    elif event == '-FILE LIST-':
        try:
            filename = os.path.join(
                values['-FOLDER-'], values['-FILE LIST-'][0]
            )
            
            # Opening file
            # Resize PNG file to size (300, 300)
            size = (300, 300)
            im = Image.open(filename)
            im = im.resize(size, resample=Image.BICUBIC)

            # Convert im to ImageTk.PhotoImage after window finalized
            image = ImageTk.PhotoImage(image=im)
            
            # Update
            window['-TOUT-'].update(filename)
            window['-IMAGE-'].update(data=image)
        except:
            print(f'[X] Error while showing image {filename}')

window.close()














