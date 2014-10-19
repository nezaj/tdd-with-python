from django.shortcuts import redirect, render

from lists.models import Item

def home_page(request):
    items = Item.objects.all()
    return render(request, 'home.html')

def new_list(request):
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/one-list/')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items })
