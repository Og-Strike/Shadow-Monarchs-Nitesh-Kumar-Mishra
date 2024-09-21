# Shadow-Monarchs-Bill-Wizard
# Bill Wizard

<img src="og2.png" alt="Project Logo" width="200"/>

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

2. Here are the required Imports:

    ```bash
    import kivy.py
    import kivymd.py
    import numpy.py
    ```

    You may need to install Tesseract OCR manually:

    ```bash
    sudo apt install tesseract-ocr
    ```

3. Ensure OpenCV is correctly installed:

    ```bash
    pip install opencv-python
    ```

## Usage

1. **Run the main script:**

    ```bash
    python main.py
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

