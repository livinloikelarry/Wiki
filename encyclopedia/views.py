from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse


class SearchEncyclopediaForm(forms.Form):
    term = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Search Encyclopedia"}), label=False)


matches = []


def index(request):
    if request.method == "POST":
        form = SearchEncyclopediaForm(request.POST)
        if form.is_valid():
            # get the user input and see if it is an existing entry
            term = form.cleaned_data["term"]
            options = [term, term.upper(), term.capitalize(), term.lower()]
            for o in options:
                if o in util.list_entries():
                    return HttpResponseRedirect(reverse("EntryPage", args=[o]))
            for entry in util.list_entries():
                print(f"entry: {entry}")
                if entry.find(term) >= 0:
                    matches.append(entry)
            if len(matches) >= 1:
                print(f"matches were: {matches}")
                return HttpResponseRedirect(reverse("search"))
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


def EntryPage(request, title):
    cleanedTitle = title.strip()
    return render(request, "encyclopedia/EntryPage.html", {
        "title": cleanedTitle,
        "entry": util.get_entry(cleanedTitle)
    })


def search(request):
    return render(request, "encyclopedia/search.html", {
        "matches": matches
    })
