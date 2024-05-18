from django.shortcuts import render

from catalog.models import Category, Product


# Create your views here.
def home(request):
    category_list = Category.objects.all()
    product_list = Product.objects.all()
    context = {
        "category_list": category_list,
        "product_list": product_list,
    }

    return render(request, "catalog/home.html", context)


def contact(request):
    return render(request, "catalog/contacts.html")
