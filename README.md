# OpenEye - Korean Vocabulary Extractor

Ứng dụng trích xuất từ vựng tiếng Hàn từ hình ảnh có khung viền đỏ.

## Tính năng chính

- **Trích xuất từ vựng**: Nhận diện và trích xuất từ vựng tiếng Hàn từ các khung viền đỏ trong ảnh
- **Giao diện thân thiện**:
  - Hỗ trợ chọn file ảnh
  - Paste ảnh trực tiếp (Ctrl+V)
  - Xem trước ảnh
  - Hiển thị kết quả trích xuất
- **Lưu trữ kết quả**: Lưu danh sách từ vựng ra file text

## Cài đặt

1. Cài đặt Tesseract-OCR:

   - Tải và cài đặt [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki)
   - Chọn thêm gói ngôn ngữ Korean trong quá trình cài đặt
   - Cài đặt vào đường dẫn mặc định: `C:\Program Files\Tesseract-OCR`

2. Cài đặt các thư viện Python cần thiết:
   bash
   pip install -r requirements.txt

## Cách sử dụng

1. Chạy ứng dụng:

   - Chạy file `KoreanVocabExtractor.exe`
   - Hoặc chạy từ source: `python korean_vocab_extractor_gui.py`

2. Nhập ảnh:

   - Click nút "Select Image" để chọn file ảnh
   - Hoặc copy ảnh và paste (Ctrl+V) trực tiếp vào ứng dụng

3. Xem và lưu kết quả:

   - Các từ được trích xuất sẽ hiển thị trong khung "Extracted Words"
   - Click "Save Results" để lưu kết quả ra file text

4. Xóa ảnh hiện tại:
   - Click "Clear Image" để xóa ảnh và kết quả hiện tại

## Yêu cầu hệ thống

- Windows 10/11
- [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki) với gói ngôn ngữ tiếng Hàn
- Các thư viện Python trong file requirements.txt

## Lưu ý

- Ảnh đầu vào cần có các từ/cụm từ được khoanh viền đỏ
- Đảm bảo Tesseract-OCR được cài đặt đúng đường dẫn
- Kích thước ảnh tối ưu: 800x600 pixels
⌢传数䕮敹•਍