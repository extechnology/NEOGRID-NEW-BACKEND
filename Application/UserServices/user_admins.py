from django.contrib import admin

from .user_models import (
    UserCartModel,UserCartItemModel,
    UserOrderModel,UserOrderItemModel,
    UserAddress, ContactModel
)


class UserCartItemInline(admin.TabularInline):
    model = UserCartItemModel
    extra = 0

@admin.register(UserCartModel)
class UserCartModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_value', 'created_at')
    search_fields = ('user__email',)
    inlines = [UserCartItemInline]


class UserOrderItemInline(admin.TabularInline):
    model = UserOrderItemModel
    extra = 0

@admin.register(UserOrderModel)
class UserOrderModelAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'status', 'total_value', 'created_at')
    list_filter = ('status',)
    search_fields = ('order_id', 'user__email', 'razorpay_order_id', 'razorpay_payment_id')
    inlines = [UserOrderItemInline]


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'phone_number', 'city', 'state', 'is_default')
    list_filter = ('is_default', 'state', 'city')
    search_fields = ('name', 'user__email', 'phone_number', 'city', 'state', 'pincode')


@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'service', 'is_read', 'created_at')
    list_filter = ('is_read', 'service')
    search_fields = ('name', 'phone', 'email', 'service', 'message')