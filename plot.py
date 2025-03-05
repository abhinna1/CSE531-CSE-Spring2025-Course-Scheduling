import pandas as pd
import plotly.express as px

# Load the CSV file into a DataFrame
df = pd.read_csv('/home/abhinna/ub/Algorithms/HW2/generated_schedule.csv')

# Convert the "Start Time" and "End Time" columns to datetime
df['Start Time'] = pd.to_datetime(df['Start Time'], format='%H:%M:%S').dt.time
df['End Time'] = pd.to_datetime(df['End Time'], format='%H:%M:%S').dt.time

# Map the "Days" column to individual days
day_mapping = {
    'MWF': ['Monday', 'Wednesday', 'Friday'],
    'TR': ['Tuesday', 'Thursday'],
    'R': ['Thursday'],
    'MW': ['Monday', 'Wednesday']
}

# Create a new DataFrame to expand the days
expanded_df_list = []

for index, row in df.iterrows():
    days = day_mapping[row['Days']]
    for day in days:
        new_row = row.copy()
        new_row['Day'] = day
        expanded_df_list.append(new_row)

expanded_df = pd.DataFrame(expanded_df_list)

# Convert "Start Time" and "End Time" to datetime with a dummy date
expanded_df['Start DateTime'] = pd.to_datetime('2025-01-01 ' + expanded_df['Start Time'].astype(str))
expanded_df['End DateTime'] = pd.to_datetime('2025-01-01 ' + expanded_df['End Time'].astype(str))

# Create a new column for the legend that includes the course name, days, and timings
expanded_df['Course_Timing'] = expanded_df['Course'] + ' (' + expanded_df['Days'] + '): ' + expanded_df['Start Time'].astype(str) + '-' + expanded_df['End Time'].astype(str)

# Create the Gantt chart
fig = px.timeline(
    expanded_df,
    x_start="Start DateTime",
    x_end="End DateTime",
    y="Day",
    color="Course_Timing",
    title="CSE Graduate Program Class Schedule—Spring 2025",
    labels={"Start DateTime": "Start Time", "End DateTime": "End Time"}
)

# Update the layout for better readability and sequence the y-axis
fig.update_layout(
    xaxis_title="Time",
    yaxis_title="Day of Week",
    yaxis=dict(categoryorder='array', categoryarray=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']),
    showlegend=True,
    legend_title="Course, Days, and Timings"
)

# Show the Gantt chart
fig.show()