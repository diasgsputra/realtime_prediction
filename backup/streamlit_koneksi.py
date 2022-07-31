import pandas as pd
from pandas import DataFrame
import streamlit as st
import mysql.connector
import time
import numpy as np
import pyautogui as pg
import datetime
from PIL import Image

class koneksi :
    def ambil_data(self):
        try:
            mydb = mysql.connector.connect(
                host="103.102.153.194",
                user="db_dias",
                password="dias1234",
                database="db_dias"
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT t5,t4,t3,t2,t1,h,t,ch FROM realtime_hujan ORDER BY id DESC LIMIT 1")
            ch_result = mycursor.fetchone()
            return ch_result
        except:
            print("ambil data gagal")
    def ambil_menit(self):
        try:
            mydb = mysql.connector.connect(
                host="103.102.153.194",
                user="db_dias",
                password="dias1234",
                database="db_dias"
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT t5,t4,t3,t2,t1,h,t,ch FROM realtime_menit ORDER BY id DESC LIMIT 1")
            ch_result = mycursor.fetchone()
            return ch_result
        except:
            print("ambil data gagal")