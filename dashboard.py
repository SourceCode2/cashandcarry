# per matematica
import streamlit as st
import pandas as pd
import numpy as np
import requests
import cashcarry

st.header("Cash and carry strategy")
st.subheader(
    "Strategia market-neutral per profittare della differenza tra contratti futures e le crypto-monete sottostanti")

capitale = st.number_input('Inserire il capitale investito:')
data = cashcarry.main(capitale)
st.table(data)

