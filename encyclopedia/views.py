from django.shortcuts import render
from django.http import HttpResponse
from . import util
from markdown2 import Markdown
import random

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()

    })

def entry(request, title):
    content = convert_md_to_html(title)
    if content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Page not found"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })

def search(request):
    if request.method == "POST":
        query = request.POST['q']
        content = convert_md_to_html(query)
        if content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": query,
                "content": content
            })
        else:
            all_entries = util.list_entries()
            recomendations = []
            for entry in all_entries:
                if query.lower() in entry.lower():
                    recomendations.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recomendations": recomendations
            })

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        exist = util.get_entry(title)
        if exist:
            return render(request, "encyclopedia/error.html", {
                "message": "Page already exists"
            })
        else:
            util.save_entry(title, content)
            return entry(request, title)
        
def edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return entry(request, title)

def random_page(request):
    all_entries = util.list_entries()
    random_entry = random.choice(all_entries)
    return entry(request, random_entry)