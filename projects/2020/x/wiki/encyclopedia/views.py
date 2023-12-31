from django.shortcuts import render
from django import forms

import random

from . import util
import markdown2
from markdown2 import Markdown

class searchForm(forms.Form):
     searchBar = forms.CharField

def index(request):    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entries(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html", {
            "error": 'This page does not exist' 
        })
    else:
        md_html = Markdown()
        title1 = util.get_entry(title)
        md_html = md_html.convert(title1)
        return render(request, "encyclopedia/entries.html", {
        "title": title,
        "content": md_html
        })

def search(request):
    if request.method == "POST":
        all_entries = util.list_entries()
        title = request.POST['q']
        if title in all_entries:
            searchContent = util.get_entry(title)
            content = markdown2.Markdown()
            content = content.convert(searchContent)
            return render(request, "encyclopedia/entries.html", {
            "title": title,
            "content": content
            })
        else:
            similar_entries = []
            for entry in all_entries:
                if title.lower() in entry.lower():
                    similar_entries.append(entry)
                else:   
                    pass
            return render(request, "encyclopedia/search.html", {
                "entries": similar_entries
                })           

def new_page(request):
    return render(request, "encyclopedia/new_page.html")

def savePage(request):
    if request.method == "POST":
        title = request.POST["title"].strip()
        textContent = request.POST["textContent"].strip()
        all_entries = util.list_entries()
        if title == "" or textContent == "":
            return render(request, "encyclopedia/index.html")
        elif title in all_entries:
            return render(request, "encyclopedia/error.html", {
            "error": "This page already exists" 
            })
        else:
            util.save_entry(title,textContent)
            return render(request, "encyclopedia/entries.html", {
                "title": title,
                "content": textContent
                })

def edit(request):
    if request.method == "POST":
        title = request.POST["editTitle"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def saveChanges(request):
    if request.method == "POST":
        title = request.POST["title"]
        textContent = request.POST["textContent"]
        text_Content1 = markdown2.Markdown()
        text_Content = text_Content1.convert(textContent)
        util.save_entry(title,textContent)
        return render(request, "encyclopedia/entries.html", {
        "title": title,
        "content": text_Content
        })

def randomPage(request):
    all_entries = util.list_entries()
    title = random.choice(all_entries)
    md_html = Markdown()
    title1 = util.get_entry(title)
    content = md_html.convert(title1)
    return render(request, "encyclopedia/entries.html", {
    "title": title,
    "content": content
    })
