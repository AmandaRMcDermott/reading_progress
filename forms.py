import tkinter as tk
import requests
from PIL import Image, ImageTk
import pandas as pd
from pandas.io.json import json_normalize
from datetime import date
import numpy as np

# NOTE - CAN ONLY SEEM TO DO PACK, GRID, NOT ALL AT ONCE


HEIGHT = 700
WIDTH = 800


# empty lists
title_list = []
author_list = []
page_count_list = []

# information for textbox
today = date.today()
today = today.strftime("%B %d")
today2 = date.today()
future = date(2020, 12, 31)
diff = (future - date.today()).days

def book_info(title):

    api = 'google_api_key'
    url = 'https://www.googleapis.com/books/v1/volumes?q=search+terms&key=yourAPIKey'

    if "," not in title:
        #print("one")
        title = title.replace(' ', '+')
        num_books = len(title)

        url2 = url.replace('search+terms', str('intitle:' + title))
        url3 = url2.replace('yourAPIKey', api)
        df = requests.get(url3)
        data = df.json()
        data = json_normalize(data['items'], sep="_")

        title = data['volumeInfo_title'][0]
        author = data['volumeInfo_authors'][0][0]
        page_count = data['volumeInfo_pageCount'][0]
        # append
        title_list.append(title)
        author_list.append(author)
        page_count_list.append(page_count)

        df = pd.DataFrame(data={'title': [title],
                                'author': [author],
                                "page_count": [page_count]})

        page_sum = int(df['page_count'].sum())
        pages_a_day = page_sum / diff

        label['text'] = 'Number of Books: %s \n\nTotal pages to read: %s \n\nToday is %s, so you have %s days \nto read %s pages, which is %s pages a day.' % (num_books, page_sum, today, diff, page_sum, round(pages_a_day, 2))


    elif ", " in title:
        #print("two")
        title2 = title.split(", ")
        num_books = len(title2)

        for each in title2:
            #title = each
            title = each.replace(' ', '+')

            url2 = url.replace('search+terms', str('intitle:' + title))
            url3 = url2.replace('yourAPIKey', api)

            df = requests.get(url3)
            data = df.json()
            data = json_normalize(data['items'], sep="_")

            title = data['volumeInfo_title'][0]
            author = data['volumeInfo_authors'][0][0]
            page_count = data['volumeInfo_pageCount'][0]
            # append
            title_list.append(title)
            author_list.append(author)
            page_count_list.append(page_count)

        df = pd.DataFrame(data={'title': np.array(title_list),
                           'author': np.array(author_list),
                           "page_count": np.array(page_count_list)})

        page_sum = int(df['page_count'].sum())
        pages_a_day = page_sum / diff

        label['text'] = 'Number of Books: %s \n\nTotal pages to read: %s \n\nToday is %s, so you have %s days to \nread %s pages, which is %s pages a day.' % (num_books, page_sum, today, diff, page_sum, round(pages_a_day, 2))



# root for tk to run
app = tk.Tk()

# make a container for the button
canvas = tk.Canvas(app, height=HEIGHT, width=WIDTH)
canvas.pack()

frame = tk.Frame(app,bg='lightblue')
# how much of the frame is filled
frame.place(relwidth=1, relheight=1)

# TEXTBOX AREA - enter text
entry = tk.Entry(frame, font=35)
entry.place(relx=0.1,rely=0.1,relheight=0.2,relwidth=0.4)

# button
# placing it in the root/app
button = tk.Button(frame, text="Enter Book Title", bg='purple', fg='red', command= lambda: book_info(entry.get()))
button.place(relx=0.6,rely=0.15,relwidth=0.2,relheight=0.1)

# displays output text
lower_frame = tk.Frame(app)
lower_frame.place(relx=0.5,rely=0.35,relheight=0.5, relwidth=0.5, anchor='n')

# label
label = tk.Label(lower_frame)
label.place(relheight=1,relwidth=1)


# to run
app.mainloop()

# books:
#