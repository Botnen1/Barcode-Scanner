import tkinter as tk
import webbrowser
import cv2
from threading import Thread
import os
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np
from tkinter import filedialog


# Window main
window = tk.Tk()
window.title('BarcodeSearcher - Botnen')
window.geometry('500x700')

# Upload file function
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
        skrivefelt.delete(0, tk.END)
        skrivefelt.insert(0, barcode_val)
        search_in_browser(barcode_val)
    else:
        print('No barcode found in the uploaded image.')


def search_in_browser(barcode_val):
    search_link = f'https://www.google.com/search?q={barcode_val}'
    webbrowser.open(search_link)


def decode_barcode(pil_image):
    # Decode the barcode using pyzbar directly on the PIL Image
    barcodes = decode(pil_image)
    if barcodes:
        # Assuming there's only one barcode in the image
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
                # Convert the image to a PIL image for pyzbar to decode
                pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                barcode_value = decode_barcode(pil_image)
                
                if barcode_value:
                    # If a barcode is found, insert it into the entry field
                    skrivefelt.delete(0, tk.END)
                    skrivefelt.insert(0, barcode_value)
                    # Call the enter function to search for the barcode
                    enter()
                
            elif key & 0xFF == ord('q'):
                break
    
    capture.release()
    cv2.destroyAllWindows()

# Scan for new code function
def scan():
    print('scan-button clicked...')
    Thread(target=camera_ON).start()

# Enter function
def enter():
    kode = skrivefelt.get()
    print(f'Enter button clicked... Entry content: "{kode}"')
    if kode:
        søkelink = f'https://www.google.com/search?q={kode}'
        print(f'Searching for: {søkelink}')
        webbrowser.open(søkelink)
    else:
        print('Entry field is empty. No search performed.')


# Frame for upload and scan buttons
frame_buttons = tk.Frame(window)
frame_buttons.pack()

button_upload = tk.Button(frame_buttons, text='Upload', command=upload_image)
button_upload.pack(side=tk.LEFT, padx=5, pady=5)

button_scan = tk.Button(frame_buttons, text='Scan', command=scan)
button_scan.pack(side=tk.LEFT, padx=5, pady=5)


# Frame for entry and enter button
frame_entry = tk.Frame(window)
frame_entry.pack(pady=10)  

skrivefelt = tk.Entry(frame_entry, width=50)
skrivefelt.pack(side=tk.LEFT, padx=(5, 0))

button_enter = tk.Button(frame_entry, text='Enter', command=enter)
button_enter.pack(side=tk.LEFT, padx=(5, 0))


window.mainloop()
