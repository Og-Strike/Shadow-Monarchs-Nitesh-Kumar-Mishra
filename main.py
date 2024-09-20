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
import cv2
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
from tkinter import filedialog, messagebox

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class MainApp(MDApp):
    bg = r"og.jpg"
    ico = r"og2.png"
    def build(self):
        self.icon = r"og2.png"
        Window.maximize()
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
                        pos_hint: {"center_x": 0.3, "center_y": 0.4}
                        on_release: app.video()
                    MDFillRoundFlatIconButton:
                        size_hint: 0.1,0.1
                        text: "Phone Camera Process"
                        pos_hint: {"center_x": 0.7, "center_y": 0.4}
                        on_release: app.phonecam()
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
                        text: "-->  Category : "
                        pos_hint: {"center_x": 0.1, "center_y": 0.6}
                        color: 'cyan'
                        size_hint: 0.1,0.1
                    MDTextField:
                        id: text_input1
                        hint_text: "Enter Category "
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
                        text: "-->  Company : "
                        pos_hint: {"center_x": 0.1, "center_y": 0.4}
                        color: 'cyan'
                        size_hint: 0.1,0.1
                    MDTextField:
                        id: text_input3
                        hint_text: "Enter Company "
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
    
    def video(self):
        try:
            video_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.mp4")])
            command = ["python","webcam.py",f"{video_path}"]
            subprocess.run(command)
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
        pass

    def show_date_picker(self):
        pass

    def show_bar_graph(self):
        pass

    def get_data(self):
        pass
        
    def load_data(self):
        pass

    def filter_data(self):
        pass
    
    
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














