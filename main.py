from tkinter import filedialog, simpledialog, messagebox
import webbrowser
import cv2
from threading import Thread
from pyzbar.pyzbar import decode
from PIL import Image
import tkinter as tk
import data
import customtkinter as ctk

window = ctk.CTk()
window.title('BarcodeSearcher - Botnen')
window.geometry('500x300')
window.iconbitmap('C:\Users\hansc\Downloads\BOTnen.ico')

def show_saved_codes():
    print('Show codes button clicked...')
    codes = data.load_data()
    codes_window = ctk.CTkToplevel(window)
    codes_window.title('Saved Codes')

    scrollbar = ctk.CTkScrollbar(codes_window)
    scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

    listbox = tk.Listbox(codes_window, yscrollcommand=scrollbar.set)

    for code in codes:
        listbox.insert(ctk.END, code.strip())  
    listbox.pack(side=ctk.LEFT, fill=ctk.BOTH)

    scrollbar.configure(command=listbox.yview)

def upload_image():
    print('upload-button clicked...')
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        print('No file was selected.')
        return
    else:
        print(f'File selected: {file_path}')

    pil_image = Image.open(file_path)
    print(f'Image opened: {pil_image}')

    barcode_val = decode_barcode(pil_image)
    if barcode_val:
        print(f'Barcode found: {barcode_val}')
        skrivefelt.delete(0, ctk.END)
        skrivefelt.insert(0, barcode_val)
        data.save_data(barcode_val)
        search_in_browser(barcode_val)
    else:
        print('No barcode found in the uploaded image.')

def search_in_browser(barcode_val):
    search_link = f'https://www.google.com/search?q={barcode_val}'
    webbrowser.open(search_link)

def decode_barcode(pil_image):
    barcodes = decode(pil_image)
    if barcodes:
        barcode_data = barcodes[0].data.decode('utf-8')
        print('Barcode data:', barcode_data)
        return barcode_data
    else:
        print('No barcode found')
        return None

def camera_ON():
    capture = cv2.VideoCapture(0)
    cv2.namedWindow("Scan - Press 'q' to close, 'c' to capture")

    while True:
        ret, frame = capture.read()
        if ret:
            cv2.imshow("Scan - Press 'q' to close, 'c' to capture", frame)

            key = cv2.waitKey(1)
            if key & 0xFF == ord('c'):
                pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                barcode_value = decode_barcode(pil_image)

                if barcode_value:
                    skrivefelt.delete(0, ctk.END)
                    skrivefelt.insert(0, barcode_value)
                    data.save_data(barcode_value)
                    enter()

            elif key & 0xFF == ord('q'):
                break

    capture.release()
    cv2.destroyAllWindows()

def scan():
    print('scan-button clicked...')
    Thread(target=camera_ON).start()

def enter():
    kode = skrivefelt.get()
    print(f'Enter button clicked... Entry content: "{kode}"')
    if kode:
        data.save_data(kode)
        search_link = f'https://www.google.com/search?q={kode}'
        print(f'Searching for: {search_link}')
        webbrowser.open(search_link)
    else:
        print('Entry field is empty. No search performed.')

frame_buttons = ctk.CTkFrame(window)  
frame_buttons.pack()

button_upload = ctk.CTkButton(frame_buttons, text='Upload', command=upload_image,fg_color='aquamarine4')  
button_upload.pack(side=ctk.LEFT, padx=5, pady=5)

button_scan = ctk.CTkButton(frame_buttons, text='Scan', command=scan, fg_color='aquamarine4') 
button_scan.pack(side=ctk.LEFT, padx=5, pady=5)

button_show_codes = ctk.CTkButton(frame_buttons, text='Show Saved Codes', command=show_saved_codes, fg_color='aquamarine4')  
button_show_codes.pack(side=ctk.LEFT, padx=5, pady=5)

frame_entry = ctk.CTkFrame(window) 
frame_entry.pack(pady=10)

skrivefelt = ctk.CTkEntry(frame_entry, width=200) 
skrivefelt.pack(side=ctk.LEFT, padx=(5, 0))

button_enter = ctk.CTkButton(frame_entry, text='Enter', command=enter, fg_color='aquamarine4')  
button_enter.pack(pady=10)

window.mainloop()