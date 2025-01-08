import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageGrab
import os
from korean_vocab_extractor import KoreanVocabExtractor
import io

class KoreanVocabExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Korean Vocabulary Extractor")
        self.root.geometry("1024x768")
        
        self.root.resizable(True, True)
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.extractor = KoreanVocabExtractor()
        
        # Create main frame with padding
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure main frame grid weights
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)  # Image preview row
        
        # Bind Ctrl+V to paste_image
        self.root.bind('<Control-v>', self.paste_image)
        
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Button frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky='ew')
        
        # Image selection button
        ttk.Button(button_frame, text="Select Image", command=self.select_image, width=15).pack(side=tk.LEFT, padx=5)
        
        # Clear image button
        ttk.Button(button_frame, text="Clear Image", command=self.clear_image, width=15).pack(side=tk.LEFT, padx=5)
        
        # Paste instruction label
        ttk.Label(button_frame, text="or Press Ctrl+V to paste image", font=('Arial', 10)).pack(side=tk.LEFT, padx=20)
        
        # Image preview in a frame with border
        preview_frame = ttk.LabelFrame(self.main_frame, text="Image Preview", padding="10")
        preview_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky='nsew')
        
        self.image_label = ttk.Label(preview_frame)
        self.image_label.pack(expand=True, fill='both')
        
        # Results area in a frame
        results_frame = ttk.LabelFrame(self.main_frame, text="Extracted Words", padding="10")
        results_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='ew')
        
        # Larger text area with scrollbar
        text_frame = ttk.Frame(results_frame)
        text_frame.pack(fill='both', expand=True)
        
        self.result_text = tk.Text(text_frame, height=12, width=60, font=('Arial', 11))
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Save button at bottom
        ttk.Button(self.main_frame, text="Save Results", command=self.save_results, width=15).grid(row=3, column=0, pady=10)

    def paste_image(self, event=None):
        try:
            # Get image from clipboard
            image = ImageGrab.grabclipboard()
            
            if image is None:
                print("No image in clipboard")
                return
                
            # Save temporary file
            temp_path = "temp_clipboard.png"
            image.save(temp_path)
            
            # Show image preview
            self.display_image(temp_path)
            
            # Process image
            self.process_image(temp_path)
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
        except Exception as e:
            print(f"Error processing clipboard image: {e}")
    
    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")]
        )
        if file_path:
            # Show image preview
            self.display_image(file_path)
            
            # Process image
            self.process_image(file_path)
    
    def display_image(self, image_path):
        # Load and resize image for preview
        image = Image.open(image_path)
        
        # Calculate size to maintain aspect ratio within 800x600
        max_size = (800, 600)
        ratio = min(max_size[0]/image.size[0], max_size[1]/image.size[1])
        new_size = tuple(int(dim * ratio) for dim in image.size)
        
        image = image.resize(new_size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        
        self.image_label.configure(image=photo)
        self.image_label.image = photo  # Keep a reference
    
    def process_image(self, image_path):
        # Clear previous results
        self.result_text.delete(1.0, tk.END)
        
        # Extract words
        extracted_words = self.extractor.extract_red_boxes(image_path)
        
        # Display results
        for i, word in enumerate(extracted_words, 1):
            self.result_text.insert(tk.END, f"{i}. {word}\n")
    
    def save_results(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            initialfile="extracted_words.txt"
        )
        if file_path:
            text = self.result_text.get(1.0, tk.END)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)

    def clear_image(self):
        # Clear image preview
        self.image_label.configure(image='')
        self.image_label.image = None
        
        # Clear results
        self.result_text.delete(1.0, tk.END)
        
        # Remove detected_boxes.jpg if it exists
        if os.path.exists('detected_boxes.jpg'):
            try:
                os.remove('detected_boxes.jpg')
            except Exception as e:
                print(f"Error removing detected_boxes.jpg: {e}")

def main():
    root = tk.Tk()
    app = KoreanVocabExtractorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 