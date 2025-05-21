Because modern web browsers block loading local JSON files directly from the file system, you first need to navigate to this directory in your command line and run a simple web server.
If you have Python installed, you can use the built-in server by running:

`python -m http.server`

If that doesn't work, you might be using an older version of Python (Python 2). In that case, try:

`python -m SimpleHTTPServer`

Once the server is running, open your browser and go to http://localhost:8000/.
Congratulations, the program is now up and running!

Folder data_by_year contains collected data and processed folder contains data after modification needed for this visualization.
