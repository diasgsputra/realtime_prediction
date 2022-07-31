import numpy as np
from matplotlib import pyplot as plt
from JST_hujan import *
from bobot import *
import pandas as pd
import streamlit as st
#from bokeh.plotting import figure
from streamlit_koneksi import *
from PIL import Image
import datetime

# menciptakan objek dari kelas koneksi
st.set_page_config(
        page_title="Realtime rainfall prediction",
        layout="wide"
    )
placeholder = st.empty()
# konek = koneksi();
jst = JST();

bb = bobot_ann()
[V,W] = bb.bobot()
# st.write(V)
# st.write(W)

n_hidden = 8
n_output = 1

min_humidity = 61
maks_humidity = 90
min_tempC = 21
maks_tempC = 35
min_precipMM = 0
maks_precipMM = 2
min_precipMM_m = 0
maks_precipMM_m = 4
min_precipMM_j = 0
maks_precipMM_j = 10

k=0
# plt.axis([0, 10, 0, 50])

# now_m = datetime.datetime.now()
# past_minute = now_m.minute
mydb = mysql.connector.connect(
    host="103.102.153.194",
    user="db_dias",
    password="dias1234",
    database="db_dias"
)
mydb.autocommit = True

while True :
    time.sleep(1)
    
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT t5,t4,t3,t2,t1,h,t,ch FROM realtime_hujan ORDER BY id DESC LIMIT 1")
    realtime = mycursor.fetchone()

    # realtime = konek.ambil_data()
    realtime = np.array(realtime)

    r_t5 = realtime[0]
    r_t5 = r_t5.astype(np.int64)
    r_t4 = realtime[1]
    r_t4 = r_t4.astype(np.int64)
    r_t3 = realtime[2]
    r_t3 = r_t3.astype(np.int64)
    r_t2 = realtime[3]
    r_t2 = r_t2.astype(np.int64)
    r_t1 = realtime[4]
    r_t1 = r_t1.astype(np.int64)

    r_humidity = realtime[5]
    r_humidity = r_humidity.astype(np.int64)
    r_tempC = realtime[6]
    r_tempC = r_tempC.astype(np.int64)
    r_precipMM = realtime[7]
    r_precipMM = r_precipMM.astype(np.int64)

    r_t5 = round((r_t5-min_precipMM)/(maks_precipMM-min_precipMM),3)
    r_t4 = round((r_t4-min_precipMM)/(maks_precipMM-min_precipMM),3)
    r_t3 = round((r_t3-min_precipMM)/(maks_precipMM-min_precipMM),3)
    r_t2 = round((r_t2-min_precipMM)/(maks_precipMM-min_precipMM),3)
    r_t1 = round((r_t1-min_precipMM)/(maks_precipMM-min_precipMM),3)
    r_humidity = round((r_humidity-min_humidity)/(maks_humidity-min_humidity),3)
    r_tempC = round((r_tempC-min_tempC)/(maks_tempC-min_tempC),3)
    r_precipMM = round((r_precipMM-min_precipMM)/(maks_precipMM-min_precipMM),3)

    realtime_normalisasi = np.array([r_t5,r_t4,r_t3,r_t2,r_t1,r_humidity,r_tempC,r_precipMM])

    data_uji = realtime_normalisasi[0:7]
    output_sebenarnya = realtime_normalisasi[7]
    data_tampil = realtime[0:7]
    
    n_datauji = 1
    hasil_prediksi = np.zeros((n_datauji, 1))

    for j in range(n_datauji):
        [Z,Y] = jst.PerambatanMaju(data_uji,V,W,n_hidden,n_output)
        hasil_prediksi[j,0]=Y[0,0]
        

    minprecipMM = min_precipMM
    maksprecipMM = maks_precipMM

    hasilprediksi_denormalisasi = np.zeros((n_datauji,1))
    outputsebenarnya_denormalisasi = np.zeros((n_datauji,1))

    for i in range(n_datauji):
        hasilprediksi_denormalisasi[i,0]=jst.Denormalisasi(hasil_prediksi[i,0],
                                                       minprecipMM,maksprecipMM)
        outputsebenarnya_denormalisasi[i,0]=jst.Denormalisasi(output_sebenarnya,
                                                           minprecipMM,maksprecipMM)

    for i in range(n_datauji):
        hasiljst=hasilprediksi_denormalisasi[i,0]
        datasebenarnya=outputsebenarnya_denormalisasi[i,0]

        hasiljst = hasiljst - 0
        print("hasil jst detik : ",hasiljst)

        erorhasil=abs(hasiljst-datasebenarnya)
        
    ch_result = hasiljst
    print("hasil detik : ",ch_result)
    y2 = datasebenarnya
    
    ##################################### PREDIKSI MENIT #####################################
    mycursor = mydb.cursor()
    mycursor.execute("SELECT t5,t4,t3,t2,t1,h,t,ch FROM realtime_menit ORDER BY id DESC LIMIT 1")
    mrealtime = mycursor.fetchone()
    #print("mrealtime: ",mrealtime)
    # mrealtime = konek.ambil_menit()
    mrealtime = np.array(mrealtime)
    
    
    mr_t5 = mrealtime[0]
    mr_t5 = mr_t5.astype(np.int64)
    mr_t4 = mrealtime[1]
    mr_t4 = mr_t4.astype(np.int64)
    mr_t3 = mrealtime[2]
    mr_t3 = mr_t3.astype(np.int64)
    mr_t2 = mrealtime[3]
    mr_t2 = mr_t2.astype(np.int64)
    mr_t1 = mrealtime[4]
    mr_t1 = mr_t1.astype(np.int64)

    mr_humidity = mrealtime[5]
    mr_humidity = mr_humidity.astype(np.int64)
    mr_tempC = mrealtime[6]
    mr_tempC = mr_tempC.astype(np.int64)
    mr_precipMM = mrealtime[7]
    mr_precipMM = mr_precipMM.astype(np.int64)
    #print("mr_precip: ",mr_precipMM)

    mr_t5 = round((mr_t5-min_precipMM_m)/(maks_precipMM_m-min_precipMM_m),3)
    mr_t4 = round((mr_t4-min_precipMM_m)/(maks_precipMM_m-min_precipMM_m),3)
    mr_t3 = round((mr_t3-min_precipMM_m)/(maks_precipMM_m-min_precipMM_m),3)
    mr_t2 = round((mr_t2-min_precipMM_m)/(maks_precipMM_m-min_precipMM_m),3)
    mr_t1 = round((mr_t1-min_precipMM_m)/(maks_precipMM_m-min_precipMM_m),3)
    mr_humidity = round((mr_humidity-min_humidity)/(maks_humidity-min_humidity),3)
    mr_tempC = round((mr_tempC-min_tempC)/(maks_tempC-min_tempC),3)
    mr_precipMM = round((mr_precipMM-min_precipMM_m)/(maks_precipMM_m-min_precipMM_m),3)

    mrealtime_normalisasi = np.array([mr_t5,mr_t4,mr_t3,mr_t2,mr_t1,mr_humidity,mr_tempC,mr_precipMM])
    #print("mrealtime normalisasi: ",mrealtime_normalisasi)
    mdata_uji = mrealtime_normalisasi[0:7]
    moutput_sebenarnya = mrealtime_normalisasi[7]
    mdata_tampil = mrealtime[0:7]
    
    n_datauji = 1
    mhasil_prediksi = np.zeros((n_datauji, 1))

    for j in range(n_datauji):
        [Z,Y] = jst.PerambatanMaju(mdata_uji,V,W,n_hidden,n_output)
        mhasil_prediksi[j,0]=Y[0,0]
        print("mhasil_prediksi: ",mhasil_prediksi[j,0])
        

    minprecipMM = min_precipMM_m
    maksprecipMM = maks_precipMM_m

    mhasilprediksi_denormalisasi = np.zeros((n_datauji,1))
    moutputsebenarnya_denormalisasi = np.zeros((n_datauji,1))

    for i in range(n_datauji):
        mhasilprediksi_denormalisasi[i,0]=jst.Denormalisasi(mhasil_prediksi[i,0],
                                                       minprecipMM,maksprecipMM)
        moutputsebenarnya_denormalisasi[i,0]=jst.Denormalisasi(moutput_sebenarnya,
                                                           minprecipMM,maksprecipMM)

    for i in range(n_datauji):
        mhasiljst=mhasilprediksi_denormalisasi[i,0]
        mdatasebenarnya=moutputsebenarnya_denormalisasi[i,0]

        mhasiljst = mhasiljst - 0
        print("hasil jst menit : ",mhasiljst)

        merorhasil=abs(mhasiljst-mdatasebenarnya)
        
    menit_result = mhasiljst
    print("hasil menit : ",menit_result)
    y2 = mdatasebenarnya

    ################################## Prediksi Jam #################################

    ##################################### PREDIKSI JAM #####################################
    mycursor = mydb.cursor()
    mycursor.execute("SELECT t5,t4,t3,t2,t1,h,t,ch FROM realtime_jam ORDER BY id DESC LIMIT 1")
    jrealtime = mycursor.fetchone()
    #print("mrealtime: ",mrealtime)
    # mrealtime = konek.ambil_menit()
    jrealtime = np.array(jrealtime)
    
    
    jr_t5 = jrealtime[0]
    jr_t5 = jr_t5.astype(np.int64)
    jr_t4 = jrealtime[1]
    jr_t4 = jr_t4.astype(np.int64)
    jr_t3 = jrealtime[2]
    jr_t3 = jr_t3.astype(np.int64)
    jr_t2 = jrealtime[3]
    jr_t2 = jr_t2.astype(np.int64)
    jr_t1 = jrealtime[4]
    jr_t1 = jr_t1.astype(np.int64)

    jr_humidity = jrealtime[5]
    jr_humidity = jr_humidity.astype(np.int64)
    jr_tempC = jrealtime[6]
    jr_tempC = jr_tempC.astype(np.int64)
    jr_precipMM = jrealtime[7]
    jr_precipMM = jr_precipMM.astype(np.int64)
    #print("mr_precip: ",mr_precipMM)

    jr_t5 = round((jr_t5-min_precipMM_j)/(maks_precipMM_j-min_precipMM_j),3)
    jr_t4 = round((jr_t4-min_precipMM_j)/(maks_precipMM_j-min_precipMM_j),3)
    jr_t3 = round((jr_t3-min_precipMM_j)/(maks_precipMM_j-min_precipMM_j),3)
    jr_t2 = round((jr_t2-min_precipMM_j)/(maks_precipMM_j-min_precipMM_j),3)
    jr_t1 = round((jr_t1-min_precipMM_j)/(maks_precipMM_j-min_precipMM_j),3)
    jr_humidity = round((jr_humidity-min_humidity)/(maks_humidity-min_humidity),3)
    jr_tempC = round((jr_tempC-min_tempC)/(maks_tempC-min_tempC),3)
    jr_precipMM = round((jr_precipMM-min_precipMM_j)/(maks_precipMM_j-min_precipMM_j),3)

    jrealtime_normalisasi = np.array([jr_t5,jr_t4,jr_t3,jr_t2,jr_t1,jr_humidity,jr_tempC,jr_precipMM])
    #print("mrealtime normalisasi: ",mrealtime_normalisasi)
    jdata_uji = jrealtime_normalisasi[0:7]
    joutput_sebenarnya = jrealtime_normalisasi[7]
    jdata_tampil = jrealtime[0:7]
    
    n_datauji = 1
    jhasil_prediksi = np.zeros((n_datauji, 1))

    for j in range(n_datauji):
        [Z,Y] = jst.PerambatanMaju(jdata_uji,V,W,n_hidden,n_output)
        jhasil_prediksi[j,0]=Y[0,0]
        print("jhasil_prediksi: ",jhasil_prediksi[j,0])
        

    minprecipMM = min_precipMM_j
    maksprecipMM = maks_precipMM_j

    jhasilprediksi_denormalisasi = np.zeros((n_datauji,1))
    joutputsebenarnya_denormalisasi = np.zeros((n_datauji,1))

    for i in range(n_datauji):
        jhasilprediksi_denormalisasi[i,0]=jst.Denormalisasi(jhasil_prediksi[i,0],
                                                       minprecipMM,maksprecipMM)
        joutputsebenarnya_denormalisasi[i,0]=jst.Denormalisasi(joutput_sebenarnya,
                                                           minprecipMM,maksprecipMM)

    for i in range(n_datauji):
        jhasiljst=jhasilprediksi_denormalisasi[i,0]
        jdatasebenarnya=joutputsebenarnya_denormalisasi[i,0]

        jhasiljst = jhasiljst - 0
        print("hasil jst jam : ",jhasiljst)

        jerorhasil=abs(jhasiljst-jdatasebenarnya)
        
    jam_result = jhasiljst
    print("hasil jam : ",jam_result)
    y2 = mdatasebenarnya

    print("############")
    with placeholder.container():
        img1, img2, img3 = st.columns(3)
        kpi1, kpi2, kpi3 = st.columns(3)

        if ch_result>0.07:
            image1 = Image.open('rain.png')
        elif ch_result>0.05 and ch_result<=0.07 :
            image1 = Image.open('cloudy.png')
        else :
            image1 = Image.open('sunny.png')
            
        img1.image(image1,width=100)

        kpi1.metric(
            label="Prediksi curah hujan 1 detik ke depan (mm)",
            value=ch_result                
        )
            
                         
        if menit_result>0.3:
            image2 = Image.open('rain.png')
        elif menit_result>0.1 and menit_result<=0.3 :
            image2 = Image.open('cloudy.png')
        else :
            image2 = Image.open('sunny.png')
                
        img2.image(image2,width=100)

        kpi2.metric(
            label="Prediksi curah hujan 1 menit ke depan (mm)",
            value=menit_result
        )
            
        if jam_result>0.6:
            image3 = Image.open('rain.png')
        elif jam_result>0.3 and ch_result<=0.6 :
            image3 = Image.open('cloudy.png')
        else :
            image3 = Image.open('sunny.png')
                
        img3.image(image3,width=100)

        kpi3.metric(
            label="Prediksi curah hujan 1 jam ke depan (mm)",
            value=jam_result
        )

            
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT t5,t4,t3,t2,t1,h,t,ch FROM realtime_hujan ORDER BY id DESC LIMIT 5")
        myresult = mycursor.fetchall()
        df = pd.DataFrame(myresult).transpose()
        st.markdown("### Detailed Data Detik")
        st.dataframe(myresult)

        mycursor = mydb.cursor()
        mycursor.execute("SELECT t5,t4,t3,t2,t1,h,t,ch FROM realtime_menit ORDER BY id DESC LIMIT 5")
        myresult = mycursor.fetchall()
        df = pd.DataFrame(myresult).transpose()
        st.markdown("### Detailed Data Menit")
        st.dataframe(myresult)

        mycursor = mydb.cursor()
        mycursor.execute("SELECT t5,t4,t3,t2,t1,h,t,ch FROM realtime_jam ORDER BY id DESC LIMIT 3")
        myresult = mycursor.fetchall()
        df = pd.DataFrame(myresult).transpose()
        st.markdown("### Detailed Data Jam")
        st.dataframe(myresult)

        i=i+1


    # plt.scatter(k,y1,color='green')
    # plt.scatter(k,y2,color='red')
    # plt.pause(0.05)
    # plt.axis([0,k+5,0,50])