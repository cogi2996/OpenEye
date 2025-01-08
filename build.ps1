$env:Path += ";C:\Users\ADMIN\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts"

pyinstaller --onefile --windowed `
    --add-data "C:\Program Files\Tesseract-OCR;tesseract" `
    --hidden-import=PIL `
    --hidden-import=PIL._tkinter_finder `
    --name KoreanVocabExtractor `
    korean_vocab_extractor_gui.py

pause 