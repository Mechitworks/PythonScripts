import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Use a style
plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-light.mplstyle')
# Brighter colors
colors = ['#7A76C2', '#FF0070', '#FF0070', '#00B2AA', '#FF4500', '#00FFFF']

# Add labels for specific dates
vacation_porto_start = pd.to_datetime('2023-02-12')  # Replace with the correct year
vacation_porto_end = pd.to_datetime('2023-02-17')  # Replace with the correct year
work_trip_NY_start = pd.to_datetime('2023-06-17')  # Replace with the correct year
work_trip_NY_end = pd.to_datetime('2023-06-25')  # Replace with the correct year
vacation_france_start = pd.to_datetime('2023-10-08')  # Replace with the correct year
vacation_france_label= pd.to_datetime('2023-10-06')  # Replace with the correct year
vacation_france_end = pd.to_datetime('2023-10-13')  # Replace with the correct year

dfwork = pd.read_csv('time report.csv')

# Convert 'Start Date' to datetime format
dfwork['Start Date'] = pd.to_datetime(dfwork['Start Date'], format='%d/%m/%Y')

# Group by 'Start Date' and sum 'Duration (decimal)'
dfwork = dfwork.groupby('Start Date')['Duration (decimal)'].sum().reset_index()

# Set 'Start Date' as the index
dfwork.set_index('Start Date', inplace=True)

# Resample to a weekly frequency and sum 'Duration (decimal)'
dfwork_weekly = dfwork.resample('W')['Duration (decimal)'].sum()

# Read the CSV file
df = pd.read_csv('Dagelijkse activiteitstatistieken.csv')

# Ensure that 'Column Data' is treated as datetime
df['Column Data'] = pd.to_datetime(df['Datum'])

# Set 'Column Data' as the index
df.set_index('Column Data', inplace=True)

# Create a mask for days with no 'hartslag' data
mask = df['Gemiddelde hartslag'].isna() & df['Max. hartslag'].isna()

# Calculate the rolling 7-day average for 'Gemiddelde hartslag' and 'Max. hartslag'
df['Gemiddelde hartslag'] = df['Gemiddelde hartslag'].rolling(window=7, min_periods=2).mean()
df['Max. hartslag'] = df['Max. hartslag'].rolling(window=7, min_periods=2).mean()
df['Gemiddeld gewicht'] = df['Gemiddeld gewicht'].rolling(window=7, min_periods=2).mean()

# Apply the mask to the rolling averages
df.loc[mask, ['Gemiddelde hartslag', 'Max. hartslag']] = np.nan

# Convert 'Duur van Fietsen' and 'Duur van lopen' from milliseconds to minutes
df['Duur van Fietsen'] = df['Duur van Fietsen'] / 60000
df['Duur van lopen'] = df['Duur van Lopen'] / 60000

# Fill NA/NaN values in 'Duur van Fietsen' and 'Duur van lopen' with 0
df['Duur van Fietsen'] = df['Duur van Fietsen'].fillna(0)
df['Duur van lopen'] = df['Duur van lopen'].fillna(0)

# Create a new DataFrame for the weekly average of 'Aantal beweegminuten', 'Duur van Fietsen', and 'Duur van lopen'
df_weekly = pd.DataFrame()
df_weekly['Aantal beweegminuten'] = df['Aantal beweegminuten'].resample('W').mean()
df_weekly['Duur van Fietsen'] = df['Duur van Fietsen'].resample('W').mean()
df_weekly['Duur van lopen'] = df['Duur van lopen'].resample('W').mean()

# Create a figure and a set of subplots
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(15, 12), sharex=True)
fig.suptitle('My 2023', fontsize=16, fontweight='bold')
# Plot 'Gemiddelde hartslag' and 'Max. hartslag' against 'Column Data' on the first subplot
ax1.plot(df.index, df['Gemiddelde hartslag'], label='Average sleeping heartrate 7d average', color=colors[0])
ax1.plot(df.index, df['Max. hartslag'], label='Max. sleeping heartrate 7d average', color=colors[1])
ax4.plot(df.index, df['Gemiddeld gewicht'], label='Weight in kg 7d average average', color=colors[2])

# Add the labels to the first subplot
ax1.annotate('Vacation to Porto, Portugal', (vacation_porto_start, df.loc[vacation_porto_start, 'Gemiddelde hartslag']),
            xytext=(-15, 15), textcoords='offset points',
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.5'))
ax1.annotate('Work trip to NY', (work_trip_NY_start, df.loc[work_trip_NY_start, 'Gemiddelde hartslag']),
            xytext=(-15, 15), textcoords='offset points',
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.5'))
ax1.annotate('Vacation to France', (vacation_france_start, df.loc[vacation_france_label, 'Gemiddelde hartslag']),
            xytext=(-15, 15), textcoords='offset points',
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.5'))

# Highlight the vacation and work trip periods
ax1.axvspan(vacation_porto_start, vacation_porto_end, color='#f3907e', alpha=0.3)
ax1.axvspan(work_trip_NY_start, work_trip_NY_end, color='#18c0c4', alpha=0.3)
ax1.axvspan(vacation_france_start, vacation_france_end, color='#f3907e', alpha=0.3)

# Plot 'Aantal beweegminuten', 'Duur van Fietsen', and 'Duur van lopen' against 'Column Data' on the second subplot
ax2.bar(df_weekly.index, df_weekly['Aantal beweegminuten'], label='Fit move minutes avg over week', color='#7A76C2', alpha=1, width=3)
ax2.bar(df_weekly.index + pd.Timedelta(days=3), df_weekly['Duur van Fietsen'], label='Cycling time avg over week', color='#f3907e', alpha=1, width=3)
ax2.bar(df_weekly.index + pd.Timedelta(days=3), df_weekly['Duur van lopen'], label='walking time avg over week', color='#66E9EC', alpha=1, width=3, bottom=df_weekly['Duur van Fietsen'])
ax3.bar(dfwork_weekly.index + pd.Timedelta(days=3), dfwork_weekly, label='work hours', color='#18c0c4', alpha=1, width=3)

# Format the x-axis to show abbreviated month names
ax2.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=15))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax3.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=15))
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

# Add vertical lines at the start of each month
for month in df.index.to_period('M').unique().to_timestamp():
    ax1.axvline(month, color='gray', linestyle='--', alpha=0.5)
    ax2.axvline(month, color='gray', linestyle='--', alpha=0.5)
    ax3.axvline(month, color='gray', linestyle='--', alpha=0.5)
    ax4.axvline(month, color='gray', linestyle='--', alpha=0.5)

# Set the labels and title
ax1.set_ylabel('Heartrate')
ax2.set_ylabel('minutes per day')
ax3.set_ylabel('Hours per week')
ax4.set_ylabel('Weight in kg')

# Add legends for each y-axis
ax1.legend(loc='upper right')
ax2.legend(loc='upper right')
ax3.legend(loc='upper right')
ax4.legend(loc='upper right')

# Remove the grid lines from the plots
ax1.grid(False)
ax2.grid(False)
ax3.grid(False)
ax4.grid(False)

# Remove vertical space
plt.subplots_adjust(hspace=0.1)
plt.tight_layout()
plt.savefig('My 2023.png', dpi=300)
plt.show()