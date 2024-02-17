import json
import pandas as pd
import plotly.express as px
from datetime import datetime


def artist_top_songs_chart():
    import pandas as pd
    import json
    import plotly.graph_objs as go
    import numpy as np

    # Load JSON data from file
    with open('combined_data.json', encoding='utf-8') as file:
        data = json.load(file)

    # Create a DataFrame from the JSON data
    df = pd.DataFrame(data)

    # Group by artist and sum 'ms_played', then sort by total play time in descending order
    artist_playtime = df.groupby('master_metadata_album_artist_name')['ms_played'].sum().sort_values(
        ascending=False).reset_index()

    # Create a DataFrame with just artist names and their rankings
    artist_rankings = pd.DataFrame({
        'artist_name': artist_playtime['master_metadata_album_artist_name'],
        'ranking': range(1, len(artist_playtime) + 1)
    })

    # Define top range for artists (e.g., top 50 artists)
    top_artists_range = 50
    top_songs_range = 25

    # Filter the DataFrame to only include songs by the top artists
    top_artists = artist_playtime.head(top_artists_range)['master_metadata_album_artist_name']
    df_top_artists = df[df['master_metadata_album_artist_name'].isin(top_artists)]

    # Define the range of the top artists to create graphs for
    start_rank = 0
    end_rank = 4

    # Loop through the specified range of top artists
    for i in range(start_rank, end_rank + 1):
        artist_name = artist_rankings.iloc[i]['artist_name']

        # Filter songs by the artist
        artist_songs = df_top_artists[df_top_artists['master_metadata_album_artist_name'] == artist_name]

        # Group by track name, count the number of plays, and get the top songs
        top_songs = artist_songs.groupby('master_metadata_track_name').agg(
            {'ms_played': 'sum', 'master_metadata_track_name': 'size'}).rename(
            columns={'master_metadata_track_name': 'count'}).nlargest(top_songs_range, 'ms_played').reset_index()

        # Truncate song names to the first 30 characters for display
        top_songs['master_metadata_track_name'] = top_songs['master_metadata_track_name'].str.slice(0, 30)

        # Define the colors for the gradient
        color_start = (51, 0, 102)
        color_end = (169, 230, 0)

        # Calculate gradient colors
        colors = [
            f'rgb({color_start[0] * (1 - x) + color_end[0] * x}, '
            f'{color_start[1] * (1 - x) + color_end[1] * x}, '
            f'{color_start[2] * (1 - x) + color_end[2] * x})'
            for x in np.linspace(0, 1, top_songs.shape[0])
        ]

        # Create the bar chart using Plotly
        fig = go.Figure()

        # Add the bar trace
        bar_trace = go.Bar(
            x=top_songs['master_metadata_track_name'],
            y=top_songs['count'],
            marker_color=colors  # Apply the colors to the bars
        )

        fig.add_trace(bar_trace)

        # Update layout for a better look
        fig.update_layout(
            title=f'Top {top_songs_range} Songs by {artist_name}',
            xaxis_title='Song Name',
            yaxis_title='Number of Plays',
            xaxis_tickangle=-45,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='White'),
            height=600,
        )

        # Save the plot to an HTML file
        fig.write_html(f'popular_artist_{i + 1}_songs.html', full_html=False, include_plotlyjs='cdn')


def artist_song_discovery_bubble():
    import json
    import pandas as pd
    import plotly.express as px
    from datetime import datetime, timezone

    # Load data from JSON file with UTF-8 encoding
    with open('combined_data.json', 'r', encoding='utf-8') as file:
        # Load only required columns from JSON into DataFrame
        data = json.load(file)
        data = [{key: entry[key] for key in
                 ['ts', 'master_metadata_album_artist_name', 'master_metadata_track_name', 'ms_played']}
                for entry in data]

    # Convert JSON data to DataFrame
    df = pd.DataFrame(data)

    # Convert timestamp to datetime format and set timezone to UTC
    df['ts'] = pd.to_datetime(df['ts']).dt.tz_localize(None).dt.tz_localize(timezone.utc)

    # Calculate sum of ms_played for each artist
    artist_sum_ms_played = df.groupby('master_metadata_album_artist_name')['ms_played'].sum().reset_index()
    artist_sum_ms_played = artist_sum_ms_played.sort_values(by='ms_played', ascending=False)

    # Filter to keep only the top 5 artists
    top_artists = artist_sum_ms_played.head(5)

    # Group by artist and create separate DataFrames for each artist
    artist_dataframes = {}
    for i, artist in enumerate(top_artists['master_metadata_album_artist_name']):
        artist_df = df[df['master_metadata_album_artist_name'] == artist]
        artist_dataframes[f'artist_{i + 1}'] = artist_df

    # Process each artist DataFrame
    for artist_name, artist_df in artist_dataframes.items():
        # Group by song and sum ms_played
        song_ms_played = artist_df.groupby('master_metadata_track_name')['ms_played'].sum().reset_index()

        # Keep only the oldest row for each song
        oldest_rows = artist_df.groupby('master_metadata_track_name')['ts'].min().reset_index()
        song_ms_played = pd.merge(song_ms_played, oldest_rows, on='master_metadata_track_name', how='inner')

        # Sort by sum_ms_played in descending order
        song_ms_played = song_ms_played.sort_values(by='ms_played', ascending=False)

        # Convert ms_played to hours and round to 2 decimal places
        song_ms_played['hours_played'] = round(song_ms_played['ms_played'] / (1000 * 60 * 60),
                                               2)  # Convert milliseconds to hours and round to 2 decimal places

        # Keep only the top 50 rows
        top_songs = song_ms_played.head(50)

        # Get the artist name for the first row
        first_artist_name = artist_df.iloc[0]['master_metadata_album_artist_name']

        # Plotly bubble chart for the top songs
        fig = px.scatter(top_songs, x=(datetime.now(timezone.utc) - top_songs['ts']).dt.days,
                         y='master_metadata_track_name',
                         size='hours_played', color='hours_played',
                         color_continuous_scale='Viridis', title=f'Top 50 Songs for {first_artist_name}',
                         labels={'master_metadata_track_name': 'Song Name', 'x': 'Days Since First Played',
                                 'hours_played': 'Hours Played'},
                         size_max=120)

        # Customize figure styling
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot area
            font=dict(color='white'),  # White text color
            xaxis=dict(showgrid=False),  # Hide x-axis grid lines
            yaxis=dict(showgrid=False)  # Hide y-axis grid lines
        )

        # Save the figure as HTML file
        fig.write_html(f'{artist_name}_bubble_chart.html')


import pandas as pd
import plotly.graph_objects as go
import calendar
import json
import os

import calendar
import pandas as pd
import plotly.graph_objects as go
import os


def artist_prog_stacked_bar():
    # Define month abbreviations dictionary
    month_abbr = {i: month_abbr[:3] for i, month_abbr in enumerate(calendar.month_abbr)}

    # Step 1: Read data from JSON file into a pandas DataFrame
    full = pd.read_json('combined_data.json')

    # Convert 'ts' column to datetime format
    full['ts'] = pd.to_datetime(full['ts'])

    # Step 2: Split data into DataFrames for each year
    years = full['ts'].dt.year.unique()
    yearly_data = {}
    for year in years:
        yearly_data[year] = full[full['ts'].dt.year == year]

    # Step 3: Split each year's data into DataFrames for each month
    monthly_data = {}
    for year, data in yearly_data.items():
        monthly_data[year] = {}
        for month in range(1, 13):
            monthly_data[year][month] = data[data['ts'].dt.month == month]

    # Step 4: Group by artist and sum ms_played, then sort
    chart_data = {}
    for year, data in monthly_data.items():
        chart_data[year] = {}
        for month, df in data.items():
            chart_data[year][month] = df.groupby('master_metadata_album_artist_name')['ms_played'].sum().reset_index()
            chart_data[year][month] = chart_data[year][month].sort_values(by='ms_played', ascending=False)

    # Define a custom color palette
    custom_colors = ['#a2cf11', '#35b55d', '#38c7b9', '#1a6cc9', '#1a32c9', '#5133a1']

    # Create a folder named "artist_prog" if it doesn't exist
    folder_name = "artist_prog"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Step 5: Create stacked bar charts for each month and chart for each year
    for year, data in chart_data.items():
        figs = []
        for month, df in data.items():
            top_artists = df.head(5)
            other = df.iloc[5:]
            if not other.empty:
                top_artists.loc[len(top_artists)] = ['Other', other['ms_played'].sum()]
            total_time = df['ms_played'].sum()

            # Convert ms_played to hours
            top_artists['hours_played'] = top_artists['ms_played'] / (1000 * 60 * 60)

            # Create a bar for each artist
            for i, artist_row in enumerate(top_artists.itertuples(), start=0):
                trace = go.Bar(
                    x=[f"{month_abbr[month]}"],  # Using month abbreviations
                    y=[artist_row.hours_played],
                    name=artist_row.master_metadata_album_artist_name,
                    hoverinfo='y+name',  # Show only hours played and artist name
                    text=[],  # Empty list to remove text inside bars
                    marker=dict(color=custom_colors[i], opacity=0.8, line=dict(width=0))
                )
                figs.append(trace)

        layout = go.Layout(
            title=f'Listening Habits for Year {year}',
            xaxis=dict(title='Month'),
            yaxis=dict(title='Time Played (Hours)'),
            barmode='stack',
            showlegend=False,  # Remove the legend
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
            font=dict(color='White'),
        )
        fig = go.Figure(data=figs, layout=layout)

        # Save chart as HTML file in the "artist_prog" folder
        filename = os.path.join(folder_name, f'listening_habits_{year}.html')
        fig.write_html(filename)


artist_prog_stacked_bar()
