import cv2
import sys
import pytesseract
import re
import difflib
import customtkinter as ctk
from tkinter import filedialog
import os




#finds tesseract-OCR folder
if getattr(sys, 'frozen', False):
    #if exe
    application_path = sys._MEIPASS
else:
    #if regular.py script
    application_path = os.path.dirname(os.path.abspath(__file__))

tesseract_path = os.path.join(application_path, 'Tesseract-OCR', 'tesseract.exe')

pytesseract.pytesseract.tesseract_cmd = tesseract_path

records = {
    # --- ACT 1: LIFE IN A GREAT HOUSE ---
    "REFINED GOLD": [40, 62, 6],
    "FACE POWDER": [40, 26, 7],
    "WATERPROOF SEALANT": [30, 26, 8],
    "HANGOVER CURE": [40, 38, 8],
    "AIRSHIP FUEL": [40, 19, 10],
    "PRECISION MACHINE OIL": [60, 27, 11],
    "HEALTH TONIC": [30, 26, 15],
    "STAMINA POTION": [60, 27, 18],

    # --- ACT 2: UNPRECEDENTED ACTIONS ---
    "HAIR PRODUCT": [30, 41, 6],
    "ROCKET PROPELLANT": [40, 33, 11],
    "MIST OF INCAPACITATION": [60, 26, 12],
    "EXPLOSIVE PHIAL": [60, 22, 11],
    "ARMOR FILAMENT": [50, 49, 20],
    "COURAGE POTION": [40, 26, 10],
    "SURRENDER FLARE": [60, 16, 12],

    # --- ACT 3: EXILE AND THIEVERY ---
    "ALCOHOL SEPARATION": [90, 16, 19],
    "WATER PURIFIER": [50, 32, 11],
    "SEAL SOLVENT": [70, 50, 17],
    "CLIMBING ROPE FIBER": [50, 74, 47],
    "WARMING TONIC": [40, 27, 19],
    "LIFE-SENSING POTION": [80, 28, 20],
    "VERY DARK THREAD": [75, 49, 52],

    # --- ACT 4: AN UNCOMMON ALLY ---
    "LITHARGE SEPARATION": [30, 23, 14],
    "STAIN REMOVER": [80, 51, 34],
    "SWORD ALLOY": [70, 100, 56],
    "INVISIBLE INK": [80, 50, 20],
    "PURIFIED GOLD": [55, 112, 10],
    "ALCHEMICAL JEWEL": [50, 75, 36],
    "GOLDEN THREAD": [45, 49, 54],

    # --- ACT 5: OPPOSING PLOTS ---
    "MIST OF HALLUCINATION": [65, 50, 22],
    "TIMING CRYSTAL": [40, 219, 46],
    "VOLTAIC COIL": [55, 49, 68],
    "UNSTABLE COMPOUND": [70, 63, 38],
    "CURIOUS LIPSTICK": [120, 111, 63],
    "UNIVERSAL SOLVENT": [140, 59, 47],
}

def analyze_opus_magnum(file_path):
    report = ""
    img = cv2.imread(file_path)

    if img is None:
        return "Error: Could not load image file."
    
    nx1, ny1, nx2, ny2 = 14, 600, 183, 625
    namecrop = img[ny1:ny2, nx1:nx2]

    gray = cv2.cvtColor(namecrop, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)


    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    inv = cv2.bitwise_not(thresh)



    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    cleaned_title_img = cv2.erode(inv, kernel, iterations=1)



    raw_title = pytesseract.image_to_string(cleaned_title_img, config='--psm 7').strip().upper()

    possible_matches = difflib.get_close_matches(raw_title, records.keys(), n=1, cutoff=0.6)

    if possible_matches:
        current_level = possible_matches[0]
        report += f"Detected Level: {current_level}\n"
        level_records = records[current_level]
    else:
        report += f"Level not recognized. (Read: '{raw_title})\n"
        current_level = "Unknown"
#setup tesseract


#load and crop
    
    x1, y1, x2, y2 = 411, 598, 804, 623
    crop = img[y1:y2, x1:x2]

#pre proccessing (easier for AI)
#convert to grayscale and threshhold(black and white) to see numbers easier
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

    smooth = cv2.bilateralFilter(gray, 9, 75, 75)

    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)



    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)


# Manual Wipe
    h_img, w_img = thresh.shape

    cv2.rectangle(thresh, (int(w_img*0.11), 0), (int(w_img*0.42), h_img), (255, 255, 255), -1)

    cv2.rectangle(thresh, (int(w_img*0.58), 0), (int(w_img*0.85), h_img), (255, 255, 255), -1)

    cv2.rectangle(thresh, (int(w_img*0.95), 0), (w_img, h_img), (255, 255, 255), -1)

    margin = int(h_img * 0.05)
    thresh = thresh[margin:h_img-margin, :]




    thresh = cv2.medianBlur(thresh, 3)


#OCR step(identification)
#config psm7 tells tesseract to see image as a line of text
    raw_text = pytesseract.image_to_string(thresh, config='--psm 7')

#cleaning the data
    try:
        found_numbers = re.findall(r'\d+', raw_text)

        if len(found_numbers) >=3:
   #assign first 3 numbers to variables
            my_cost = int(found_numbers[0])
            my_cycles = int(found_numbers[1])
            my_area = int(found_numbers[2])

            my_stats = [my_cost, my_cycles, my_area]

     #fetch world records
   
            wr = records[current_level]
            report += f"\n--- Analysis for {current_level} ---\n"
            categories = ["Cost", "Cycles", "Area"]

            for i in range(3):
                my_val = my_stats[i]
                wr_val = wr[i]
                cat_name = categories[i]

                diff = my_val - wr_val

                if diff == 0:
                    report += f"{cat_name}: {my_val} -- {cat_name} WORLD RECORD MATCHED!!!!\n"
                elif diff < 0:
                    report += f"{cat_name}: {my_val} -- YOU BEAT WORLD RECORD BY {abs(diff)}!!!!!!\n"
                else:
                    report += f"{cat_name}: {my_val} (+{diff} over record)\n"
            return report
    

        else:
            return f"Not enough numbers found. OCR saw: {raw_text}"


    

    except Exception as e:
        return f"Error: {e}"
    

class AnalyzerUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Opus Magnum Analyzer")
        self.geometry("600x500")

        #header
        self.header = ctk.CTkLabel(self, text="Opus Magnum Stats Improved", font=("Arial", 22, "bold"))
        self.header.pack(pady=20)

        #selection area
        self.main_frame = ctk.CTkFrame(self, width=500, height=200, border_width=2)
        self.main_frame.pack(pady=10)
        self.main_frame.pack_propagate(False)

        self.label = ctk.CTkLabel(self.main_frame, text="SELECT SOLUTION GIF", font=("Arial", 14))
        self.label.pack(pady=(40, 10))

        #The button
        self.select_button = ctk.CTkButton(self.main_frame, text="Choose File", command=self.open_file_dialog)
        self.select_button.pack(pady=20)

        #results box
        self.result_box = ctk.CTkTextbox(self, width=500, height=150, font=("Consolas", 14))
        self.result_box.pack(pady=20)

    def open_file_dialog(self):
        #opens windows file picker
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif"), ("All files", "*.*")]
        )
        if file_path:
            self.result_box.delete("0.0", "end")
            self.result_box.insert("0.0", f"Precessing {file_path.split('/')[-1]}...")
            self.update()
        #calls to analyze image
            report = analyze_opus_magnum(file_path)

        #display report in window
            self.result_box.delete("0.0", "end")
            self.result_box.insert("0.0", report)

if __name__ =="__main__":
    app = AnalyzerUI()
    app.mainloop()

    