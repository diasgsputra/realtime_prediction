import streamlit as st
import mysql.connector
import time
import numpy as np
import pyautogui as pg
import datetime
import random
from random import choices

genre = st.radio(
     "What's your favorite movie genre",
     ('Comedy', 'Drama', 'Documentary'))

if genre == 'Comedy':
     st.write('You selected comedy.')
elif genre == 'Drama':
     st.write("You selected Drama.")
else:
    st.write("You selected Documentary.")