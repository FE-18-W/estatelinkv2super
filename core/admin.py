from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import *


# ═══════════════════════════════════════
#  CUSTOM USER ADMIN - Strict Estate Isolation
# ═══════════════════════════════════════
class CustomUserAdmin(UserAdmin):
    """
    Strict estate isolation:
    - Superuser sees ALL users
    - Estate admin sees ONLY regular users from THEIR estate
    - Users without UserProfile are hidden from estate admins
    """
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Superuser sees everyone
        if request.user.is_superuser:
            return qs
        
        # Estate admin - strict filtering
        try:
            estate_admin = EstateAdmin.objects.get(user=request.user)
            if estate_admin.is_subscribed:
                # Get all user IDs that have a UserProfile in this estate
                allowed_user_ids = UserProfile.objects.filter(
                    estate=estate_admin.estate
                ).values_list('user_id', flat=True)
                
                # Only show those users AND ensure they are not staff/superusers
                return qs.filter(
                    id__in=allowed_user_ids,
                    is_staff=False,
                    is_superuser=False
                )
        except EstateAdmin.DoesNotExist:
            pass
        
        # If not authorized, show nothing
        return qs.none()
    
    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        if request.user.is_superuser:
            # Add approval status for superuser
            return list(list_display) + ['is_active']
        return list_display
    
    def approve_user(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} user(s) approved successfully.')
    approve_user.short_description = "✓ Approve selected users"
    
    def reject_user(self, request, queryset):
        queryset.delete()
        self.message_user(request, 'Selected user(s) rejected and deleted.')
    reject_user.short_description = "✗ Reject selected users"
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.is_superuser:
            actions['approve_user'] = (self.approve_user, 'approve_user', self.approve_user.short_description)
            actions['reject_user'] = (self.reject_user, 'reject_user', self.reject_user.short_description)
        return actions
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            # Remove permissions fieldset for estate admins
            fieldsets = [fs for fs in fieldsets if fs[0] != 'Permissions']
        return fieldsets
    
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        
        if obj:
            # Cannot view superusers or staff
            if obj.is_superuser or obj.is_staff:
                return False
            # Check if user belongs to admin's estate
            try:
                estate_admin = EstateAdmin.objects.get(user=request.user)
                if hasattr(obj, 'userprofile'):
                    return obj.userprofile.estate == estate_admin.estate
            except EstateAdmin.DoesNotExist:
                pass
            return False
        
        # Has view permission if approved estate admin
        try:
            estate_admin = EstateAdmin.objects.get(user=request.user)
            return estate_admin.is_subscribed
        except EstateAdmin.DoesNotExist:
            return False
    
    def has_add_permission(self, request):
        """Only superuser can add users via admin"""
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        
        if obj:
            # Cannot edit superusers or staff
            if obj.is_superuser or obj.is_staff:
                return False
            # Check estate
            try:
                estate_admin = EstateAdmin.objects.get(user=request.user)
                if estate_admin.is_subscribed and hasattr(obj, 'userprofile'):
                    return obj.userprofile.estate == estate_admin.estate
            except EstateAdmin.DoesNotExist:
                pass
            return False
        
        return True
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        
        if obj:
            if obj.is_superuser or obj.is_staff:
                return False
            try:
                estate_admin = EstateAdmin.objects.get(user=request.user)
                if estate_admin.is_subscribed and hasattr(obj, 'userprofile'):
                    return obj.userprofile.estate == estate_admin.estate
            except EstateAdmin.DoesNotExist:
                pass
            return False
        
        return False


# ═══════════════════════════════════════
#  ESTATE-SCOPED MODEL ADMINS
# ═══════════════════════════════════════
class EstateScopedAdmin(admin.ModelAdmin):
    """Base admin that limits queryset to the admin's own estate"""
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            estate_admin = EstateAdmin.objects.get(user=request.user)
            if estate_admin.is_subscribed:
                if hasattr(self.model, 'estate'):
                    return qs.filter(estate=estate_admin.estate)
        except EstateAdmin.DoesNotExist:
            pass
        return qs.none()
    
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            estate_admin = EstateAdmin.objects.get(user=request.user)
            return estate_admin.is_subscribed
        except EstateAdmin.DoesNotExist:
            return False
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        try:
            estate_admin = EstateAdmin.objects.get(user=request.user)
            return estate_admin.is_subscribed
        except EstateAdmin.DoesNotExist:
            return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            estate_admin = EstateAdmin.objects.get(user=request.user)
            if estate_admin.is_subscribed and obj and hasattr(obj, 'estate'):
                return obj.estate == estate_admin.estate
            return estate_admin.is_subscribed
        except EstateAdmin.DoesNotExist:
            return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            estate_admin = EstateAdmin.objects.get(user=request.user)
            if estate_admin.is_subscribed and obj and hasattr(obj, 'estate'):
                return obj.estate == estate_admin.estate
            return estate_admin.is_subscribed
        except EstateAdmin.DoesNotExist:
            return False


class WaterVendorAdmin(EstateScopedAdmin):
    list_display = ('name', 'estate', 'rating', 'is_subscribed')

class GarbageScheduleAdmin(EstateScopedAdmin):
    list_display = ('estate', 'collection_day', 'time')

class SecurityAlertAdmin(EstateScopedAdmin):
    list_display = ('title', 'estate', 'created_at', 'reported_by')

class LostItemAdmin(EstateScopedAdmin):
    list_display = ('title', 'estate', 'is_found', 'posted_by')

class GigAdmin(EstateScopedAdmin):
    list_display = ('title', 'estate', 'posted_by')

class MarketItemAdmin(EstateScopedAdmin):
    list_display = ('title', 'estate', 'price', 'featured', 'seller')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'estate', 'phone')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            estate_admin = EstateAdmin.objects.get(user=request.user)
            if estate_admin.is_subscribed:
                return qs.filter(
                    estate=estate_admin.estate,
                    user__is_superuser=False,
                    user__is_staff=False
                )
        except EstateAdmin.DoesNotExist:
            pass
        return qs.none()


# ═══════════════════════════════════════
#  ESTATE ADMIN MANAGEMENT (superuser only)
# ═══════════════════════════════════════
class EstateAdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'estate', 'is_subscribed', 'approved_by', 'approved_at')
    
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).none()
    
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser


# ═══════════════════════════════════════
#  REGISTER ALL MODELS
# ═══════════════════════════════════════
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Estate)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(WaterVendor, WaterVendorAdmin)
admin.site.register(WaterOrder)
admin.site.register(GarbageSchedule, GarbageScheduleAdmin)
admin.site.register(ServiceCategory)
admin.site.register(ServiceProvider)
admin.site.register(Booking)
admin.site.register(SecurityAlert, SecurityAlertAdmin)
admin.site.register(LostItem, LostItemAdmin)
admin.site.register(Gig, GigAdmin)
admin.site.register(MarketItem, MarketItemAdmin)
admin.site.register(BillReminder)
admin.site.register(EstateAdmin, EstateAdminAdmin)
admin.site.register(CustomTab)