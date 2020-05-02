from django.shortcuts import render
from .models import Category,Phone,Watch,Value,CommonValue,Status,Image,Chart,Shipping
from .form import PhoneForm, ChartForm, BillingForm
from django.shortcuts import render, get_object_or_404, redirect
from decimal import *
from django.db.models import F,Q,Count
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
def index(request):
    # phones = Phone.objects.filter(status=1)
    id = request.GET.get('order')
    like = None
    chart= None
    count = 0
    images = Image.objects.filter(cat=4)
    brand = CommonValue.objects.filter(val=2,cat=4)
    if id:
        best_phones=Phone.objects.filter(brand__id=id).annotate(count=Count('like',distinct=True)).order_by('-count')[:3]
        phones = Phone.objects.filter(brand__id=id).annotate(count=Count('like',distinct=True)).order_by('-count')[4:]
    else:
        best_phones=Phone.objects.annotate(count=Count('like',distinct=True)).order_by('-count')[:3]
        phones = Phone.objects.annotate(count=Count('like',distinct=True)).order_by('-count')[4:]
    if request.user.is_authenticated:
        chart = Chart.objects.filter(user = request.user)
        count = Chart.objects.filter(user = request.user).count()
        like=Phone.objects.filter(like__username=request.user)
    
   
    context = {
        'best_phones' : best_phones,
        'images' : images,
        'chart'  : chart,
        'count'  : count,
        'like'   : like,
        'phones' : phones,
        'brands' : brand
    }
    return render(request, 'index.html',context)

def payment(request):

    return render(request, 'payment.html')

def createProduct(request):
    category = Category.objects.all()
    brand = CommonValue.objects.filter(val=2,cat=4)
    dual =  CommonValue.objects.filter(val=4,cat=4)
    os =  CommonValue.objects.filter(val=1,cat=4)
    status =  Status.objects.filter(id=1)
    if request.user.is_authenticated:
        if request.method == "POST":
            form=PhoneForm(request.POST, request.FILES or None)
            files =  request.FILES.getlist('image')
            # print('files=',files[0])
            if form.is_valid():
                product=form.save(commit=False)
                product.user=request.user
                product.picture='phone/' + str(files[0])
                product.save()

                for f in files:

                   gallery = Image(product=product,image=f )
                   gallery.save()
                return redirect('main:index')
            else:
                print(form.errors)
                # print('is_valid deyil')

    context = {
         'category':category,
         'brand': brand,
         'dual' : dual,
         'os'   : os,
         'status': status,

    }
    return render(request, 'createproduct.html',context)

def checkoutDetail(request):
    
    if request.user.is_authenticated:
        chart =Chart.objects.filter(user=request.user,order=1)
        total=0
        count = Chart.objects.filter(user = request.user).count()

        for i in chart:
            total+=i.total
        s =Shipping.objects.filter(user=request.user).first()
        print(s)
        context={
            'chart':chart,
            'subtotal':total ,
            'shipping': s.shipping,
            'total' : total + Decimal(s.shipping),
            'count' : count
        }
        if request.method == "POST":
            form=BillingForm(request.POST, request.FILES or None)
            if form.is_valid():
                bill=form.save(commit=False)
                bill.user=request.user
                bill.save()
                return redirect('main:payment')
            else:
                print(form.errors)    
    return render(request,'checkout.html',context)

def ProductDetailView(request,slug):
    count = 0
    chart = 0
    is_chart= False
    phone_id = Phone.objects.get(slug=slug)
    if request.user.is_authenticated:
        count = Chart.objects.filter(user = request.user).count()
        chart = Chart.objects.filter(user = request.user,product__id = phone_id.id).count()
        if chart>0:
           is_chart = True

    phone = get_object_or_404(Phone, pk=phone_id.id)
    image =Image.objects.filter(cat=4, product=phone_id.id)
    img1 = image[1]
    img0 = image[0]
    img2 = image[2]
    context = {
        'img0' : img0,
        'img1' : img1,
        'img2' : img2,
        'phone': phone,
        'count': count,
        'is_chart': is_chart
    }
    return render(request, 'detailproduct.html', context)

#JsonRespones
def chartDetail(request):
   
    print(request.user)
    
    if request.user.is_authenticated:
        count = Chart.objects.filter(user = request.user).count()

        chart = Chart.objects.filter(user = request.user)
        subTotal = 0
        for i in chart:
            subTotal += i.total
            if request.method == "POST":  
                form = ChartForm(request.POST, request.FILES or None)
                product=request.POST.getlist("product")
                quantity=request.POST.getlist("quantity") 
                total=request.POST.getlist("total")
                state=request.POST.get("state")
                country=request.POST.get("country")
                postcode=request.POST.get("postcode")
                shipping=request.POST.get("shipping")
                shipping_model=Shipping.objects.filter(user=request.user)
                if shipping_model:
                    Shipping.objects.filter(user = request.user).update(state=state,country=country,
                postcode=postcode,shipping=shipping )
                else:
                    s = Shipping(state=state,country=country,
                postcode=postcode,shipping=shipping,user=request.user )
                    s.save()

                if form.is_valid():
                    for i in range(0,len(product)):
                        Chart.objects.filter(user = request.user,product=product[i]).update(quantity=
                        quantity[i],total=total[i],order=1)
                    return redirect('main:checkout')
                else:
                    print(form.errors)
    else:
        return redirect('user:signup')
    context = {
        'chart' : chart,
        'subTotal' : subTotal,
        'count' : count
    }
    return render(request,'chart.html',context)

from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.urls import reverse_lazy,reverse

def ajaxify_cart_form(request):
    if request.is_ajax():
        if request.POST.get('user') is None:
            return HttpResponseRedirect(reverse_lazy('user:signup'))
        product_id=request.POST.get("product")
        quantity=request.POST.get('quantity')
        phone=Phone.objects.get(id=product_id)
        user = request.user
        chart = Chart.objects.filter(user = request.user, product = product_id)
        print(type(phone.price))
        print(type(quantity))
        if chart:
            value = True
        
        if Chart.objects.filter(user = int(user.id), product = int(product_id)):
            Chart.objects.get(user = int(user.id), product = int(product_id)).delete()
        else:
            a = Chart(product = phone, quantity= 1 ,total = Decimal(phone.price * int(quantity)) , user = user )
            a.save()
        return JsonResponse({
        'message': "successfully",
         }, status=201)


def ajaxify_like_form(request):
    if request.is_ajax():
        if request.POST.get('user') is None:
            return HttpResponseRedirect(reverse_lazy('user:signup'))
        product_id=request.POST.get("product")
        user = request.user
        phone=Phone.objects.get(id=product_id)
        print('salamaaa=',)
        if phone.like.filter(username=user.username).count():
            phone.like.remove(user)
        else:
            phone.like.add(user)
        return JsonResponse({
        'message': "successfully",
         }, status=201)

def ajaxify_detail_form(request):
    if request.is_ajax():
        if request.POST.get('user') is None:
            return HttpResponseRedirect(reverse_lazy('user:signup'))
        product_id=request.POST.get("product")
        quantity=request.POST.get('quantity')
        phone=Phone.objects.get(id=product_id)
        user = request.user
        chart = Chart.objects.filter(user = request.user, product = product_id)
        product_id=request.POST.get("product")
        user = request.user
        phone=Phone.objects.get(id=product_id)
        if Chart.objects.filter(user = int(user.id), product = int(product_id)):
            Chart.objects.get(user = int(user.id), product = int(product_id)).delete()
        else:
            a = Chart(product = phone, quantity= quantity ,total = Decimal(phone.price * int(quantity)) , user = user )
            a.save()
        return JsonResponse({
        'message': "successfully",
         }, status=201)


#Payment process
def process_payment(request):
    order_id = request.session.get('order_id')
    # order = get_object_or_404(Chart, id=order_id)
    host = request.get_host()
 
    paypal_dict = {
        'business': 'ravil.lavrenov405@gmail.com',
        'amount': 12202 ,
        'item_name': 'phone',
        'invoice': str(1),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('main:payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('main:payment_cancelled')),
    }
 
 
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'form': form})

# def paymentComplete(request):
# 	body = json.loads(request.body)
# 	# product = Phone.objects.get(id=body['35'])
# 	# Chart.objects.create(
# 	# 	product=product
# 	# 	)

# 	return JsonResponse('Payment completed!', safe=False)

@csrf_exempt
def payment_done(request):
    return render(request, 'payment_done.html')
 
 
@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html')