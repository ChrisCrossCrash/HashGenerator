"""
Hash Generator
Copyright (C) 2019 Christopher Kumm

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import hashlib

TITLE = 'Hash Generator'
TITLE_FONT = ('fixedsys', 20)
GET_HASH = 'Get Hash'
BROWSE = 'Browse'
COPY = 'Copy'
GEN_FROM_TEXT = 'Generate from text'
GEN_FROM_FILE = 'Generate from file'
BUTTON_WIDTH = max(len(BROWSE), len(GET_HASH), len(COPY))
BUFFER_SIZE = 65536

ICON = r'lock.ico'

# Boarder options
RELIEF = 'flat'  # flat, sunken, raised, groove, or ridge
BOARDER_WIDTH = 2
PADDING = 5


class App(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hashtext= tk.StringVar()
        self.filename = tk.StringVar() # TODO: get rid of this
        self.file = None

        self.alg_mode = tk.StringVar()
        self.alg_mode.set('sha256')
        self.input_mode = tk.StringVar()
        self.input_mode.set('text')

        self.title_label = tk.Label(self, text=TITLE, font=TITLE_FONT)
        self.algorithm_options = AlgorithmOptions(self)
        self.txt_input = TxtInput(self)
        self.file_input = FileInput(self)
        self.output = Output(self)

        self.title_label.pack(fill='x')
        self.algorithm_options.pack(side='left', anchor='n')
        self.txt_input.pack(fill='x')
        self.file_input.pack(fill='x')
        self.output.pack(fill='x')

    def hash_alg_changed(self):
        if self.input_mode.get() == 'text':
            self.get_hash_clicked()
        else:
            self.get_file_hash()

    def get_hash_clicked(self):
        self.input_mode.set('text')
        txt = self.txt_input.entry.get('1.0', 'end-1c')
        self.hashtext.set(hashlib.new(self.alg_mode.get(), bytes(txt, 'utf-8')).hexdigest())

    def browse_clicked(self):
        self.input_mode.set('file')
        self.file = filedialog.askopenfile(mode='rb')
        self.get_file_hash()

    def get_file_hash(self):
        hasher = hashlib.new(self.alg_mode.get())
        buffer = self.file.read(BUFFER_SIZE)
        self.filename.set(self.file.name)
        while buffer:
            hasher.update(buffer)
            buffer = self.file.read(BUFFER_SIZE)
        self.hashtext.set(hasher.hexdigest())

    def copy_clicked(self):
        self.update_clipboard()

    def update_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.hashtext.get())


class AlgorithmOptions(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.buttons = []
        algorithms = list(hashlib.algorithms_available)
        algorithms.sort()
        for algorithm in algorithms:
            if 'shake' not in algorithm:  # 'shake' algorithms need a length specified, so they are excluded.
                button = tk.Radiobutton(self,
                                        text=algorithm,
                                        variable=self.parent.alg_mode,
                                        value=algorithm,
                                        command=parent.hash_alg_changed)
                self.buttons.append(button)

    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        for button in self.buttons:
            button.pack(anchor='w')


class TxtInput(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.entry = scrolledtext.ScrolledText(self, height=5, width=64)
        self.btn = tk.Button(self,
                             text=GET_HASH,
                             width=BUTTON_WIDTH,
                             command=parent.get_hash_clicked)

    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        self.entry.pack(side='left', fill='x', expand=True)
        self.btn.pack(side='right', fill='y')


class FileInput(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.entry = tk.Entry(self, state='readonly', textvariable=parent.filename)
        self.button = tk.Button(self, text=BROWSE, width=BUTTON_WIDTH, command=parent.browse_clicked)

    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        self.button.pack(side='right')
        self.entry.pack(side='right', fill='x', expand=True)


class Output(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.entry = tk.Entry(self, state='readonly', textvariable=parent.hashtext)
        self.button = tk.Button(self, text=COPY, width=BUTTON_WIDTH, command=parent.copy_clicked)

    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        self.entry.pack(side='left', fill='x', expand=True)
        self.button.pack(side='left')


if __name__ == '__main__':
    root = tk.Tk()
    App(root).pack(fill='both', expand=True)
    root.mainloop()
