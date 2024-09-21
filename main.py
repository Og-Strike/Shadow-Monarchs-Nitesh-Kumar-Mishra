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
from kivymd.uix.label import MDLabel
import cv2
import universal
import numpy as np
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
from kivy.uix.scrollview import ScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
import shutil
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class MainApp(MDApp):
    bg = r"og.jpg"
    ico = r"og2.png"
    i=0
    def build(self):
        self.icon = r"og2.png"
        Window.maximize()
        self.fields = {
            "Low": 100,
            "Low Mid": 250,
            "Mid": 500,
            "Mid High": 750,
            "High": 1000
        }
        self.create_folders()
        self.entered_values=self.fields
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "A700"
        self.theme_cls.accent_palette = "Cyan"
        self.theme_cls.accent_hue = "A700"
        self.theme_cls.theme_style = "Dark" 
        return Builder.load_string('''
MDBoxLayout:
    orientation: "vertical"
    MDTopAppBar:
        title: "Bill Wizard - Monarchs Edition"
        left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
        elevation: 10
    MDNavigationLayout:
        ScreenManager:
            id: screen_manager
            Screen:
                name: "Home"
                RelativeLayout:
                    orientation: 'vertical'
                    Image:
                        source: app.bg 
                        allow_stretch: True
                        keep_ratio: False
                        size_hint: None, None
                        size: self.parent.size
                        pos: self.parent.pos
                    MDLabel:
                        text: "1. Download IP Webcam App from play store."
                        pos_hint: {"center_x": 1.08, "center_y": 0.9}
                        color: 'cyan'
                    MDLabel:
                        text: "2. Open App in and scroll down and Click on 'Start Server' and Put IPv4 Url in below box. "
                        pos_hint: {"center_x": 1.08, "center_y": 0.8}
                        color: 'cyan'
                        multiline: True
                    MDLabel:
                        text: "Note: Make sure to connect both devices on the same network. "
                        pos_hint: {"center_x": 1.08, "center_y": 0.7}
                        color: 'cyan'
                    MDLabel:
                        text: "Url: "
                        pos_hint: {"center_x": 1.08, "center_y": 0.6}
                        color: 'cyan'
                    MDTextField:
                        id: text_input
                        hint_text: "Enter Url Of Phone Cam"
                        pos_hint: {"center_x": 0.7, "center_y": 0.6}
                        size_hint: 0.1,0.1
                    MDFillRoundFlatIconButton:
                        size_hint: 0.1,0.1
                        text: "Browse Video Process"
                        pos_hint: {"center_x": 0.3, "center_y": 0.65}
                        on_release: app.video()
                    MDFillRoundFlatIconButton:
                        size_hint: 0.1,0.1
                        text: "Phone Camera Process"
                        pos_hint: {"center_x": 0.7, "center_y": 0.4}
                        on_release: app.phonecam()
                    MDFillRoundFlatIconButton:
                        size_hint: 0.1,0.1
                        text: "Set Category Parameters"
                        pos_hint: {"center_x": 0.3, "center_y": 0.5}
                        on_release: app.create_fields_based_on_selection()
                    MDFillRoundFlatIconButton:
                        size_hint: 0.1,0.1
                        text: "Export to  XML"
                        pos_hint: {"center_x": 0.2, "center_y": 0.3}
                        on_release: app.convert_xml()
                    MDFillRoundFlatIconButton:
                        size_hint: 0.1,0.1
                        text: "Export to  json"
                        pos_hint: {"center_x": 0.4, "center_y": 0.3}
                        on_release: app.convert_json()
            Screen:
                name: "Data Retrive"
                RelativeLayout:
                    orientation: 'vertical'
                    Image:
                        source: app.bg 
                        allow_stretch: True
                        keep_ratio: False
                        size_hint: None, None
                        size: self.parent.size
                        pos: self.parent.pos
                    MDLabel:
                        text: "-->  Company : "
                        pos_hint: {"center_x": 0.1, "center_y": 0.6}
                        color: 'cyan'
                        size_hint: 0.1,0.1
                    MDTextField:
                        id: text_input1
                        hint_text: "Enter Company "
                        pos_hint: {"center_x": 0.2, "center_y": 0.6}
                        size_hint: 0.1,0.1
                    MDLabel:
                        text: "-->  Date : "
                        pos_hint: {"center_x": 0.1, "center_y": 0.5}
                        color: 'cyan'
                        size_hint: 0.1,0.1
                    MDTextField:
                        id: text_input2
                        hint_text: "Enter Date "
                        pos_hint: {"center_x": 0.2, "center_y": 0.5}
                        size_hint: 0.1,0.1
                    MDLabel:
                        text: "-->  Amount : "
                        pos_hint: {"center_x": 0.1, "center_y": 0.4}
                        color: 'cyan'
                        size_hint: 0.1,0.1
                    MDTextField:
                        id: text_input3
                        hint_text: "Enter Total Amount "
                        pos_hint: {"center_x": 0.2, "center_y": 0.4}
                        size_hint: 0.1,0.1
                    MDFillRoundFlatIconButton:
                        size_hint: 0.1,0.1
                        text: "Get Data"
                        pos_hint: {"center_x": 0.5, "center_y": 0.9}
                        on_release: app.filter_data()
                    RelativeLayout:
                        id: table_layout
                        orientation: 'vertical'
                                               
            Screen:
                name: "Anylisys"
                RelativeLayout:
                    orientation: 'vertical'
                    padding: dp(20)
                    spacing: dp(20)
                                   
                    Image:
                        source: app.bg 
                        allow_stretch: True
                        keep_ratio: False
                        size_hint: None, None
                        size: self.parent.size
                        pos: self.parent.pos

                    MDFillRoundFlatIconButton:
                        id: button
                        size_hint: 0.1,0.1
                        text: "Select Column"
                        pos_hint: {"center_x": .4, "center_y": .9}
                        on_release: app.menu_open()

                    MDTextField:
                        id: date_from
                        hint_text: "Date From"
                        size_hint_y: 0.1
                        size_hint_x: 0.2
                        pos_hint: {"center_x": .15, "center_y": .7}
                        on_focus: if self.focus: app.show_date_picker('from')

                    MDTextField:
                        id: date_to
                        hint_text: "Date To"
                        size_hint_y: 0.1
                        size_hint_x: 0.2
                        pos_hint: {"center_x": .85, "center_y": .7}
                        on_focus: if self.focus: app.show_date_picker('to')

                    MDFillRoundFlatIconButton:
                        size_hint: 0.1,0.1
                        text: "Show Graph"
                        pos_hint: {"center_x": 0.6, "center_y": 0.9}
                        on_release: app.show_bar_graph()

                    RelativeLayout:
                        id: graph_box
                        orientation: 'vertical'
                        pos_hint: {"center_x": 0.5, "center_y": 0.4}
                                   
            Screen:
                name: "AboutUs"
                RelativeLayout:
                    orientation: 'vertical'
                    RelativeLayout:
                        orientation: 'vertical'
                        Image:
                            source: app.bg 
                            allow_stretch: True
                            keep_ratio: False
                            size_hint: None, None
                            size: self.parent.size
                            pos: self.parent.pos
                        Image:
                            source: app.ico
                            pos_hint: {"center_x": 0.5, "center_y": 0.7}
                            size_hint: None, None
                            size: 400,400
                            spacing: [0, 50]
                        Label:
                            text: "Developer Name's: Strike, Night Wolf, er-adarsh"
                            font_size: "25sp"
                            color: "cyan"
                            bold: True
                            pos_hint: {"center_x": 0.5, "center_y": 0.4}
                        Label:
                            text: "Email: contact.monarchs.bill@gmail.com"
                            font_size: "25sp"
                            color: "cyan"
                            bold: True
                            pos_hint: {"center_x": 0.5, "center_y": 0.2}
        MDNavigationDrawer:
            id: nav_drawer
            BoxLayout:
                orientation: "vertical"
                Image:
                    source: app.ico
                MDList:
                    OneLineIconListItem:
                        text: "Home"
                        theme_text_color: "Custom" 
                        text_color: 0, 1, 1, 1 
                        on_press:
                            nav_drawer.set_state("close")
                            screen_manager.current = "Home"
                        IconLeftWidget:
                            icon: "home"
                            theme_text_color: "Custom" 
                            text_color: 0, 1, 1, 1 
                    OneLineIconListItem:
                        text: "Data Retrive"
                        theme_text_color: "Custom" 
                        text_color: 0, 1, 1, 1 
                        on_press:
                            nav_drawer.set_state("close")
                            screen_manager.current = "Data Retrive"
                        IconLeftWidget:
                            icon: "google-lens"
                            theme_text_color: "Custom" 
                            text_color: 0, 1, 1, 1 
                    OneLineIconListItem:
                        text: "Anylisys"
                        theme_text_color: "Custom" 
                        text_color: 0, 1, 1, 1 
                        on_press:
                            nav_drawer.set_state("close")
                            screen_manager.current = "Anylisys"
                        IconLeftWidget:
                            icon: "graph"
                            theme_text_color: "Custom" 
                            text_color: 0, 1, 1, 1 
                    OneLineIconListItem:
                        text: "About Us"
                        theme_text_color: "Custom" 
                        text_color: 0, 1, 1, 1  
                        on_press:
                            nav_drawer.set_state("close")
                            screen_manager.current = "AboutUs"
                        IconLeftWidget:
                            icon: "information"
                            theme_text_color: "Custom" 
                            text_color: 0, 1, 1, 1 
                    OneLineIconListItem:
                        text: "Feedback"
                        theme_text_color: "Custom" 
                        text_color: 0, 1, 1, 1 
                        on_press:
                            nav_drawer.set_state("close")
                            app.feedback()
                        IconLeftWidget:
                            icon: "comment-quote"
                            theme_text_color: "Custom" 
                            text_color: 0, 1, 1, 1 
                    OneLineIconListItem:
                        text: "Rate Us"
                        theme_text_color: "Custom" 
                        text_color: 0, 1, 1, 1 
                        on_press:
                            nav_drawer.set_state("close")
                            app.rate_us_link("com.akm_appmakers")
                        IconLeftWidget:
                            icon: "star"
                            theme_text_color: "Custom" 
                            text_color: 0, 1, 1, 1 
''')
    
    def convert_json(self):
        csv_file = filedialog.askopenfilename(title="Select an Image", filetypes=[("csv file", "*.csv ")])
        json_file = "daily_e.json"
        df = pd.read_csv(csv_file)
        df.to_json(json_file, orient="records", indent=4)
        toast(f" {json_file} created")

    def convert_xml(self):
        csv_file = filedialog.askopenfilename(title="Select an Image", filetypes=[("csv file", "*.csv ")])
        xml_file = "daily_e.xml"
        df = pd.read_csv(csv_file)
        root = ET.Element("Data")

        for _, row in df.iterrows():
            item = ET.SubElement(root, "Item")
            for col in df.columns:
                child = ET.SubElement(item, col)
                child.text = str(row[col])

        tree = ET.ElementTree(root)
        tree.write(xml_file, encoding='utf-8', xml_declaration=True)
        toast(f" {xml_file} created")
    
    def show_popup(self):
        title = "Not Valid URL"
        message = "Please Enter Valid URL"
        dialog = MDDialog(
            title=title,
            type="alert",
            text=message,
            size_hint=(0.8, 0.3),
            auto_dismiss=True,
            buttons=[
                MDFillRoundFlatIconButton(
                    text="Close",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def show_error_dialog(self,Message):
        self.dialog = MDDialog(
                title="Error",
                text=Message,
                buttons=[
                    MDFillRoundFlatIconButton(
                        text="Close",
                        on_release=lambda x: self.dialog.dismiss()
                    )
                ]
            )
        self.dialog.open()

    def create_fields_based_on_selection(self, *args):

        # Define the field labels and corresponding default values


        content = MDBoxLayout(orientation="vertical", spacing=10, adaptive_height=True)
        self.text_fields = {}

        # Create text fields for each category
        for field in self.fields.keys():
            text_field = MDTextField(
                hint_text=f"Enter {field} value",
                input_filter="float"
            )
            self.text_fields[field] = text_field
            content.add_widget(text_field)

        self.float_input_dialog = MDDialog(
            title="Enter Float Values",
            type="custom",
            content_cls=ScrollView(do_scroll_y=True, size_hint_y=None, height="400dp"),
            auto_dismiss=False,
            buttons=[
                MDRaisedButton(
                    text="Submit",
                    on_release=self.submit_values
                ),
            ],
        )
        self.float_input_dialog.content_cls.add_widget(content)
        self.float_input_dialog.open()

    def create_folders(self):
        # Create folders if they do not exist
        categories = ["Low", "Low Mid", "Mid", "Mid High", "High","None"]
        for category in categories:
            if not os.path.exists(category):
                os.makedirs(category)
                print(f"Folder '{category}' created.")

    def classify_value(self,value):
        # Classify the value into the corresponding category
        print(self.entered_values)
        if value >= self.entered_values["High"]:
            print("High")
            return "High"
        elif self.entered_values["Mid High"] <= value < self.entered_values["High"]:
            print("Mid High")
            return "Mid High"
        elif self.entered_values["Mid"] <= value < self.entered_values["Mid High"]:
            print("Mid")
            return "Mid"
        elif self.entered_values["Low Mid"] <= value < self.entered_values["Mid"]:
            print("Low Mid")
            return "Low Mid"
        elif 0 <= value < self.entered_values["Low Mid"]:
            print("Low")
            return "Low"
        else:
            print("None")
            return None
        
        

    def submit_values(self, *args):
        # Create folders
        self.create_folders()

        # Create a dictionary to store the entered or default values
        

        # Loop through the fields and assign entered or default values
        for key, text_field in self.text_fields.items():
            # If the field is empty, use the default value from self.fields
            if text_field.text:
                self.entered_values[key] = float(text_field.text)
            else:
                self.entered_values[key] = self.fields[key]  # Assign default value

        print("Entered Values:", self.entered_values)
        
        # self.classify_value()
        # Classify each entered value
  

        self.float_input_dialog.dismiss()
    
    def video(self):
        try:
            video_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.mp4")])
            command = ["python","webcam.py",f"{video_path}"]
            subprocess.run(command)
            filename="a.txt"
            float_value=0
            
            with open(filename, 'r') as file:
                value = file.read().strip()  # Read and remove any extra spaces/newlines
                float_value = float(value)  # Convert to float
                print(f"Value read from {filename} as float: {float_value}")
            st=self.classify_value(float_value)
            current_directory = os.path.dirname(os.path.abspath(__file__))

            new_folder_path = os.path.join(current_directory, st)

            # If the new folder does not exist, create it
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)

            # Get the new file path
            new_file_path = os.path.join(new_folder_path, f'{self.i}.png')
            self.i+=1

            # Copy the screenshot to the new folder with the new name
            shutil.copy("screenshot_1.png", new_file_path)
            print(f"Screenshot saved to: {new_file_path}")
                

        except Exception as e:
            self.show_error_dialog(str(e))

    def phonecam(self):
    
        url = self.root.ids.text_input.text
        ipv4_pattern = re.compile(
            r'^(http|https):\/\/'
            r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
            r'(:[0-9]{1,5})?$'
        )
        if re.match(ipv4_pattern, url):
            url = url + "/shot.jpg"
            try:
                command = ["python","phonecam.py",f"{url}"]
                subprocess.run(command)
            except Exception as e:
                self.show_error_dialog(str(e))
        else:
            self.show_popup()
    
    def menu_open(self):
        
        columns = ["Company", "Date"]
        menu_items = [
            {"text": f"{columns[i]}", "on_release": lambda x=f"{columns[i]}": self.menu_callback(x)}
            for i in range(len(columns))
        ]
        self.menu = MDDropdownMenu(caller=self.root.ids.button, items=menu_items)
        self.menu.open()


    def menu_callback(self, text_item):
        self.Column = text_item
        toast(f"Selected column {text_item}")
        if self.menu:  
            self.menu.dismiss()

    def show_date_picker(self,date_type):
        self.date_type = date_type
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        if self.date_type == 'from':
            self.root.ids.date_from.text = value.strftime('%Y-%m-%d')
        else:
            self.root.ids.date_to.text = value.strftime('%Y-%m-%d')

    def show_bar_graph(self):
        column_name = self.Column
        date_from_str = self.root.ids.date_from.text.strip()
        date_to_str = self.root.ids.date_to.text.strip()

        if not column_name:
            self.show_error_dialog("Please select a column.")
            return

        if not date_from_str or not date_to_str:
            self.show_error_dialog("Please select both 'Date From' and 'Date To'.")
            return

        try:
            # Parse selected dates
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d')
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d')

            # Validate date range
            if date_from > date_to:
                self.show_error_dialog("'Date To' must be later than 'Date From'.")
                return

            self.get_data(column_name,date_from,date_to)

        except KeyError:
            self.show_error_dialog("No Data Available for selected Column ")


    def get_data(self, column, datef, datet):
        # Path to the directory containing the CSV file
        current_directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(current_directory, 'daily_expenditure.csv')

        # Check if the file exists
        if os.path.exists(csv_file_path):
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_file_path)

            # Convert 'Date' column to datetime if it's not already in that format
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

            # Filter the DataFrame based on the date range
            filtered_df = df[(df['Date'] >= datef) & (df['Date'] <= datet)]

            if filtered_df.empty:
                self.show_error_dialog(f"No data available for '{column}' column within the specified date range.")
                return

            color_counts = filtered_df[column].value_counts()

            if color_counts.empty:
                self.show_error_dialog(f"No data available for '{column}' column within the specified date range.")
                return

            # Plot the bar graph
            plt.figure(figsize=(8, 6))
            plt.bar(color_counts.index, color_counts.values, align='center', alpha=0.5)
            plt.xlabel(column)
            plt.ylabel('Count')
            plt.title(f'{column} Trend')
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Save the graph and display it
            graph_filename = f'bar_graph_{self.i}.png'
            self.i += 1
            plt.savefig(graph_filename)

            # Display the image using Kivy's Image widget
            self.root.ids.graph_box.clear_widgets()
            self.root.ids.graph_box.add_widget(Image(source=graph_filename))

            # Optionally remove the graph image file after displaying
            os.remove(graph_filename)

        else:
            self.show_error_dialog( "daily_expenditure.csv file is not found in the directory. Type a valid file name.")

        
    def load_data(self, file):
        # Get the current directory and construct the file path
        current_directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(current_directory, f'daily_expenditure.csv')

        # Check if the file exists
        if os.path.exists(csv_file_path):
            # Load the CSV data into a pandas DataFrame
            df = pd.read_csv(csv_file_path)
            return df
        else:
            self.show_error_dialog(f"{file} file is not found in the directory.")
            return pd.DataFrame()  # Return an empty DataFrame if the file doesn't exist

    def filter_data(self):
        file = "daily_expenditure.csv"

        if True:
            # Load data from the CSV file
            data_df = self.load_data(file)

            if data_df.empty:
                self.show_error_dialog(f"No data available in {file}")
                return
            else:
                # Create a dictionary for filters based on input fields
                filters = {
                    "Company": self.root.ids.text_input1.text.strip(),
                    "Date": self.root.ids.text_input2.text.strip(),
                    "Total Amount": self.root.ids.text_input3.text.strip(),
                }

                # Filter the DataFrame based on user inputs
                filtered_df = data_df.copy()
                for key, value in filters.items():
                    if value:
                        filtered_df = filtered_df[filtered_df[key].str.contains(value, case=False, na=False)]

                self.update_table(filtered_df)
        else:
            self.show_error_dialog(f"daily_expenditure.csv file is not there in the database. Type a valid file name.")

    def update_table(self, df):
        table_layout = self.root.ids.table_layout
        table_layout.clear_widgets()

        if df.empty:
            table_layout.add_widget(MDLabel(text="No matching records found.", color="cyan"))
            return

        # Create and display the data table
        data_table = MDDataTable(
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.6, 'center_y': 0.5},
            column_data=[
                ("Index", dp(30)),
                ("Company", dp(30)),
                ("Date", dp(30)),
                ("Total Amount", dp(30)),
                ("Tax Amount", dp(30)),
                ("GST", dp(30))
            ]
        )

        table_layout.add_widget(data_table)

        # Add row data to the table
        k = 0
        for _, row in df.iterrows():
            row_text = (
                k, row['Company'], row['Date'], row['Total Amount'], row['Tax Amount'], row['GST']
            )
            data_table.row_data.append(row_text)
            k += 1

        self.lendata = len(data_table.row_data)
    
    
    def open_link(self,link):
        webbrowser.open(link)
    
    def rate_us_link(self,package_name):
        link = f"https://play.google.com/store/apps/details?id={package_name}"
        self.open_link(link)

    def feedback(self):
        link = "https://forms.gle/w143RjgNPP1GBNe37"
        self.open_link(link)
    
if __name__ == '__main__':
    MainApp().run()














