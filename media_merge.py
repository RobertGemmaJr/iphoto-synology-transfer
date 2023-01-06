import re

import datetime

import exifread
import os
import shutil
import mimetypes
import ffmpeg
from PIL import Image
from PIL.ExifTags import TAGS

DIR = os.path.join(os.path.expanduser('~'), 'Desktop', 'Rob Photos (temp)')
METADATA = ["Name", "Size", "Item type", "Date modified", "Date taken"]
            
# Loop over all photos
# Extract datetime
# Extract year, month
# Create year, month folder (Inside "Rob Photos (temp)") if it doesn't exist
# Copy file to that folder (Make sure to use shutil.copy2)
# Loop over all videos, do the same

def isImage(file: str):
    mimestart = mimetypes.guess_type(file)[0]
    return mimestart.split('/')[0] == 'image'

def isVideo(file: str):
    type = mimetypes.guess_type(file)[0]
    return type.split('/')[0] == 'video'

def get_datetime(file: str):
    assert os.path.exists(file)
    
    if(isImage(file)):
        # Using exifread
        with open(file, 'rb') as f:
            tags = exifread.process_file(f)
            # print(tags.keys())
        
        
        # Using ffmpeg
        # t = ffmpeg.probe(file)
        # streams = t['streams']
        # format = t['format']
        # print(streams[0].keys())
        # print(format.keys())
        
        
        
        # Using PIL
        # image = Image.open(file)
        # exif = { TAGS[k]: v for k, v in image.getexif().items() if k in TAGS }
        # print('Image: ', exif['DateTime'])
        # return exif['DateTime']
    elif(isVideo(file)):
        print(file)
        video = ffmpeg.probe(os.path.abspath(file))
        print(video)
        return 'video'
    else:
        print(f"{file} is not a media file, skipped")
        return None
    


def main():
    
    # Get directory
    # dir = os.path.join(os.path.expanduser('~'), 'Desktop', 'Rob Photos (temp)')
    assert os.path.exists(DIR)
    
    
    # Get full paths to the files
    # dir should contain 2 folders - one for photos and one for videos, will recurse either way
    # TODO: Just use PIL? It seems easier?
    fileDict = {}
    for root, subdirs, files in os.walk(os.path.join(DIR, 'Photos')):
        for file in files:
            file = os.path.join(root, file)
            with open(file, 'rb') as f:
                tags = exifread.process_file(f)
                fileDict[f.name] = tags['EXIF DateTimeOriginal']
    print(fileDict)
    
    # TODO: Read metadata for video files
    for root, subdirs, files in os.walk(os.path.join(DIR, 'Videos')):
        for file in files:
            file = os.path.join(root, file)
            print(file)
            with open(file, 'rb') as f:
                tags = exifread.process_file(f)
                print(tags)
                fileDict[f.name] = tags['EXIF DateTimeOriginal']
    print(fileDict)
                
                
    # EXIF DateTimeOriginal, Image DateTimeOriginal
            
    
    # Create output directory (forced)
    # dest = os.path.join(DIR, 'out')
    # if(os.path.exists(dest)):
    #     shutil.rmtree(dest)
    # os.mkdir(dest)
    # assert os.path.exists(dest)
    
    # Sort path by datetime
    # paths.sort(key=get_datetime)
        
    # exif = { TAGS[k]: v for k, v in imageData.items() if k in TAGS }
    # print(exif)
    # for tag, data in exif.items():
    #     # Decode bytes 
    #     if isinstance(data, bytes): data = data.decode()
    #     print(f"{tag:15}: {data}")
    
    # TODO: 1.jpeg is wrong, save correct DateTime
        


if __name__ == "__main__":
    main()
