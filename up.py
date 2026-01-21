def prg():
    import cv2
    import pytesseract
    import os

    # Set the path to your Tesseract installation
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    def detect_plate():
        """ Detects number plate and saves cropped image """
        harcascade = "model/haarcascade_russian_plate_number.xml"

        if not os.path.exists(harcascade):
            print("Error: Haarcascade file not found!")
            return None

        plate_cascade = cv2.CascadeClassifier(harcascade)
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not access the webcam")
            return None

        cap.set(3, 640)
        cap.set(4, 480)
        min_area = 500
        output_dir = "plates"
        os.makedirs(output_dir, exist_ok=True)

        print("Press 's' to save the plate when detected, or 'q' to quit.")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            img_roi = None
            for (x, y, w, h) in plates:
                if w * h > min_area:
                    img_roi = frame[y:y + h, x:x + w]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, "Plate Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
                    cv2.imshow("Detected Plate", img_roi)

            cv2.imshow("Webcam", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('s') and img_roi is not None:
                image_path = os.path.join(output_dir, "plate.jpg")
                cv2.imwrite(image_path, img_roi)
                print(f"Plate image saved to {image_path}")
                cap.release()
                cv2.destroyAllWindows()
                return image_path

            if key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return None

    def ocr_core(image_path):
        """ Extract text from image using Tesseract OCR """
        img = cv2.imread(image_path)
        if img is None:
            print("Error: Could not load image for OCR")
            return ""

        # Preprocessing for better OCR
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Noise reduction

        # Optional: increase contrast
        gray = cv2.equalizeHist(gray)

        # Resize image for better OCR
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # OCR configuration
        config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

        text = pytesseract.image_to_string(gray, config=config).strip()
        return text

    # Run the full process
    image_path = detect_plate()
    if image_path:
        print("Running OCR...")
        extracted_text = ocr_core(image_path)
        print("Extracted Plate Number:", extracted_text)
        return extracted_text
    else:
        print("No plate image captured.")
        return None
