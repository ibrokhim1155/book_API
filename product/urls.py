from django.urls import path
from product.views import product, category, group

urlpatterns = [

    path('', category.CategoriesDetailListApiView.as_view(), name='categories-detail-list'),
    path('category/<slug:slug>/', category.CategoryDetailApiView.as_view(), name='category-detail'),
    path('add-category/', category.CategoryAddView.as_view(), name='add-category'),
    path('category/<slug:category_slug>/<slug:slug>/', group.GroupDetailListApiView.as_view(), name='group-detail'),
    path('add-group/', group.GroupAddView.as_view(), name='add-group'),
    path('products/', product.ProductsListApiView.as_view(), name='products-list'),
    path('product/view/<slug:slug>/', product.ProductDetailApiView.as_view(), name='product-detail'),
    path('add-product/', product.ProductAddView.as_view(), name='add-product'),
]
