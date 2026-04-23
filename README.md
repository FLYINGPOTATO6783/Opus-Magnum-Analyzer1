# 🧪 Opus Magnum Analyzer

An automated OCR tool designed for **Opus Magnum** (by Zachtronics). This application allows users to upload screenshots of their level completions and instantly compares their **Cost**, **Cycles**, and **Area** against the absolute global theoretical minimums (Pareto Frontier).



This program will only recognize puzzles from the main game (acts 1-5), not recognizing journal puzzles or DLC.



## 🚀 Features
- **OCR Detection:** Uses Tesseract OCR and OpenCV to read statistics directly from game screenshots.
- **Fuzzy Matching:** Implements `difflib` to correctly identify level names even if the OCR makes minor reading errors.
- **Global Benchmarks:** Includes a comprehensive library of world-record minimums for Acts 1 through 5.
- **Instant Feedback:** Calculates the "delta" (difference) between your score and the world record.



## 🛠️ Requirements

To run this project locally, you will need:

1. **Python 3.10+**
2. **Tesseract OCR:** - You must install the Tesseract engine on your OS.
   - [Download Tesseract for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
   - *Note: Ensure the Tesseract path in the code matches your installation directory.*
3. **Dependencies:**
   Install the required Python libraries using:
   ```bash
   pip install -r requirements.txt
<img width="589" height="511" alt="Screenshot 2026-04-19 190342" src="https://github.com/user-attachments/assets/8e80ae66-e41c-4d1d-8d94-d040af0f228b" />
## ⚖️ Disclaimer
World records in Opus Magnum are constantly evolving. The records stored in this app reflect the Pareto Frontier minimums as of April 2026.



EXAMPLE GIF


<img width="826" height="647" alt="Opus Magnum - Hair Product (150G, 50, 14, 2026-04-12-12-58-20)" src="https://github.com/user-attachments/assets/2af07965-6c7d-49ee-bec8-5c5e1a334f09" />



