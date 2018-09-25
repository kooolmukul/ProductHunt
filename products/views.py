from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone
# Create your views here.


def home(request):
    products = Product.objects

    return render(request, 'product/home.html', {'products': products})


@login_required(login_url="/accounts/signin")
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES.get('icon') and request.FILES.get('image'):
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            return redirect('/product/' + str(product.id))
        else:
            return render(request, 'product/create.html', {'error': "Please fill all Fields!"})
    else:
        return render(request, 'product/create.html')


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product/detail.html', {'product': product})


@login_required(login_url="/accounts/signin")
def upvote(request, product_id):

    product = get_object_or_404(Product, pk=product_id)
    product.votes_total += 1
    product.save()
    return redirect('/product/' + str(product.id))
