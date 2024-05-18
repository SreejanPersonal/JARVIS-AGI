import cv2

def realtime_vision(image_path: str="ASSETS/captured_image.png") -> str:
    """
        Capture and save a real-time image from the default camera.

        Args:
            image_path (str): The path where the captured image will be saved.
                            Defaults to "captured_image.png".

        Returns:
            str: The path where the captured image is saved.
    """

    print("\033[92m" + "Turned on Realtime Vision. Capturing Image.\033[0m")
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite(image_path, frame)
    print("\033[92m" + "Image captured.....\033[0m")

    cap.release()  # Release the camera resource
    cv2.destroyAllWindows()  # Close OpenCV windows
    return image_path

if __name__ == '__main__':
    realtime_vision()