import os
import cv2
from easyocr import Reader

# Initialize the OCR reader
reader = Reader(['en'])

def mileage_output():
    """
    This function activates the webcam to capture a vehicle dashboard image, compresses it, and uses OCR to extract text.
    It filters the text to identify and return the highest numeric mileage value within a valid range.
    If no valid mileage is found or an error occurs, it returns an appropriate error message.
    """

    try:
        # Open the camera
        cap = cv2.VideoCapture(0)  # 0 is the default camera

        if not cap.isOpened():
            raise Exception("Camera not accessible. Please check permissions or if the camera is connected.")

        print("Press 'c' to capture the image or 'q' to quit.")

        while True:
            ret, frame = cap.read()
            if not ret:
                raise Exception("Failed to capture image from the camera.")

            # Show the video feed
            cv2.imshow("Camera Feed", frame)

            # Wait for user to press 'c' to capture the image or 'q' to quit
            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):  # Capture the image
                original_image_path = "original_image.jpg"
                compressed_image_path = "compressed_image.jpg"

                # Save the original image
                cv2.imwrite(original_image_path, frame)
                print("Image captured successfully!")

                # Compress the image
                compressed_frame = cv2.resize(frame, (640, 480))  # Resize to 640x480
                cv2.imwrite(
                    compressed_image_path,
                    compressed_frame,
                    [cv2.IMWRITE_JPEG_QUALITY, 50],  # Set JPEG quality to 50%
                )
                print("Image compressed successfully!")
                break
            elif key == ord('q'):  # Quit
                raise Exception("User exited without capturing an image.")

        # Release the camera and close the window
        cap.release()
        cv2.destroyAllWindows()

        # Perform OCR on the compressed image
        if not os.path.exists(compressed_image_path):
            raise Exception("Compressed image file not found.")

        results = reader.readtext(compressed_image_path, detail=0)

        # Filter numbers without decimals and within the specified range
        mileage_candidates = [
            text for text in results
            if text.isdigit() and 0 <= int(text) <= 999999 and '.' not in text
        ]

        if mileage_candidates:
            mileage = max(mileage_candidates, key=int)  # Choose the largest number
            return f"Mileage: {mileage}"
        else:
            return "Mileage not found!"
    except Exception as e:
        # Release the camera and close the window in case of an error
        if 'cap' in locals() and cap.isOpened():
            cap.release()
            cv2.destroyAllWindows()
        return f"Error: {str(e)}"
