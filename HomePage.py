# HomePage.py
# This is the home page for my Lab 2 project.

import streamlit as st

st.title("National Parks Data")
st.header("CS 1301")
st.subheader("Web Development - Section C")
st.subheader("Sachin Udeshi")

st.write("Welcome to my Lab 2 app! This project is about United States national parks. You can move between the pages using the sidebar on the left.")

st.write("1. **Survey**: Answer a few questions about national parks. Your answers get saved into a CSV file.")
st.write("2. **Visuals**: Charts made from my JSON file of park facts and from the survey answers people entered.")

st.write("---")
st.write("The park facts in data.json are things like how many visitors each park gets, how big it is, and what year it was founded.")
