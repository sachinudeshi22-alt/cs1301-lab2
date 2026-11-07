# Visuals.py
# This page has my charts. Part 1 charts use data.json and Part 2 charts use data.csv.

import json
import streamlit as st
import matplotlib.pyplot as plt

st.title("National Parks Visuals")


# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------

def get_json_data():
    # Open data.json and turn it into a dictionary
    json_file = open("data.json")
    data = json.load(json_file)
    json_file.close()
    return data


def get_csv_rows():
    # Read data.csv and return a list of tuples, one tuple per answer
    csv_file = open("data.csv", "r")
    lines = csv_file.readlines()
    csv_file.close()

    rows = []
    for i, line in enumerate(lines):
        # Line 0 is the header row with the column names, so skip it
        if i == 0:
            continue

        clean_line = line.strip()
        if clean_line == "":
            continue

        pieces = clean_line.split(",")
        if len(pieces) < 3:
            continue

        park = pieces[0]
        visited = int(pieces[1])
        activity = pieces[2]

        # Store each answer as a tuple
        rows.append((park, visited, activity))

    return rows


def count_each_park(rows):
    # Build a dictionary that counts how many people picked each park
    counts = {}
    for park, visited, activity in rows:
        if park in counts:
            counts[park] = counts[park] + 1
        else:
            counts[park] = 1
    return counts


def get_mean_and_median(numbers):
    # Returns a tuple with the mean and the median
    total = 0
    for n in numbers:
        total = total + n
    mean = total / len(numbers)

    in_order = sorted(numbers)
    middle = len(in_order) // 2
    if len(in_order) % 2 == 1:
        median = in_order[middle]
    else:
        median = (in_order[middle - 1] + in_order[middle]) / 2

    return (mean, median)


data = get_json_data()
park_names = data["park_names"]
states = data["state"]
visitors = data["visitors_millions"]
acres = data["acres_millions"]
years = data["year_founded"]


# ==================================================================
# PART 1, CHART 1 - STATIC and ADVANCED (matplotlib bar chart)
# ==================================================================

st.write("---")
st.header("Chart 1: Visitors Per Park")
st.write("This is my static chart. It always looks the same because it just shows everything in data.json.")

fig1 = plt.figure()
plt.bar(park_names, visitors, color="green")
plt.title("Yearly Visitors at Each National Park")
plt.xlabel("National Park")
plt.ylabel("Visitors (millions)")
plt.xticks(rotation=45)
st.pyplot(fig1)


# ==================================================================
# PART 1, CHART 2 - DYNAMIC (scatter chart with a slider)
# ==================================================================

st.write("---")
st.header("Chart 2: Park Size vs Visitors")
st.write("This is my dynamic chart. Move the slider to only show parks founded in or after a certain year.")

# Set up the session state the first time the page loads
if "min_year" not in st.session_state:
    st.session_state["min_year"] = 1872

st.session_state["min_year"] = st.slider("Only show parks founded in or after this year:",
                                         1872, 1938, st.session_state["min_year"])

chosen_year = st.session_state["min_year"]

# Build new lists with only the parks that pass the filter
shown_acres = []
shown_visitors = []
shown_names = []
shown_states = []

for i, year in enumerate(years):
    if year >= chosen_year:
        shown_acres.append(acres[i])
        shown_visitors.append(visitors[i])
        shown_names.append(park_names[i])
        shown_states.append(states[i])

if len(shown_names) == 0:
    st.write("No parks were founded in or after that year. Try moving the slider back.")
else:
    scatter_data = {"Size (million acres)": shown_acres, "Visitors (millions)": shown_visitors}
    st.scatter_chart(scatter_data, x="Size (million acres)", y="Visitors (millions)")

    # EXTRA CREDIT: these numbers change every time the slider moves
    stats1 = get_mean_and_median(shown_visitors)
    col_a, col_b = st.columns(2)
    col_a.metric("Mean visitors (millions)", round(stats1[0], 2))
    col_b.metric("Median visitors (millions)", round(stats1[1], 2))

    st.write("Parks being shown right now:")
    for i, name in enumerate(shown_names):
        st.write("- " + name + " (" + shown_states[i] + ")")


# ==================================================================
# PART 2, CHART 3 - STATIC and ADVANCED (matplotlib pie chart)
# ==================================================================

rows = get_csv_rows()

st.write("---")
st.header("Chart 3: Which Park People Want To Visit")
st.write("This is my static chart for Part 2. It uses the survey answers saved in data.csv.")

if len(rows) == 0:
    st.write("Nobody has taken the survey yet. Go to the Survey page and add an answer.")
else:
    park_counts = count_each_park(rows)

    pie_labels = []
    pie_sizes = []
    for park in park_counts:
        pie_labels.append(park)
        pie_sizes.append(park_counts[park])

    fig3 = plt.figure()
    plt.pie(pie_sizes, labels=pie_labels, autopct="%1.0f%%")
    plt.title("Park People Most Want To Visit")
    st.pyplot(fig3)


# ==================================================================
# PART 2, CHART 4 - DYNAMIC (line chart with a slider)
# ==================================================================

st.write("---")
st.header("Chart 4: How Many Parks People Have Visited")
st.write("This is my dynamic chart for Part 2. Move the slider to change the highest number of parks included.")

if len(rows) == 0:
    st.write("Nobody has taken the survey yet, so there is nothing to graph.")
else:
    # Find the biggest answer anyone gave so the slider does not go too high
    biggest = 0
    for park, visited, activity in rows:
        if visited > biggest:
            biggest = visited

    if "max_visited" not in st.session_state:
        st.session_state["max_visited"] = biggest

    if st.session_state["max_visited"] > biggest:
        st.session_state["max_visited"] = biggest

    st.session_state["max_visited"] = st.slider("Only include people who have visited this many parks or fewer:",
                                                0, biggest, st.session_state["max_visited"])

    cutoff = st.session_state["max_visited"]

    # Keep only the answers under the cutoff
    kept_numbers = []
    for park, visited, activity in rows:
        if visited <= cutoff:
            kept_numbers.append(visited)

    if len(kept_numbers) == 0:
        st.write("Nobody matches that, try moving the slider up.")
    else:
        # Count how many people gave each number
        line_counts = {}
        for number in range(0, cutoff + 1):
            line_counts[number] = 0

        for number in kept_numbers:
            line_counts[number] = line_counts[number] + 1

        people_list = []
        for number in line_counts:
            people_list.append(line_counts[number])

        st.line_chart({"Number of people": people_list})

        # EXTRA CREDIT: show the mean and median, and they update with the slider
        stats = get_mean_and_median(kept_numbers)
        mean_value = stats[0]
        median_value = stats[1]

        col1, col2 = st.columns(2)
        col1.metric("Mean parks visited", round(mean_value, 2))
        col2.metric("Median parks visited", median_value)

        st.write("This is based on " + str(len(kept_numbers)) + " survey answers.")
