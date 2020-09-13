import markdown2
import secrets

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse

from . import util
from markdown2 import Markdown

class NewFormEntry(forms.Form):
    title = forms.CharField(label = 'Title')
    content = forms.CharField(label= 'Content' , widget= forms.Textarea(attrs= {'class' : 'form-control col-md-8 col-lg-10',    "rows":8}))
    edit = forms.BooleanField(initial= False, widget= forms.HiddenInput(), required = False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    md = Markdown()
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/error.html", {
            "entryTitle": entry,
            "error_link": "/",
            "massege1": "An unexpected error has occured, If your want to see all entries ",
            "massege2": "Hey Programmers...Please enter valid contents, We will definitely give best result...Thank you!!!"    
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": md.convert(entryPage),
            "entryTitle": entry
        })

        
def newentry(request):
    if request.method == "POST":
        form = NewFormEntry(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data['content']
            if (util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse('entry', kwargs={"entry":title}))
            
            else: 
                return render(request, "encyclopedia/error.html", {
                    "form":form,
                    "error1":"Page Alreday exists"
                })

        else:
            return render(request, "encyclopedia/newentry.html", {
                "form": form
            })
    else:
            return render(request, "encyclopedia/newentry.html", {
                "form": NewFormEntry()
            })
            
def random(request):
    entries = util.list_entries()
    random = secrets.choice(entries)
    return HttpResponseRedirect(reverse('entry' , kwargs= {"entry":random}))
    
def search(request):
    value = request.GET.get('q','')
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': value }))
    else:
        subStringEntries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subStringEntries.append(entry)

        return render(request, "encyclopedia/index.html", {
        "entries": subStringEntries,
        "search": True,
        "value": value
    })

def edit(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/error.html", {
            "title": entry
        })
    else:
        form = NewFormEntry()
        form.fields["title"].initial = entry     
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/newentry.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "entryTitle": form.fields["title"].initial
        }) 