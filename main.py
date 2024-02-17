import common
import loop
import os
import webbrowser
import glob

#common.pdf_remove()
#common.combine()

common.top_songs_bar()
common.top_artist_bar()
common.artist_discovery_bubble()
loop.artist_song_discovery_bubble()
loop.artist_top_songs_chart()
loop.artist_prog_stacked_bar()
common.generate_dynamic_html_viewer("artist_prog")

# Get the current working directory
current_directory = os.getcwd()

# Specify the HTML file name
html_file_name = 'index.html'  # Replace with the actual name of your HTML file

# Construct the full path to the HTML file
html_file_path = os.path.join(current_directory, html_file_name)

# Open the HTML file in the default web browser
webbrowser.open('file://' + html_file_path, new=2)
