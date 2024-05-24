from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import CategoryListView, ProductDetailView, CategoryCreateView, CategoryUpdateView, \
    CategoryDeleteView, BloglistView, BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView, \
    ProductCreateView, ProductUpdateView, ProductDeleteView, toggle_activity
from catalog.views import contact

app_name = CatalogConfig.name

urlpatterns = [
    path("", CategoryListView.as_view(), name="index"),
    path("contact/", contact, name="contact"),
    path("product/<int:pk>", ProductDetailView.as_view(), name="product"),
    path("catalog_create/", CategoryCreateView.as_view(), name="catalog_create"),
    path("product_create/", ProductCreateView.as_view(), name="product_create"),
    path("<int:pk>/catalog_update/", CategoryUpdateView.as_view(), name="catalog_update"),
    path("<int:pk>/product_update/", ProductUpdateView.as_view(), name="product_update"),
    path("<int:pk>/catalog_delete/", CategoryDeleteView.as_view(), name="catalog_delete"),
    path("<int:pk>/product_delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("blog/", BloglistView.as_view(), name="blog"),
    path("blog_create", BlogCreateView.as_view(), name="blog_create"),
    path("<int:pk>/blog_detail", BlogDetailView.as_view(), name="blog_detail"),
    path("<int:pk>/blog_update", BlogUpdateView.as_view(), name="blog_update"),
    path("<int:pk>/blog_delete", BlogDeleteView.as_view(), name="blog_delete"),
    path("activity<int:pk>/", toggle_activity, name="toggle_activity"),
]
