# Shadow-Monarchs-Bill-Wizard
# Bill Wizard

<img src="og2.png" alt="Project Logo" width="100"/>

**Bill Wizard** is a robust tool designed to process store receipts through video input, leveraging OCR technology to extract data and generate insightful graphs. This project was developed for the **Lens Xplore Hackathon** by our team:

- **Nitesh Kumar Mishra**
- **Aryan Pathak**
- **Adarsh Kumar Thakur**

## Features

- **Capture Video Input**: Uses OpenCV to capture multiple receipts appearing in a video frame.
- **OCR Processing**: Utilizes Tesseract to process the text from the receipts.
- **Data Extraction & Storage**: Extracts receipt data such as store name, items, prices, dates, etc., and stores them in a CSV file.
- **Graph Generation**: Creates visual insights based on:
  - Expenditure
  - Dates
  - Stores
- **Handles Multiple Receipts**: Efficiently processes multiple receipts in one video stream.

## Technologies Used

- **OpenCV**: For capturing video frames.
- **Tesseract OCR**: For extracting text from the receipts.
- **Python**: Core logic implementation.
- **Matplotlib & Seaborn**: For generating graphs.
- **Pandas**: For storing and managing the CSV data.
- **Kivymd**: For creating a visually stunning UI.

## Installation

1. Clone the repository:

    ```bash
    git clone https://https://github.com/Og-Strike/Shadow-Monarchs-Nitesh-Kumar-Mishra
    ```

2. Here are the required Imports for the UI:

    ```bash
    from kivy.lang import Builder
    from kivymd.app import MDApp
    from kivymd.uix.dialog import MDDialog
    from kivymd.uix.button import MDFillRoundFlatIconButton
    from kivymd.uix.toolbar import MDTopAppBar
    from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
    from kivymd.uix.navigationdrawer import MDNavigationDrawer
    from kivy.uix.screenmanager import ScreenManager, Screen
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.image import Image
    from kivy.core.window import Window
    from kivy.config import Config
    import time
    from datetime import datetime
    from ultralytics import YOLO
    import sys
    import os
    import logging
    import multiprocessing as mp
    import requests
    import imutils
    import subprocess
    import re
    import webbrowser
    from kivymd.uix.spinner import MDSpinner
    from kivymd.uix.menu import MDDropdownMenu
    from kivy.uix.dropdown import DropDown
    from kivymd.uix.pickers import MDDatePicker
    from kivymd.toast import toast
    from matplotlib import pyplot as plt
    import pandas as pd
    from oauth2client.service_account import ServiceAccountCredentials
    import gspread
    from kivy.properties import StringProperty
    from kivymd.uix.datatables import MDDataTable
    from kivy.metrics import dp
    from tkinter import filedialog, messagebox
    ```

    You may need to install Tesseract OCR manually:

    ```bash
    sudo apt install tesseract-ocr
    ```

3. Ensure main libraries are also correctly installed:

    ```bash
    import cv2
    import numpy as np
    import pytesseract
    from PIL import Image
    import pandas as pd
    import re
    import os
    import matplotlib.pyplot as plt
    import sys
    import argparse
    ```

## Usage

1. **Run the scripts:**

    ```bash
    python main.py #main script
    python ocr.py
    python phonecam.py
    python webcam.py
    data.py
    ```

2. **Provide video input**:

   - Use your device’s camera to scan receipts or provide a pre-recorded video of receipts.

3. **CSV Generation**:

   After processing, a CSV file will be generated containing:
   - Receipt details
   - Store names
   - Dates
   - Total amount spent

4. **Graph Generation**:

   Graphs based on the receipts' data will be saved in the `graphs` directory.
   
   ![Sample Graph](path_to_sample_graph_image)

## Project Structure

```bash
.
├── main.py               # Main script to run the project
├── requirements.txt      # List of dependencies
├── README.md             # Project readme file
├── data/                 # Directory for storing CSV files
├── graphs/               # Directory for storing generated graphs
└── utils/                # Utility functions for OCR, data extraction, etc.
```
