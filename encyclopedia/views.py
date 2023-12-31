from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
from markdown2 import Markdown


class SearchEncyclopediaForm(forms.Form):
    term = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Search Encyclopedia"}), label=False)


class NewPageForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="text", widget=forms.Textarea(
        attrs={'rows': 5, 'cols': 20}))


class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 5, 'cols': 20}), label=False)


matches = []


def index(request):
    matches.clear()
    if request.method == "POST":
        form = SearchEncyclopediaForm(request.POST)
        if form.is_valid():
            # get the user input and see if it is an existing entry
            term = form.cleaned_data["term"]
            options = [term, term.upper(), term.capitalize(), term.lower()]
            for o in options:
                if o in util.list_entries():
                    return HttpResponseRedirect(reverse("EntryPage", args=[o]))
            # no match but substring found
            for entry in util.list_entries():
                if entry.find(term) >= 0:
                    matches.append(entry)
            if len(matches) >= 1:
                print(f"matches were: {matches}")
                return HttpResponseRedirect(reverse("search"))
            # search term not in entries
            return HttpResponseRedirect(reverse("EntryPage", args=[term]))
        else:  # form not valid
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(),
                "form": form
            })
    # else if method is GET
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchEncyclopediaForm()
    })


def NewPage(request):
    entryExists = False
    # if post request
    if request.method == "POST":
        PageForm = NewPageForm(request.POST)
        if PageForm.is_valid():
            title = PageForm.cleaned_data["title"]
            content = PageForm.cleaned_data["content"]
            if title in util.list_entries():
                entryExists = True
                return render(request, "encyclopedia/NewPage.html", {
                    "entryExists": entryExists
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("EntryPage", args=[title]))
    # if get request
    return render(request, "encyclopedia/NewPage.html", {
        "NewPageForm": NewPageForm(),
        "entryExists": entryExists
    })


def EntryPage(request, title):
    cleanedTitle = title.strip()
    markdowner = Markdown()
    # if entry doesn't exist
    if not cleanedTitle in util.list_entries():
        return render(request, "encyclopedia/EntryPage.html", {
            "title": cleanedTitle,
            "entry": None
        })
    return render(request, "encyclopedia/EntryPage.html", {
        "title": cleanedTitle,
        "entry": markdowner.convert(util.get_entry(cleanedTitle))
    })


def search(request):
    return render(request, "encyclopedia/search.html", {
        "matches": matches
    })


def randomPage(request):
    entries = util.list_entries()
    numOfEntries = len(entries)
    randomNum = random.randint(0, numOfEntries - 1)
    title = entries[randomNum]
    return HttpResponseRedirect(reverse("EntryPage", args=[title]))


def edit(request, title):
    # get entry text based on title
    if request.method == "POST":
        editedForm = EditEntryForm(request.POST)
        if editedForm.is_valid():
            text = editedForm.cleaned_data['content']
            util.save_entry(title, text)
            print("going to redirect")
            return HttpResponseRedirect(reverse("EntryPage", args=[title]))

    # GET method called when user clicks edit link
    entryText = util.get_entry(title)
    content = EditEntryForm()
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "editForm": EditEntryForm(initial={'content': entryText})
    })
