import os
import pathlib
import PySimpleGUI as sg
import datetime


class Filefinder:

    def __init__(self):
        self.filedict = {}
        self.filelist = []
        self.filecount = 0
        self.sortedlist = []
        self.outputstring = ''

    def search_file_ext(self, rootpath):
        self.filedict.clear()
        self.filecount = 0
        self.sortedlist.clear()
        self.filelist.clear()
        self.outputstring = ''

        for root, dirs, files in os.walk(rootpath):
            for file in files:
                self.filecount += 1
                ext = pathlib.Path(file).suffix
                if ext == '':
                    ext = 'None'
                self.filedict[ext] = self.filedict.get(ext, 0) + 1
                print(file)

        for k, v in self.filedict.items():
            format = f'{k} {v}'
            self.filelist.append(format)

        self.sortedlist = sorted(self.filelist, key=sorter, reverse=True)

        self.outputstring = 'Scan result'.center(50, '*') + f'\n'
        self.outputstring = self.outputstring + f'Root: {rootpath} \n'
        self.outputstring = self.outputstring + f'Total number of files: {self.filecount} \n \n'
        self.outputstring = self.outputstring + 'Extension' + 'Files'.rjust(26) + f'\n'

        for value in self.sortedlist:
            split = value.split()
            rowlength = 34 - len(split[0])
            self.outputstring = self.outputstring + split[0] + split[1].rjust(rowlength, '.') + f'\n'

    def write_result_to_file(self, resultstring):
        now = datetime.datetime.now()
        filename = now.strftime("%Y-%m-%d_%H_%M_%S") + '.txt'
        outputfile = open(filename,'w')
        outputfile.write(resultstring)
        print(f'Printed output to {filename}')


def sorter(lista):
    return int(lista.split()[1])


cwd = os.getcwd()
search = Filefinder()

sg.theme('Dark')

layout = [[sg.Text("Choose root path "), sg.Input(cwd),sg.FolderBrowse(key="-PATH-", initial_folder=cwd),sg.Button("Start scan", button_color='Red')]
    ,[[sg.Text("Get result as txt-file: "), sg.Radio('Yes', group_id='fileradio', key="-Textfile-", default=False), sg.Radio('No', group_id='fileradio', default=True)]]
   ,[sg.Output(size=(100, 300), key=('_output_'), font='Consolas')]]
window = sg.Window('File Runner v 1.0', layout, size=(600, 500))


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "Start scan":
        print('TESTAR')
        print(values["-PATH-"])
        if values["-PATH-"] == '':
            search.search_file_ext(cwd)
            window.FindElement('_output_').Update('')
            print(search.outputstring)
        else:
            search.search_file_ext(values["-PATH-"])
            window.FindElement('_output_').Update('')
            print(search.outputstring)
        if values['-Textfile-'] is True:
            search.write_result_to_file(search.outputstring)
