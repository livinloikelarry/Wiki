from django.shortcuts import render
from django import forms
from . import util


class SearchEncyclopediaForm(forms.Form):
    term = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Search Encyclopedia"}), label=False)


def index(request):
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
