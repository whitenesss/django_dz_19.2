from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.models import Category, Product, Blog, Version
from catalog.forms import CategoryForm, ProductForm, VersionForm, ProductModeratorForm


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


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    login_url = '/users/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['versions'] = Version.objects.filter(product=self.object, is_activ_version=True)
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')
    login_url = '/users/'

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')
    login_url = '/users/'

    def get_success_url(self):
        return reverse('catalog:product', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        Version_Form = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = Version_Form(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = Version_Form(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']

        if formset.is_valid() and form.is_valid:
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.is_superuser:
            return ProductForm
        if user.has_perm("catalog.can_unpublish_product") and user.has_perm(
                "catalog.change_product_description") and user.has_perm(
                "catalog.change_product_category"):
            return ProductModeratorForm

        raise PermissionDenied


class CategoryCreateView(CreateView, LoginRequiredMixin):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        category = form.save()
        user = self.request.user
        category.owner = user
        category.save()
        return super().form_valid(form)


class CategoryUpdateView(UpdateView, LoginRequiredMixin):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:index')
    login_url = '/users/'


class CategoryDeleteView(DeleteView, LoginRequiredMixin):
    model = Category
    success_url = reverse_lazy('catalog:index')
    login_url = '/users/'


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')
    login_url = '/users/'


def toggle_activity(request, pk):
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.is_active:
        blog_item.is_active = False
    else:
        blog_item.is_active = True

    blog_item.save(update_fields=['is_active'])
    return redirect(reverse('catalog:blog'))
