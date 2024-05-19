from django.shortcuts import render, get_object_or_404

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

def product_list(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, "catalog/product_list.html", context)