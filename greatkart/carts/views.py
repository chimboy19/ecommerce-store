from django.shortcuts import get_object_or_404, render,redirect
from store.models import Product,Variation
from .models import Cartitem,Cart
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django .contrib import messages
# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart




def add_cart(request,product_id):
    current_user= request.user
    product=Product.objects.get(id=product_id)
    # if the user is authenticated
    if current_user.is_authenticated:
        product_variation=[]
        # this is in charge of selecting the various size or color of the product etc
        if request.method =='POST':
         for item in request.POST:
            key=item
            value=request.POST[key]
            try:
                variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                product_variation.append(variation)
                #    print (variation)
            except :
                pass
                

            
            
        #    color= request.POST['color']
        #    size= request.POST['size']
            

        # product=Product.objects.get(id=product_id)#get the product
       

        is_cart_item_exists=Cartitem.objects.filter(product=product,user=current_user).exists()

        if is_cart_item_exists:
                cart_item=Cartitem.objects.filter(product=product, user=current_user)
                ex_var_list=[]
                id=[]
                for item in cart_item:
                    existing_variation= item.variations.all()
                    ex_var_list.append(list(existing_variation))
                    id.append(item.id)
                    
                print(ex_var_list)


                if product_variation in ex_var_list:
                    #    increase the cart item Quantity
                    index=ex_var_list.index(product_variation)
                    item_id=id[index]
                    item=Cartitem.objects.get(product=product, id=item_id)
                    item.quantity +=1
                    item.save()
                      
                   # Check stock before increasing quantity added by me//////////////
                    selected_variation_stock = min([v.stock for v in item.variations.all()])
                    if item.quantity + 1 <= selected_variation_stock:
                       item.quantity += 1
                       item.save()
                    else:
                      messages.error(request, "Not enough stock available.")
                      return redirect('cart')
                    # added by me/////////////////////

                else:
                    item= Cartitem.objects.create(product=product,quantity=1,user=current_user)
                    if len(product_variation) > 0:
                        item.variations.clear()
                        item.variations.add(*product_variation)
                    item.save()
                
                
            

        else:
            cart_item=Cartitem.objects.create(
                product= product,
                quantity=1,
                user=current_user,

            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            
            
            cart_item.save()

        # return HttpResponse(cart_item.product)
        # exit()
        return  redirect('cart')

        
   # if user is not authenticated
    else:
            
        product_variation=[]
        # this is in charge of selecting the various size or color of the product etc
        if request.method =='POST':
         for item in request.POST:
            key=item
            value=request.POST[key]
            try:
                variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                product_variation.append(variation)
                #    print (variation)
            except :
                pass
                

            
            
        #    color= request.POST['color']
        #    size= request.POST['size']
            

        # product=Product.objects.get(id=product_id)#get the product
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))# get the cart using the present in the session

        except Cart.DoesNotExist:
            cart=Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        is_cart_item_exists=Cartitem.objects.filter(product=product,cart=cart).exists()

        if is_cart_item_exists:
                cart_item=Cartitem.objects.filter(product=product, cart=cart)
                # existing variations coming from the database
                #    current variation is the product variation
                #    item_id is form the database


                ex_var_list=[]
                id=[]
                for item in cart_item:
                    existing_variation= item.variations.all()
                    ex_var_list.append(list(existing_variation))
                    id.append(item.id)
                    
                print(ex_var_list)


                if product_variation in ex_var_list:
                    #    increase the cart item Quantity
                    index=ex_var_list.index(product_variation)
                    item_id=id[index]
                    item=Cartitem.objects.get(product=product, id=item_id)
                    item.quantity +=1
                    item.save()
                    selected_variation_stock = min([v.stock for v in item.variations.all()])
                    if item.quantity + 1 <= selected_variation_stock:
                       item.quantity += 1
                       item.save()
                    else:
                       messages.error(request, "Not enough stock available.")
                       return redirect('cart')
                  



                else:
                    item= Cartitem.objects.create(product=product,quantity=1,cart=cart)
                    if len(product_variation) > 0:
                        item.variations.clear()
                        item.variations.add(*product_variation)
                    item.save()
                
                
            

        else:
            cart_item=Cartitem.objects.create(
                product= product,
                quantity=1,
                cart=cart,

            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            
            
            cart_item.save()

        # return HttpResponse(cart_item.product)
        # exit()
        return  redirect('cart')


    
    
def remove_cart(request,product_id,cart_item_id):
   
    product= get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item=Cartitem.objects.get(product=product,user=request.user,id=cart_item_id)
        else:
             cart=Cart.objects.get(cart_id=_cart_id (request))                
             cart_item=Cartitem.objects.get(product=product,cart=cart,id=cart_item_id)
        if cart_item.quantity > 1:
           cart_item.quantity -=1
           cart_item .save()
        else:
           cart_item.delete()
    except:
        pass     
    
    return redirect ('cart')

# this removes the cart item 
def remove_cart_item(request,product_id,cart_item_id):
    product=get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
         cart_item=Cartitem.objects.get(product=product,user=request.user,id=cart_item_id)
    else:
      cart=Cart.objects.get(cart_id=_cart_id (request))
      cart_item=Cartitem.objects.get(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request , total=0, quantity=0, cart_items=None):
    try:
      tax=0
      grand_total=0
      if request.user.is_authenticated:
        cart_items=Cartitem.objects.filter(user=request.user, is_active=True)
      else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=Cartitem.objects.filter(cart=cart, is_active=True)
           
      
      for cart_item in cart_items:
          total+=(cart_item.product.price*cart_item.quantity)
          quantity+=cart_item.quantity
          cart_item.selected_variation_stock = min([v.stock for v in cart_item.variations.all()])

      tax=(2*total)/100    
      grand_total= total + tax
    except ObjectDoesNotExist:  
        pass  
        

    context={
        'total':total,
         'quantity':quantity,
         'cart_items':cart_items,
         'tax':tax,
         'grand_total' : grand_total
    }
    

    return render(request,'cart.html',context)




@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
      tax=0
      grand_total=0
      if request.user.is_authenticated:
         cart_items=Cartitem.objects.filter(user=request.user, is_active=True)
      else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=Cartitem.objects.filter(cart=cart, is_active=True)
      for cart_item in cart_items:
          total+=(cart_item.product.price*cart_item.quantity)
          quantity+=cart_item.quantity
      tax=(2*total)/100    
      grand_total= total + tax
    except ObjectDoesNotExist:  
        pass  
        

    context={
        'total':total,
         'quantity':quantity,
         'cart_items':cart_items,
         'tax':tax,
         'grand_total' : grand_total
    }
    
    return render(request,'checkout.html',context)


