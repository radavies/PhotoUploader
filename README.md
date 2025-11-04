# Photo Uploader

1. In Photomechanic or similar update the IPTC headline with the persons pictured (this will also be used as the name of the folder to upload into on Dropbox). Use a comma seperated list if there is more than one person in the image.
2. Start this app and select the folder containing the images from the previous step
3. Get a Dropbox OAuth token using the link provided and paste it back into the app
4. Click the "Go" button
5. The app will upload each image into the folders of all the people listed in it's IPTC headline
6. Updates / error messages are displayed as the uploads happen

Note to self, command to build dist:  pyinstaller main.py --add-data "data:data" --name "Photo Uploader" -F