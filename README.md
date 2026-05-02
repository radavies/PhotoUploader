# Photo Uploader

## To Install

1. Install the requirements file using pip
2. Install exempi ```brew install exempi```
3. Add your dropbox credentials to a file called ```dropbox_creds.json``` in the ```data``` folder.
4. The format for the creds is ```{"key": "???", "secret": "???"}```

## To Use

1. In Photo Mechanic or similar update the XMP headline with the persons pictured (this will also be used as the name of the folder to upload into on Dropbox). Use a comma separated list if there is more than one person in the image.
2. Start this app and select the folder containing the images from the previous step
3. Get a Dropbox OAuth token using the link provided and paste it back into the app
4. Click the "Go" button
5. The app will upload each image into the folders of all the people listed in the XMP headline
6. Each uploaded is logged into ```log.txt``` in the ```logs``` folder for debugging / troubleshooting

## Notes

Note to self, command to build dist:  ```pyinstaller main.py --add-data "data:data" --name "Photo Uploader" -F```