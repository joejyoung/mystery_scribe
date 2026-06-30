import cv2
import numpy as np
import pytesseract
import easyocr

def preprocess(cell: np.ndarray, scale: int = 3) -> np.ndarray:
    big = cv2.resize(cell, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(big, cv2.COLOR_BGR2GRAY)
    _, thr = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if np.mean(thr) < 127:
        thr = cv2.bitwise_not(thr)
    return thr

def read_number(cell: np.ndarray) -> str:
    c = "--psm 7 -c tessedit_char_whitelist=0123456789,"
    return pytesseract.image_to_string(preprocess(cell), config=c).strip().replace(',', '')

def read_name(cell: np.ndarray) -> str:
    reader = easyocr.Reader(["en"], gpu=True)
    res = reader.readtext(cell, detail=0)
    return res