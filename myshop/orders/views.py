from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
from django.shortcuts import render, redirect


def order_create(request):
    cart=Cart(request)#we'll obtain the current cart from session
    if request.method=='POST':
        form=OrderCreateForm(request.POST)
        if form.is_valid():
            order=form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            #Clear the cart
            cart.clear()
            order_created.delay(order.id)
            request.session['order_id']=order.id

            return redirect(reverse('payment:process'))
    else:#Get request instanciates the OrderCreateForm form and renders the
        #orders/order/create.html
        form=OrderCreateForm()
    return render(request,
                 'orders/order/create.html',
                 {'cart':cart, 'form':form})


#Line 9. Post request validates the data sent in the request. If the data is
# valid , we create a new order in the database using order=form.save().

#we iterate over the cart items and create an OrderItem for each of them.
#Finally, we clear the cart content and render the template orders/order/created.html

# Create your views here.
