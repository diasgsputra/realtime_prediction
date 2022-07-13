import numpy as np
import sys
from math import *

class JST:

    # pendefinisian fungsi untuk mengacak bobot awal
    def AcakBobot(self, n_input, n_hidden, n_output):
        try:
            bobot_V = np.zeros((n_input+1, n_hidden))
            bobot_W = np.zeros((n_hidden+1, n_output))

            tmp_v = np.random.rand(n_input, n_hidden)
            tmp_w = np.random.rand(n_hidden, n_output)

            bobot_V[0,:] = 0.1
            bobot_V[1:n_input+1,:]=tmp_v

            bobot_W[0,:] = 0.1
            bobot_W[1:n_hidden+1,:]=tmp_w

            return [bobot_V, bobot_W]
        except:
            print('Terjadi kesalahan pada proses pembangkitan bobot awal',sys.exc_info()[0])

    #pendefinisian fungsi untuk melakukan normalisasi data
    def Normalisasi(self,data):
        try:
            n_data = data.shape[0]
            x = np.zeros((n_data,1))
            datamaks = max(data)
            datamin = min(data)

            #print("x = ",x)
            #print("datamaks = ",datamaks)
            #print("datamin = ",datamin)
            #exit()
            
            for i in range(n_data):
                x[i,0] = round((data[i]-datamin)/(datamaks-datamin),3)
                
            return x
        except:
            print('Terjadi kesalahan pada proses normalisasi data',sys.exc_info()[0])

    #normalisasi data realtime
    def Normalisasi_realtime(self,data,datamin, datamaks):
        try:
            
            n_data = data.shape[0]
            x = np.zeros((n_data,1))

            #print("x = ",x)
            #print("datamaks = ",datamaks)
            #print("datamin = ",datamin)
            #exit()
            
            for i in range(n_data):
                x[i,0] = round((data[i]-datamin)/(datamaks-datamin),3)
                
            return x
        except:
            print('Terjadi kesalahan pada proses normalisasi data realtime',sys.exc_info()[0])


    # pendefinisian fungsi untuk melakukan proses denomalisasi data
    def Denormalisasi(self, data, mindata, maksdata):
        try:
            #print("data (JST) : ",data)
            #print("mindata (JST) : ",mindata)
            #print("maksdata (JST) : ",maksdata)
            x = round((data*maksdata-data*mindata)+mindata,3)
            #print("x (JST) : ",x)
            return x
        except:
            print('Terjadi kesalahan pada proses denormalisasi data',sys.exc_info()[0])

    # pendefinisian fungsi untuk melakukan perhitungan nilai neuron pada hidden layer
    def Input2Hidden(self,data,n_hidden,V):
        try:
            n_data=data.shape[0]
            Z = np.zeros((1, n_hidden))

            for j in range(n_hidden):
                tmp=0
                for i in range(n_data):
                    tmp=tmp+V[i+1,j]*data[i]

                tmp = V[0,j]+tmp
                Z[0,j] = round(1/(1+exp(-tmp)),3)

            return Z
        except:
            print('Terjadi kesalahan pada proses perhitungan Z (Dari input layer ke hidden layer)',sys.exc_info()[0])
    
    # pendefinisian fungsi untuk menghitung nilai neuron pada output layer
    def Hidden2Output(self,Z,n_output,W):
        try:
            [baris,kolom] = Z.shape
            Y = np.zeros((1, n_output))
            for k in range(n_output):
                tmp = 0
                for j in range(kolom):
                    tmp = tmp+W[j+1,k]*Z[k,j]

                tmp=W[0,k]+tmp
                Y[0,k] = round(1/(1+exp(-tmp)),3)
            return Y
        except:
            print('Terjadi kesalahan pada proses perhitungan output Y (dari hidden layer ke output layer)',sys.exc_info()[0])
    
    # pendefinisian fungsi untuk melakukan perambatan maju
    def PerambatanMaju(self,data,V,W,n_hidden,n_output):
        try:
            Z = self.Input2Hidden(data,n_hidden,V)
            Y = self.Hidden2Output(Z, n_output, W)

            return [Z,Y]
        except:
            print('Terjadi kesalahan pada proses perambatan maju',sys.exc_info()[0])

    #pendefinisian fungsi untuk melakukan pembaruan bobot W
    def Output2Hidden(self,target_output,output,Z,alpha,W):
        try:
            baris, kolom=output.shape
            tao = np.zeros((baris,kolom))

            for i in range(baris):
                for j in range(kolom):
                    tao[i,j]= (target_output-output[i,j])*output[i,j]*(1-output[i,j])

            baris, kolom = tao.shape
            baris1, kolom1 = Z.shape
            deltaW = np.zeros((kolom1 + 1, kolom))

            for i in range(kolom):
                for j in range (kolom1):
                    deltaW[j+1,i]=round(alpha*tao[0,i]*Z[i,j],3)

                deltaW[0,i]=round(alpha*tao[0,i],3)

            W_baru=W+deltaW

            return W_baru
        except:
            print('Terjadi kesalahan pada proses perambatan mundur output layer ke hidden layer',sys.exc_info()[0])

    #pendefinisian fungsi untuk melakukan pembaruan bobot V
    def Hidden2Input(self,target_output,output,data,alpha,Z,W,V):
        try:
            baris, kolom=output.shape
            tao = np.zeros((baris,kolom))

            for i in range (baris):
                for j in range(kolom):
                    tao[i,j]= (target_output-output[i,j])*output[i,j]*(1-output[i,j])

            baris1, kolom1 = W.shape
            baris2, kolom2 = Z.shape
            taow = np.zeros((baris2,kolom2))

            for i in range(kolom2):
                tmp=0
                for j in range(kolom):
                    tmp=round(tmp+tao[0,j]*W[i+1,j],3)

                taow[0,i] = round(tmp*Z[0,i]*(1-Z[0,i]),3)

            baris,kolom = taow.shape
            n_data = data.shape[0]
            m,n = V.shape
            deltaV = np.zeros((m,n))
            
            for j in range(kolom):
                tmp = 0
                for i in range(n_data):
                    deltaV[i+1,j]=round(alpha*taow[0,j]*data[i],3)

                deltaV[0,j]=round(alpha*taow[0,j],3)

            Vbaru=V+deltaV

            return Vbaru
        except:
            print('Terjadi kesalahan pada proses perambatan mundur hidden layer ke input layer',sys.exc_info()[0])

    # pendefinisian fungsi untuk melakukan proses perambatan mundur
    def PerambatanMundur(self, target_output, output, data, alpha, Z, W, V):
        try:
            W_baru = self.Output2Hidden(target_output, output, Z, alpha, W)
            V_baru = self.Hidden2Input(target_output, output, data, alpha, Z,W,V)

            return [W_baru, V_baru]
        except:
            print('Terjadi kesalahan pada proses perambatan mundur',sys.exc_info()[0])
    
