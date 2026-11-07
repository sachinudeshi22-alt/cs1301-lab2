# Survey.py
# This page asks the user some questions and saves their answers into data.csv

import streamlit as st

st.title("National Parks Survey")
st.write("Answer the questions below. Your answers get added to my data file and show up on the Visuals page.")

# The list of parks comes from the same parks I put in data.json
parks = ["Yellowstone", "Yosemite", "Zion", "Acadia", "Glacier", "Everglades", "Shenandoah", "Olympic"]

park_choice = st.selectbox("Which national park do you most want to visit?", parks)

parks_visited = st.number_input("How many national parks have you visited?", 0, 20, 0)

activity = st.text_input("What is your favorite thing to do outdoors?")

button = st.button("Submit My Answers")

if button:
    # The activity is typed in by the user, so it might have a comma in it.
    # A comma would mess up the CSV file, so I take them out first.
    clean_activity = activity.replace(",", "")
    clean_activity = clean_activity.strip()

    if clean_activity == "":
        st.write("Please type in your favorite outdoor activity before submitting.")
    else:
        # Open the file in "a" mode so it adds a new line instead of erasing the old ones
        new_line = park_choice + "," + str(parks_visited) + "," + clean_activity + "\n"

        my_file = open("data.csv", "a")
        my_file.write(new_line)
        my_file.close()

        st.write("Thanks! Your answers were saved.")
        st.write("You picked " + park_choice + " and you have visited " + str(parks_visited) + " parks.")

st.write("---")
st.subheader("Answers So Far")

# Read the file back so the user can see everything that has been entered
read_file = open("data.csv", "r")
all_lines = read_file.readlines()
read_file.close()

count = 0
for i, line in enumerate(all_lines):
    # The first line is just the column names, so skip it
    if i == 0:
        continue
    count = count + 1

st.write("There are " + str(count) + " answers saved right now.")
