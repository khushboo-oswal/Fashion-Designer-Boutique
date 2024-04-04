from django.urls import path
from StyleSculptapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('index',views.index),
    path('register1',views.register),
    path('login1',views.user_login),
    path('logout',views.user_logout),
    path('about',views.about),
    path('contact',views.contact),
    path('main',views.main),
    path('collections',views.product),
    path('product_details/<pid>',views.product_details),
    path('catfilter/<cid>',views.catfilter),
    path('sorting/<sv>',views.sorting),
    path('filtering',views.filtering),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.removecart),
    path('quantity/<x>/<cid>',views.quantity),
    path('placeorder',views.placeorder),
    path('order_history',views.history),
    path('fetchorder',views.fetchorder),
    path('makepayment',views.makepayment),
    path('payment_success',views.payment_success),
    #path('success',views.success),
]

# Image Setting
#document_root is a path where we will save the image
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)