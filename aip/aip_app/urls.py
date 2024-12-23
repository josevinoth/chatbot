from django.urls import path
from . import views
from django.contrib.auth import views as auth_views #import this
urlpatterns = [
    # path('print_pdf', views.print_pdf, name='print_pdf'),  # Print PDF
    # path('asset_qr_id/<int:asset_qr_id>', views.qr_code_asset, name='asset_qr_id'),  # qr_code
    # path('goods_qr_id/<int:goods_qr_id>', views.qr_code_goods, name='goods_qr_id'),  # goods qr_code
    # path('registration_page', views.registration_page, name='registration_page'),  # Registration_page
    # path('login_page', views.login_page,name='login_page'),#Login_page
    # path('logout_page', views.logout_page,name='logout_page'),#Logout_page
    # path('home_page', views.home_page,name='home_page'),#Home_page
    # path('asset_insert', views.assetinfo_add,name='asset_insert'),#Add Asset
    # path('asset_update/<int:asset_id>/', views.assetinfo_add,name='asset_update'),#Update asset
    # path('asset_delete/<int:asset_id>/',views.asset_delete,name='asset_delete'), #Delete asset
    # path('asset_list/',views.asset_list,name='asset_list'), #List Asset
]