'''
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
'''

import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from functools import partial
import hashlib

TITLE = 'Hash Generator'
GEN_TEXT = 'gen_text'
GEN_FILE = 'gen_file'
SHA_256 = 'SHA-256'
MD5 = 'MD5'
ICON = r'lock.ico'


# ROOT OPTIONS

root = tk.Tk()
root.title(TITLE)
root.iconbitmap(ICON)

# radio buttons
input_mode = tk.StringVar()
hash_alg = tk.StringVar()
hash_alg.set(SHA_256)


def open_file(*args, file_name=None):
    if not file_name:
        file_name = filedialog.askopenfilename()
    gen_file_entry.delete(0, tk.END)
    gen_file_entry.insert(0, file_name)
    with open(file_name, 'rb') as file:
        get_txt_hash(txt=file.read())


def change_mode(*args, mode=None):
    output_frame_result.configure(text='')
    if mode == GEN_TEXT:
        gen_txt_button.configure(state=tk.NORMAL)
        input_mode.set(GEN_TEXT)
        gen_txt_entry_scrolledtext.configure(state=tk.NORMAL, bg='white')
        gen_file_entry.configure(state=tk.DISABLED)
    elif mode == GEN_FILE:
        gen_txt_button.configure(state=tk.DISABLED)
        input_mode.set(GEN_FILE)
        gen_txt_entry_scrolledtext.configure(state=tk.DISABLED, bg='grey95')
        gen_file_entry.configure(state=tk.NORMAL)
    else:
        raise Exception(f'{mode} is not a valid mode.')


def change_alg(*args):
    if input_mode.get() == GEN_TEXT:
        get_txt_hash(txt=gen_txt_entry_scrolledtext.get('1.0', 'end-1c').encode('utf-8'))
    elif input_mode.get() == GEN_FILE:
        open_file(file_name=gen_file_entry.get())  # There is a problem here


def get_txt_hash(*args, txt=None):
    if hash_alg.get() == SHA_256:
        output_frame_result.configure(text=hashlib.sha256(txt).hexdigest())
    elif hash_alg.get() == MD5:
        output_frame_result.configure(text=hashlib.md5(txt).hexdigest())


title_lbl = tk.Label(root, text=TITLE, font=('fixedsys', 20)).pack()

gen_txt_radio_button = tk.Radiobutton(root,
                                      text='Generate from text',
                                      variable=input_mode,
                                      value=GEN_TEXT,
                                      command=lambda: [change_mode(mode=GEN_TEXT), gen_txt_entry_scrolledtext.focus()],
                                      anchor=tk.W)
gen_txt_radio_button.pack(fill=tk.X)

gen_txt_entry_frame = tk.Frame(root)
gen_txt_entry_frame.pack(fill=tk.X)
gen_txt_entry_scrolledtext = scrolledtext.ScrolledText(gen_txt_entry_frame, width=64, height=5)
gen_txt_entry_scrolledtext.bind('<1>', partial(change_mode, mode=GEN_TEXT))
gen_txt_entry_scrolledtext.pack(side=tk.LEFT)
gen_txt_button = tk.Button(gen_txt_entry_frame,
                           text='Get Hash',
                           command=lambda: get_txt_hash(txt=gen_txt_entry_scrolledtext.get('1.0', 'end-1c').encode('utf-8')))
gen_txt_button.pack(side=tk.RIGHT, fill=tk.Y)

gen_file_radio_button = tk.Radiobutton(root,
                                       text='Generate from file',
                                       variable=input_mode,
                                       value=GEN_FILE,
                                       command=lambda: [change_mode(mode=GEN_FILE), gen_file_entry.focus()],
                                       anchor=tk.W)
gen_file_radio_button.pack(fill=tk.X)

gen_file_entry_frame = tk.Frame(root)
gen_file_entry_frame.pack(fill=tk.X)
gen_file_entry = tk.Entry(gen_file_entry_frame, width=88)
gen_file_entry.pack(side=tk.LEFT, fill=tk.X)
gen_file_entry.bind('<1>', partial(change_mode, mode=GEN_FILE))
gen_file_entry.bind('<Return>', lambda: open_file(file_name=gen_file_entry.get()))
gen_file_entry_browse_btn = tk.Button(gen_file_entry_frame,
                                      text='Browse', width=7,
                                      command=lambda: [change_mode(mode=GEN_FILE), open_file()])
gen_file_entry_browse_btn.pack(side=tk.RIGHT)

sel_alg_frame = tk.Frame(root)
sel_alg_frame.pack(fill=tk.X)
sel_alg_sha256_radio_button = tk.Radiobutton(sel_alg_frame,
                                             text=SHA_256,
                                             variable=hash_alg,
                                             value=SHA_256,
                                             command=change_alg)
sel_alg_sha256_radio_button.pack(side=tk.LEFT)
sel_alg_MD5_radio_button = tk.Radiobutton(sel_alg_frame, text=MD5, variable=hash_alg, value=MD5, command=change_alg)
sel_alg_MD5_radio_button.pack(side=tk.LEFT)

output_title_lbl = tk.Label(root, text='Result:', anchor=tk.W)
output_title_lbl.pack(fill=tk.X)

output_frame = tk.Frame(root)
output_frame.pack(fill=tk.X)
output_frame_result = tk.Label(output_frame, text='')
output_frame_result.pack()

root.after(0, lambda: change_mode(mode=GEN_TEXT))
root.mainloop()
