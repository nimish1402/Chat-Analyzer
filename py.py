import tkinter as tk
from textblob import TextBlob

def summarize():
    try:
        with open('gift-of-magi.txt', 'r', encoding='utf-8') as file:
            text_content = file.read()

        analysis = TextBlob(text_content)
        sentiment.delete('1.0', "end")
        sentiment.insert('1.0', f'Polarity: {analysis.polarity}, Sentiment: {"positive" if analysis.polarity > 0 else "negative" if analysis.polarity < 0 else "neutral"}')

        title.config(state='normal')
        author.config(state='normal')
        publication.config(state='normal')
        summary.config(state='normal')

        title.delete('1.0', 'end')
        title.insert('1.0', 'N/A')

        author.delete('1.0', 'end')
        author.insert('1.0', 'N/A')

        publication.delete('1.0', 'end')
        publication.insert('1.0', 'N/A')

        summary.delete('1.0', 'end')
        summary.insert('1.0', analysis.sentences[0])  # Displaying the first sentence as a summary

        title.config(state='disabled')
        author.config(state='disabled')
        publication.config(state='disabled')
        summary.config(state='disabled')
    except FileNotFoundError:
        sentiment.delete('1.0', "end")
        sentiment.insert('1.0', 'File not found. Please make sure the "text.txt" file exists in the same directory as this script.')

root = tk.Tk()
root.title('News Summarizer')
root.geometry('1200x600')

tlabel = tk.Label(root, text='Title')
tlabel.pack()

title = tk.Text(root, height=1, width=140) 
title.config(state='disabled')
title.pack()

alabel = tk.Label(root, text='Author')
alabel.pack()

author = tk.Text(root, height=1, width=140) 
author.config(state='disabled', bg='#dddddd')
author.pack()

plabel = tk.Label(root, text="Publishing Date")
plabel.pack()

publication = tk.Text(root, height=1, width=140) 
publication.config(state='disabled', bg='#dddddd')
publication.pack()

slabel = tk.Label(root, text="Summary")
slabel.pack()

summary = tk.Text(root, height=1, width=140) 
summary.config(state='disabled', bg='#dddddd')
summary.pack()

selabel = tk.Label(root, text="Sentiment Analysis")
selabel.pack()

sentiment = tk.Text(root, height=1, width=140) 
sentiment.config(state='disabled', bg='#dddddd')
sentiment.pack()

btn = tk.Button(root, text='Summarize', command=summarize)
btn.pack()

root.mainloop()
