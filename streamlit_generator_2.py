import streamlit as st
import mysql.connector
import time
import numpy as np
import pyautogui as pg
import datetime
import random
from random import choices



class koneksi :
    i=0
    j=0
    h_population = [61, 62, 63, 64, 65,
                    66, 67, 68, 69, 70, 71,
                    72, 73, 74, 75, 76, 77,
                    78, 79, 80, 81, 82, 83,
                    84, 85, 86, 87, 88, 89, 90
                    ]
    h_weights = [0.01, 0.01, 0.01, 0.01, 0.01,
                    0.01, 0.01, 0.01, 0.01, 0.02, 0.02,
                    0.02, 0.02, 0.02, 0.025, 0.025, 0.025,
                    0.025, 0.025, 0.025, 0.025, 0.025, 0.05,
                    0.05, 0.05, 0.05, 0.05, 0.05, 0.3, 0.01
                    ]
    
    t_population = [21,22,23,24,25,
                    26,27,28,29,30,
                    31,32,33,34,35
                    ]
    t_weights = [0.05,0.05,0.05,0.1,0.1,
                0.1,0.1,0.1,0.05,0.05,
                0.05,0.05,0.05,0.05,0.05
                ]

    

    ch_population = [0,1,2]
    ch_weights = [0.98,0.015,0.005]

    sum_menit_h = 0.0
    sum_menit_t = 0.0
    sum_menit_ch = 0.0
    sum_jam_h = 0.0
    sum_jam_t = 0.0
    sum_jam_ch = 0.0
    mydb = mysql.connector.connect(
        host="103.102.153.194",
        user="db_dan",
        password="dan1313",
        database="db_dan"
    )
    now_m = datetime.datetime.now()
    past_minute = now_m.minute
    now_j = datetime.datetime.now()
    past_jam = now_m.hour
    while True :
        mycursor = mydb.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        now_m = datetime.datetime.now()
        now_j = datetime.datetime.now()
        
        st.write("i = "+str(i))
        
        h = choices(h_population, h_weights)
        h = h[0]
        t = choices(t_population, t_weights)
        t = t[0]
        ch = choices(ch_population, ch_weights)
        ch = ch[0]

        sql = ("INSERT INTO loghujan"
            "(id_alat,waktu,t,h,aero,speed,ldr,hujan,ch,note,reset)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)")
        val = ("C002",now, t, h, 0,0,895,860,ch,"ok",1)
        mycursor.execute(sql, val)

        mydb.commit()

        st.write(mycursor.rowcount, "record inserted.")
        st.write("ch = "+str(ch))
        time.sleep(1)

        sum_menit_h = sum_menit_h + h
        sum_menit_t = sum_menit_t + t
        sum_menit_ch = sum_menit_ch + ch
        i=i+1
        if now_m.minute>past_minute:
            past_minute = now_m.minute
            rata_menit_h = sum_menit_h/i
            rata_menit_t = sum_menit_t/i
            rata_menit_ch = sum_menit_ch/i
            sum_menit_h = 0.0
            sum_menit_t = 0.0
            sum_menit_ch = 0.0
            i=0;
        
