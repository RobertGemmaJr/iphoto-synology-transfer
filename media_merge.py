import os
import shutil
import datetime
import ffmpeg
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS

DIR = Path(Path.expanduser(Path("~")), "Desktop", "Rob Photos (temp)")

# Use PIL to transfer the photos by datetime
def get_photos(fileDict: dict):
    for file in [p for p in Path(DIR, "Photos").rglob("*") if p.is_file()]:
        exif = {TAGS[k]: v for k, v in Image.open(file).getexif().items() if k in TAGS}
        date = datetime.datetime.strptime(exif["DateTime"], "%Y:%m:%d %H:%M:%S").date()
        
        fileDict[file] = date
    return fileDict


# Use ffmpeg to transfer the videos by datetime
def get_videos(fileDict: dict):
    for file in [p for p in Path(DIR, "Videos").rglob("*") if p.is_file()]:
            probe = ffmpeg.probe(file)

            # TODO: Some don't have creation_time
            # C:\Users\gemr1\Desktop\Rob Photos (temp)\Videos\GHDL5952.mp4
            # C:\Users\gemr1\Desktop\Rob Photos (temp)\Videos\IMG_1791.mp4
            # C:\Users\gemr1\Desktop\Rob Photos (temp)\Videos\ONYQ6525.mp4
            # C:\Users\gemr1\Desktop\Rob Photos (temp)\Videos\OUKJ5151.mp4
            # C:\Users\gemr1\Desktop\Rob Photos (temp)\Videos\URI Day of Giving 2021.mp4
            # C:\Users\gemr1\Desktop\Rob Photos (temp)\Videos\WACY1703.mp4
            # C:\Users\gemr1\Desktop\Rob Photos (temp)\Videos\WQDX6014.mp4
            # C:\Users\gemr1\Desktop\Rob Photos (temp)\Videos\XHQC6528.mp4
            try:
                dateT = probe["format"]["tags"]["creation_time"]
                date = datetime.datetime.strptime(dateT, "%Y-%m-%dT%H:%M:%S.%fZ").date()
                fileDict[file] = date
            except Exception:
                print("FAILED:", file)
    return fileDict


def main():
    # TODO: 1.jpeg is wrong, save correct DateTime
    assert Path.exists(DIR)

    fileDict: dict[str, datetime.date] = {}
    get_photos(fileDict)
    get_videos(fileDict)

    # Create output directory (forced)
    dest = Path(DIR, "out")
    if Path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    assert Path.exists(dest)

    for path, date in fileDict.items():
        print(f"{path} {date.year} {date.month}")
        year = str(date.year)
        month = str(date.month)
        # Create year/ if not created
        # Create year/month/ if not created
        # Path(dest, year).mkdir(parents=True, exist_ok=True)
        Path(dest, year, month).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    main()
