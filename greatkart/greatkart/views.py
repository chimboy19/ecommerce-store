from django.shortcuts import render,redirect
from store.models import Product

def Home(request):

    products=Product.objects.all().filter(is_available=True)
    context={
        'products':products,
    }
    return render(request,'home.html',context)