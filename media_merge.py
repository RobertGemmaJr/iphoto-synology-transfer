import re
import os
import datetime
import shutil

import exifread
import win32com.client
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS

MEDIA_DIR = Path(Path.home(), "Desktop", "Rob Photos (temp)")
METADATA = ["Name", "Size", "Item type", "Date modified", "Date taken"]


def main():
    dir = Path(MEDIA_DIR, "Photos")
    file = "1.jpeg"
    
    # Loop over all photos
    # Extract datetime
    # Extract year, month
    # Create year, month folder (Inside "Rob Photos (temp)") if it doesn't exist
    # Copy file to that folder
    # Loop over all videos, do the same

    # Pillow image metatdata
    image = Image.open(f"{dir}/{file}")
    imageData = image.getexif()
        
    exif = { TAGS[k]: v for k, v in imageData.items() if k in TAGS }
    print(exif)
    for tag, data in exif.items():
        # Decode bytes 
        if isinstance(data, bytes): data = data.decode()
        print(f"{tag:15}: {data}")
        


if __name__ == "__main__":
    main()
