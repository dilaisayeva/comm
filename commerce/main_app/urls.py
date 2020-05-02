
from django.urls import path,include,re_path
from . import views

app_name='main'

urlpatterns = [
	path("",views.index,name='index'),
	path("create/",views.createProduct,name='create'),
	path("detail/<slug:slug>/",views.ProductDetailView,name='detail'),
	path("ajaxify_cart_form/",views.ajaxify_cart_form),
    path("ajaxify_like_form/",views.ajaxify_like_form),
    path("ajaxify_detail_form/",views.ajaxify_detail_form),
	path('payment/',views.payment,name='payment'),
	path("chart/",views.chartDetail,name='chart'),
	path("checkout/",views.checkoutDetail,name="checkout"),
	path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),

	 

]