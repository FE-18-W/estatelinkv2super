from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Water Delivery
    path('water/', views.water_view, name='water'),
    path('vendor-respond-water/<int:order_id>/', views.vendor_respond_water, name='vendor_respond_water'),
    
    # Garbage Schedule
    path('garbage/', views.garbage_view, name='garbage'),
    
    # Fundis & Help
    path('fundi/', views.fundi_view, name='fundi'),
    path('fundi-requests/', views.fundi_requests_view, name='fundi_requests'),
    path('admin-respond/<int:request_id>/', views.admin_respond_view, name='admin_respond'),
    
    # My Feedback
    path('my-feedback/', views.my_notifications_feedback, name='my_feedback'),
    
    # Security Alerts
    path('security/', views.security_view, name='security'),
    
    # Lost & Found
    path('lost-found/', views.lost_found_view, name='lost_found'),
    
    # Estate Jobs
    path('jobs/', views.jobs_view, name='jobs'),
    
    # Marketplace
    path('marketplace/', views.marketplace_view, name='marketplace'),
    
    # Rent & Bills
    path('bills/', views.bills_view, name='bills'),
    path('bills/mark-paid/<int:bill_id>/', views.mark_bill_paid, name='mark_bill_paid'),
    path('admin-confirm-bill/<int:bill_id>/', views.admin_confirm_bill, name='admin_confirm_bill'),
    path('admin-delete-bill/<int:bill_id>/', views.admin_delete_bill, name='admin_delete_bill'),
    
    # User Signup
    path('signup/', views.signup_view, name='signup'),
    
    # Approve Users (staff only)
    path('approve-users/', views.approve_users_view, name='approve_users'),
    
    # Admin Management (superuser only)
    path('admin-management/', views.admin_management_view, name='admin_management'),
    
    # Approve Estate Admins (staff only)
    path('approve-estate-admin/', views.approve_estate_admin_view, name='approve_estate_admin'),
    
    # Admin Actions (from dashboard)
    path('admin-approve-resident/<int:user_id>/', views.admin_approve_resident, name='admin_approve_resident'),
    path('admin-remove-resident/<int:user_id>/', views.admin_remove_resident, name='admin_remove_resident'),
    path('admin-add-water-vendor/', views.admin_add_water_vendor, name='admin_add_water_vendor'),
    path('admin-add-garbage-schedule/', views.admin_add_garbage_schedule, name='admin_add_garbage_schedule'),
    path('admin-resolve-alert/<int:alert_id>/', views.admin_resolve_alert, name='admin_resolve_alert'),
    path('admin-add-bill/', views.admin_add_bill, name='admin_add_bill'),
    
    # Vendor Promotion (estate admins)
    path('admin-promote-vendor/', views.admin_promote_vendor, name='admin_promote_vendor'),
    path('admin-add-gas-vendor/', views.admin_add_gas_vendor, name='admin_add_gas_vendor'),
    path('admin-add-shop-owner/', views.admin_add_shop_owner, name='admin_add_shop_owner'),
    path('request-vendor-deletion/<str:vendor_type>/<int:vendor_id>/', views.request_vendor_deletion, name='request_vendor_deletion'),
    path('approve-vendor-deletion/<int:deletion_request_id>/', views.approve_vendor_deletion, name='approve_vendor_deletion'),
    
    # Shop & Gas refill
    path('shop-gas/', views.shop_gas_view, name='shop_gas'),
    path('shop-gas/respond/<str:order_type>/<int:order_id>/', views.shop_gas_respond_view, name='shop_gas_respond'),
    
    # Manage Custom Tabs (estate admins)
    path('manage-tabs/', views.manage_tabs_view, name='manage_tabs'),
    path('delete-tab/<int:tab_id>/', views.delete_tab_view, name='delete_tab'),
    
    # Notifications
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/read-all/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    
    # Delete Broadcast (estate admins)
    path('delete-broadcast/<int:notification_id>/', views.delete_broadcast, name='delete_broadcast'),
    
    # API: Live Alert Count
    path('api/latest-alert-count/', views.latest_alert_count, name='latest_alert_count'),
    
    # Access Denied
    path('access-denied/', views.access_denied_view, name='access_denied'),
]