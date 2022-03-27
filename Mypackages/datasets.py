import pandas as pd
import streamlit as st


class Data:
    @st.cache()
    def get_data(self):
        self.app_data = pd.read_csv('App_data.csv')
        self.app_data = self.app_data.drop_duplicates(["App","Category","Rating"])
        return self.app_data
