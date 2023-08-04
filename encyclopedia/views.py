from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def EntryPage(request, title):
    cleanedTitle = title.strip()
    return render(request, "encyclopedia/EntryPage.html", {
        "title": cleanedTitle,
        "entry": util.get_entry(cleanedTitle)
    })
