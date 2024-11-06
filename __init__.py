# You need libs below...

import numpy as np
from os import path
from PIL import Image
from time import sleep
import onnxruntime as ort
from colorama import Fore
from fuzzywuzzy import fuzz
from threading import Thread
from ultralytics import YOLO
from paddleocr import PaddleOCR
import selenium.webdriver as wb
from selenium.webdriver.common.by import By
import sys, cv2, ddddocr, json, logging, re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

logging.disable(logging.DEBUG | logging.WARNING)
