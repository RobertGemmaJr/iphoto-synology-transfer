import re
import os
import datetime
import shutil


def renameDateFiles(dir):
    for entry in os.scandir(dir):
        if os.path.isdir(entry):
            print(entry.name)
            
            # Handles rereading of changed folders
            matched = re.match("[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}[,]?", entry.name)

            if bool(matched):
                continue

            list = entry.name.split(",")
            length = len(list)
            md = list[length - 2]
            y = list[length - 1]
            loc = ""

            for i in range(0, length - 2):
                loc += list[i]
                loc += " "

            y = y.strip(" ")
            md = md.lstrip(" ")
            mdl = md.split(" ")
            m = mdl[0]
            d = mdl[1]

            mon_num = datetime.datetime.strptime(m, "%B").month
            final = y + "-" + str(mon_num) + "-" + d
            if loc != "":
                final += ", " + loc

            os.rename(os.path.join(entry.path), os.path.join(dir, final))


def mergefolders(root_src_dir, root_dst_dir):
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)

            if os.path.exists(dst_file):
                os.remove(dst_file)

            shutil.copy(src_file, dst_dir)


photo = "/Users/me/photo_export"

video = "/Users/me/video_export"

mergefolders(video, photo)
renameDateFiles(photo)
