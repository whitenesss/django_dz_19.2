from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.models import Category, Product, Blog


class BloglistView(ListView):
    model = Blog


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        object.views_count += 1
        object.save(update_fields=['views_count'])
        return object


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'description', 'image', 'is_active')
    success_url = reverse_lazy('catalog:blog')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)

        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'description', 'image', 'is_active')
    success_url = reverse_lazy('catalog:blog')

    def get_success_url(self):
        return reverse('catalog:blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog')


class CategoryListView(ListView):
    model = Category
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Product.objects.all()
        return context


def contact(request):
    return render(request, "catalog/contacts.html")


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    fields = ('name', 'description', 'price', 'category', 'image')
    success_url = reverse_lazy('catalog:index')


class ProductUpdateView(UpdateView):
    model = Product
    fields = ('name', 'description', 'price', 'category', 'image')
    success_url = reverse_lazy('catalog:index')

    def get_success_url(self):
        return reverse('catalog:product', args=[self.kwargs.get('pk')])


class CategoryCreateView(CreateView):
    model = Category
    fields = ('name', 'description')
    success_url = reverse_lazy('catalog:index')


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ('name', 'description')
    success_url = reverse_lazy('catalog:index')


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('catalog:index')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')


def toggle_activity(request, pk):
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.is_active:
        blog_item.is_active = False
    else:
        blog_item.is_active = True

    blog_item.save(update_fields=['is_active'])
    return redirect(reverse('catalog:blog'))
