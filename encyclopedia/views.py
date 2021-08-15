##################################
from django.shortcuts import render
##################################
from . import util
#################################
from random import randrange
from django.contrib import messages
from django.shortcuts import redirect
from markdown2 import Markdown

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title_name):
    content = util.get_entry(title_name)
    

    if content is None:
        return render(request, "encyclopedia/entry.html", {
            "title_name" : title_name ,
            "title_content" : f"{title_name} does't exist"
        })
    else :
        return render(request, "encyclopedia/entry.html", {
            "title_name" : title_name ,
            "title_content" : markdowner.convert(content)
        })

def search(request):
    q = request.GET["q"]
    data = util.get_entry(q)
    all = util.list_entries()
    list = []

    if data is None:
        for a in all:
            if a.find(q) != -1:
                list.append(a)

        return render(request, "encyclopedia/index.html", {
            "entries" : list
        })

    else :
        return render(request, "encyclopedia/entry.html", {
            "title_name" : q ,
            "title_content" : markdowner.convert(data)
        })

def new(request):
    if request.method == "POST":
        title_new = request.POST["title_new"]
        content_new = request.POST["content_new"]
        entries = util.list_entries()

        for entry in entries:
            if title_new == entry:
                messages.info(request,f"{title_new} already exist")
                return redirect("new")

            else:
                util.save_entry(title_new, content_new)
                return render(request, "encyclopedia/new.html")
    else :
        return render(request, "encyclopedia/new.html")

def edit(request,title_edit):
    if request.method == "POST":
        content_edited = request.POST["content_edited"]
        util.save_entry(title_edit, content_edited)
        return render(request,"encyclopedia/entry.html",{
            "title_name" : title_edit ,
            "title_content" : markdowner.convert(util.get_entry(title_edit))
        })
    else:
        return render(request, "encyclopedia/edit.html", {
            "content_edit" : util.get_entry(title_edit) ,
            "title_edit" : title_edit
        })

def random(request):
    entries = util.list_entries()
    x = randrange(len(entries))
    return render(request, "encyclopedia/entry.html",{
        "title_name" : entries[x],
        "title_content" : markdowner.convert(util.get_entry(entries[x]))  
    })