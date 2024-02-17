
def generate_dynamic_html_viewer(folder_name):
    import os

    folder_name = "artist_prog"

    # Get list of HTML files in the folder
    html_files = [file for file in os.listdir(folder_name) if file.endswith('.html')]

    # Generate HTML code to display each HTML file in its own div
    html_code = ""
    for file_name in html_files:
        html_code += f"""
        <div class="iframe-container">
            <iframe src="{folder_name}/{file_name}" width="100%" height="750px" style="border: none;"></iframe>
        </div>\n
        """

    return html_code

# Call the function to generate the dynamic HTML viewer
dynamic_viewer_code = generate_dynamic_html_viewer("artist_prog")



def pdf_remove():
    import os
    import glob

    folder_path = "Spotify Extended Streaming History"

    # Construct the full path to the folder
    folder_path = os.path.join(os.getcwd(), folder_path)

    # Change the current working directory to the folder
    os.chdir(folder_path)

    # Get a list of all PDF files in the folder
    pdf_files = glob.glob("*.pdf")

    # Delete each PDF file
    for pdf_file in pdf_files:
        os.remove(pdf_file)
        print(f"Deleted: {pdf_file}")




def combine():
    import os
    import json

    # Get the current directory
    current_directory = os.getcwd()

    # Specify the directory containing the JSON files
    json_folder = os.path.join(current_directory, 'Spotify Extended Streaming History')

    # Create an empty list to store all data
    all_data = []

    # Iterate through each file in the specified directory
    for filename in os.listdir(json_folder):
        if filename.endswith('.json'):
            # Construct the full path to the JSON file
            json_file_path = os.path.join(json_folder, filename)

            # Load JSON data from the file
            with open(json_file_path, encoding='utf-8') as file:
                data = json.load(file)

            # Append data to the list
            all_data.extend(data)

    # Write the combined data to a new JSON file
    output_json_path = os.path.join(current_directory, 'combined_data.json')
    with open(output_json_path, 'w', encoding='utf-8') as output_file:
        json.dump(all_data, output_file, ensure_ascii=False, indent=2)

    print(f'Merged data saved to {output_json_path}')


def top_songs_bar():
    import pandas as pd
    import json
    import numpy as np
    import plotly.graph_objs as go

    # Load JSON data from file
    with open('combined_data.json', encoding='utf-8') as file:
        data = json.load(file)

    # Create an empty list to store dictionaries
    records = []

    # Iterate through each entry in the JSON data
    for entry in data:
        record = {
            "ts": entry["ts"],
            "ms_played": entry["ms_played"],
            "master_metadata_track_name": entry["master_metadata_track_name"],
            "master_metadata_album_artist_name": entry["master_metadata_album_artist_name"],
            "master_metadata_album_album_name": entry["master_metadata_album_album_name"],
        }

        records.append(record)

    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(records)

    # Create a new DataFrame with only the "master_metadata_track_name" column
    track_name_df = df[['master_metadata_track_name']].copy()

    # Count the occurrences of each track name
    track_counts = track_name_df['master_metadata_track_name'].value_counts().reset_index()

    # Rename the columns for clarity
    track_counts.columns = ['master_metadata_track_name', 'count']

    # Sort the DataFrame by 'count' in descending order
    track_counts_sorted = track_counts.sort_values('count', ascending=False)

    # Define the range for the tracks to display
    start_range = 0  # Assuming the index starts at 0, for the 4th row use 3
    end_range = 49  # For the 100th row use 99

    # Select the range of rows for the bar chart
    range_tracks = track_counts_sorted.iloc[start_range:end_range + 1]

    # Truncate song names to the first 15 characters
    range_tracks['master_metadata_track_name'] = range_tracks['master_metadata_track_name'].str.slice(0, 30).copy()

    # Define the colors for the gradient
    color_start = (51, 0, 102)  # Red in RGB
    color_end = (191, 230, 0)  # Blue in RGB

    # Calculate gradient colors
    colors = [
        f'rgb({color_start[0] * (1 - x) + color_end[0] * x}, '
        f'{color_start[1] * (1 - x) + color_end[1] * x}, '
        f'{color_start[2] * (1 - x) + color_end[2] * x})'
        for x in np.linspace(0, 1, range_tracks.shape[0])
    ]

    # Create the bar chart using Plotly
    fig = go.Figure()

    # Add the bar trace
    bar_trace = go.Bar(
        x=range_tracks['master_metadata_track_name'],
        y=range_tracks['count'],
        marker_color=colors  # Apply the colors to the bars
    )

    fig.add_trace(bar_trace)

    # Update layout for a better look
    fig.update_layout(
        title='Top Songs by Number of Plays',
        xaxis_title='Song Name',
        yaxis_title='Number of Plays',
        xaxis_tickangle=-45,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='White'),
        height=600,
    )

    # Convert the plot to an HTML file
    fig.write_html('top_tracks.html', full_html=False, include_plotlyjs='cdn')


def top_artist_bar():
    import pandas as pd
    import json
    import numpy as np
    import plotly.graph_objs as go

    # Load JSON data from file
    with open('combined_data.json', encoding='utf-8') as file:
        data = json.load(file)

    # Create an empty list to store dictionaries
    records = []

    # Iterate through each entry in the JSON data
    for entry in data:
        record = {
            "ts": entry["ts"],
            "ms_played": entry["ms_played"],
            "master_metadata_track_name": entry["master_metadata_track_name"],
            "master_metadata_album_artist_name": entry["master_metadata_album_artist_name"],
            "master_metadata_album_album_name": entry["master_metadata_album_album_name"],
        }

        records.append(record)

    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(records)

    # Create a new DataFrame with only the "ms_played" and "master_metadata_album_artist_name" columns
    df_selected = df[["ms_played", "master_metadata_album_artist_name"]].copy()

    # Group by "master_metadata_album_artist_name" and sum the "ms_played" values
    df_summed = df_selected.groupby("master_metadata_album_artist_name")["ms_played"].sum().reset_index()

    # Sort the DataFrame by 'ms_played' in descending order
    track_time_sorted = df_summed.sort_values('ms_played', ascending=False)

    # Convert 'ms_played' to hours with 2 decimal places
    track_time_sorted['ms_played'] = track_time_sorted['ms_played'] / 3600000  # Convert to hours
    track_time_sorted['ms_played'] = track_time_sorted['ms_played'].round(2)  # Round to 2 decimal places

    # Rename the column for clarity
    track_time_sorted.rename(columns={'ms_played': 'total_hours_played'}, inplace=True)

    # Define the range for the artists to display
    start_range = 0
    end_range = 49

    # Select the range of rows for the bar chart
    range_artists = track_time_sorted.iloc[start_range:end_range + 1]

    # Define the colors for the gradient
    color_start = (51, 0, 102)  # Red in RGB
    color_end = (191, 230, 0)

    # Calculate gradient colors
    colors = [
        f'rgb({color_start[0] * (1 - x) + color_end[0] * x}, '
        f'{color_start[1] * (1 - x) + color_end[1] * x}, '
        f'{color_start[2] * (1 - x) + color_end[2] * x})'
        for x in np.linspace(0, 1, end_range - start_range + 1)
    ]

    # Create the bar chart using Plotly
    fig = go.Figure()

    # Add the bar trace
    bar_trace = go.Bar(
        x=range_artists['master_metadata_album_artist_name'],
        y=range_artists['total_hours_played'],
        marker_color=colors  # Apply the colors to the bars
    )

    fig.add_trace(bar_trace)

    # Update layout for a better look
    fig.update_layout(
        title='Top Artists by Total Hours Played',
        xaxis_title='Artist Name',
        yaxis_title='Total Hours Played',
        xaxis_tickangle=-45,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='White'),
        height=600,
    )

    # Convert the plot to an HTML file
    fig.write_html('artist_time.html', full_html=False, include_plotlyjs='cdn')


def artist_discovery_bubble():
    import json
    import pandas as pd
    import plotly.express as px
    from datetime import datetime, timedelta

    # Load data from JSON file with UTF-8 encoding
    with open('combined_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Continue with the previous steps
    chunk = pd.DataFrame(data)

    # Sort the DataFrame by date in ascending order
    chunk['ts'] = pd.to_datetime(chunk['ts'], format='%Y-%m-%dT%H:%M:%SZ')
    chunk = chunk.sort_values(by='ts')

    # Keep the oldest row for each artist
    oldest_rows = chunk.groupby('master_metadata_album_artist_name').first().reset_index()

    # Group by artist and sum 'ms_played'
    bubble = chunk.groupby('master_metadata_album_artist_name')['ms_played'].sum().reset_index()
    bubble.rename(columns={'ms_played': 'sum_ms_played'}, inplace=True)

    # Merge the two DataFrames on both 'master_metadata_album_artist_name' and 'ts'
    result_df = pd.merge(bubble, oldest_rows[['master_metadata_album_artist_name', 'ts']],
                         left_on='master_metadata_album_artist_name', right_on='master_metadata_album_artist_name',
                         how='inner')

    # Rename the timestamp column to 'oldest_instance'
    result_df.rename(columns={'ts': 'oldest_instance'}, inplace=True)

    # Calculate days ago the artist was first listened to
    result_df['oldest_instance'] = (datetime.now() - result_df['oldest_instance']).dt.days

    # Convert sum_ms_played to sum_hour_played in hours
    result_df['sum_hour_played'] = result_df['sum_ms_played'] / (1000 * 60 * 60)  # Convert milliseconds to hours

    # Sort the DataFrame by 'sum_hour_played' in descending order
    result_df = result_df.sort_values(by='sum_hour_played', ascending=False)

    # Define range variables
    start_range = 0  # Replace with your desired start range
    end_range = 50  # Replace with your desired end range

    # Filter the DataFrame based on the specified range
    filtered_df = result_df.iloc[start_range:end_range]

    # Calculate the difference between the highest and lowest 'sum_hour_played' values
    max_sum_hour_played = filtered_df['sum_hour_played'].max()
    min_sum_hour_played = filtered_df['sum_hour_played'].min()
    diff_sum_hour_played = max_sum_hour_played - min_sum_hour_played

    # Avoid zero division
    if diff_sum_hour_played != 0:
        # Normalize the 'sum_hour_played' values to the range [0, 1]
        normalized_sum_hour_played = (filtered_df['sum_hour_played'] - min_sum_hour_played) / diff_sum_hour_played

        # Calculate the RGB values based on the normalized values
        filtered_df['color_r'] = 191 + (normalized_sum_hour_played * (51 - 191))
        filtered_df['color_g'] = 230 - (normalized_sum_hour_played * 230)
        filtered_df['color_b'] = 0 + (normalized_sum_hour_played * (102 - 0))
    else:
        # If diff_sum_hour_played is zero, set normalized values to 0 for all rows
        filtered_df['color_r'] = 191
        filtered_df['color_g'] = 230
        filtered_df['color_b'] = 0

    # Create the bubble chart for the filtered range
    fig = px.scatter(filtered_df,
                     x='oldest_instance',
                     y='master_metadata_album_artist_name',
                     size='sum_hour_played',
                     color=filtered_df['color_r'],
                     color_continuous_scale=[[0, 'rgb(191, 230, 0)'], [1, 'rgb(51, 0, 102)']],
                     labels={'master_metadata_album_artist_name': 'Artist Name',
                             'oldest_instance': 'Days Since Discovery'},
                     title=f'Artist Discovery Timeline - Top {end_range}',
                     size_max=120,  # Maximum bubble size
                     custom_data=['master_metadata_album_artist_name', 'oldest_instance']
                     )

    # Set the height of the chart
    fig.update_layout(height=1100)  # Adjust the height as needed

    # Make the background transparent
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')

    # Set text color to white
    fig.update_layout(font=dict(color='white'))

    # Remove grid lines
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    # Customize hover template
    fig.update_traces(
        hovertemplate='<b>Artist Name:</b> %{customdata[0]}<br><b>Days Since Discovery:</b> %{customdata[1]}')

    # Save the figure as an HTML file
    fig.write_html('spotify_bubble_chart.html')








