import cv2
import sys

def load_image(img_path):
    image = cv2.imread(img_path)

    if image is None:
        sys.exit(f"Unable to find image in path {img_path}")

    grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(grey_img)
    blur = cv2.GaussianBlur(invert, (21, 21), 0)
    invertedblur = cv2.bitwise_not(blur)
    sketch = cv2.divide(grey_img, invertedblur, scale=256.0)
    flipped_img = cv2.flip(sketch, 0) # Mirror the image so the 3D printer will draw it in the correct orientation
    return flipped_img

def resize_image(img, width, height):
    return cv2.resize(img, (width, height))