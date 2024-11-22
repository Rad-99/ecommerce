from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm




urlpatterns = [
  
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path("category/<slug:val>", views.CategoryView.as_view(),name="category"),
    #path("category-title/<val>", views.CategoryTitle.as_view(),name="category-title"),
    path("product-detail/<int:pk>", views.ProductDetail.as_view(),name="product-detail"),
    path("profile/", views.ProfileView.as_view(),name="profile"),
    # path("name/", views.ProfileView.as_view(),name="name"),
    # path("mobilenumber/", views.ProfileView.as_view(),name="mobilenumber"),
    path("details/", views.details,name="details"),
    path("updatedetails/<int:pk>",views.Updatedetails.as_view(),name="updatedetails"),

    #login Authentication

    path("registration/", views.CustomerregistrationView.as_view(),name="customerregistration"),
    path('account/login/', views.CustomLoginView.as_view(), name='login'),

    # path("account/login/", auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm),name='login'),
   
    path("passwordchange/", auth_view.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordChangeForm, success_url=
    '/passwordchangedone'),name = 'passwordchange'),

    path('passwordchangedone/', auth_view. PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html') , name='passwordchangedone'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

    #passwordreset
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',
    form_class=MyPasswordResetForm) , name='password_reset'),
   
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html') ,
    name='password_reset_done' ),
    
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm) , name='password_reset_confirm'),
    
    path('password-reset-complete/', auth_view. PasswordResetCompleteView. as_view(template_name='app/password_reset_complete.html') , name='password_reset_complete'),

    #cart
    # path('pluscart/', views.plus_cart),
    
    
    path('cart/', views.show_cart, name='cart'),  # This is the URL for the cart view
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('remove-item/<int:prod_id>/', views.remove_item, name='remove_item'),
    path('place-order/', views.place_order, name='place_order'), 
    path('order-confirmation/<uuid:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('delete-order/<uuid:order_id>/', views.delete_order, name='delete_order'),
    
   

   

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)        