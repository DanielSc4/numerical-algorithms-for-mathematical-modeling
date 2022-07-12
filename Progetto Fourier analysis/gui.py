from fileinput import filename
import PySimpleGUI as sg
import os.path
from PIL import Image, ImageTk

from compressor import main


font = ("Arial", 13)


# first the windown layout in 2 columns
file_list_column = [
    [
        sg.Text("Image Folder", font=font),
        sg.In(size = (25, 1), enable_events=True, key = '-FOLDER-', expand_x=True, expand_y=True),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values = [], enable_events=True, size = (50, 30), key = "-FILE LIST-", expand_x=True, expand_y=True
        ),
    ],
]


# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Choose an image from list on left:", font = font)],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-", size = (30, 30), expand_x=True, expand_y=True)],
]


max_F = 300
f_slider = [ 
    [sg.Text("Scegli un intero F:", font = font)],
    [sg.Slider(key = '-INTF-', range=(0, max_F), orientation='h', size=(70, 20), default_value = 100, enable_events = True)],
    [sg.Text("Scegli un intero d compreso tra 0 e 2F - 2:", font = font)],
    [sg.Slider(key = '-INTd-', range=(0, 2 * max_F - 2), orientation='h', size=(70, 20), default_value = 0, enable_events = True)],
    [sg.Button('Start', size=(8, 1), key='-START_KEY-')]
]


# Full layout
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeparator(),
        sg.Column(image_viewer_column),
        sg.VSeparator(),
        sg.Column(f_slider),
    ]
]

window = sg.Window("Image viewer", layout=layout, resizable=True, finalize=True, size=(1500, 600))

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
            and f.lower().endswith(('.png', '.gif', '.bmp'))
        ]
        window['-FILE LIST-'].update(fnames)

    # when a file is chosen from the list block
    elif event == '-FILE LIST-':
        try:
            filename = os.path.join(
                values['-FOLDER-'], values['-FILE LIST-'][0]
            )
            
            # Opening file
            # Resize PNG file to size (500, 500)
            size = (500, 500)
            img = Image.open(filename)

            basewidth = 500

            # im = im.resize(size, resample=Image.BICUBIC)
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)

            # Convert im to ImageTk.PhotoImage after window finalized
            image = ImageTk.PhotoImage(image=img)
            
            # Update
            window['-TOUT-'].update(filename)
            window['-IMAGE-'].update(data=image)
        except:
            print(f'[X] Error while showing image {filename}')
    elif event == '-INTF-':
        try:
            window['-INTd-'].update(range=(0, 2 * values['-INTF-'] - 2))
        except:
            print(f'[X] Error intF')
    elif event == '-START_KEY-':
        try:
            if values['-FILE LIST-']:
                print('hi')
                filename = os.path.join(values['-FOLDER-'], values['-FILE LIST-'][0])
                main(path_image = filename, F = int(values["-INTF-"]), d = int(values["-INTd-"]))
            else:
                print('Si, ma inserisci prima il file')
                print(f'Woooo {values["-INTF-"]}, {values["-INTd-"]}, {values["-FOLDER-"]}, {values["-FILE LIST-"]}')
        except Exception as e:
            print(f'[X] Error while starting \n{e}')
            print(f'Woooo {values["-INTF-"]}, {values["-INTd-"]}, {values["-FOLDER-"]}, {values["-FILE LIST-"]}')


window.close()














