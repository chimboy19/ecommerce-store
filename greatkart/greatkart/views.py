from django.shortcuts import render,redirect
from store.models import product

def Home(request):

    products=product.objects.all().filter(is_available=True)
    context={
        'products':products,
    }
    return render(request,'home.html',context)