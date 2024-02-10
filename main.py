import common
import loop
import os
import webbrowser
import glob

common.pdf_remove()

first_time = ''

# Get the current working directory
current_directory = os.getcwd()

# Specify the file name you want to check
file_name = "combined_data.json"

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

# Create the full path to the file by joining the current directory and the file name
file_path = os.path.join(current_directory, file_name)

# Check if the file exists
if os.path.exists(file_path):
  first_time = False
else:
  first_time = True

if first_time == True:
  common.combine()

common.top_songs_bar()
common.top_artist_bar()
common.artist_discovery_bubble()
loop.artist_song_discovery_bubble()
loop.artist_top_songs_chart()


# Get the current working directory
current_directory = os.getcwd()

# Specify the HTML file name
html_file_name = 'Web.html'  # Replace with the actual name of your HTML file

# Construct the full path to the HTML file
html_file_path = os.path.join(current_directory, html_file_name)

# Open the HTML file in the default web browser
webbrowser.open('file://' + html_file_path, new=2)
