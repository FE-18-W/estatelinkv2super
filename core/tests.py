import os
from io import StringIO
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Estate, EstateAdmin, GasVendor, ShopOwner, UserProfile, VendorDeletionRequest, WaterVendor


class VendorManagementFlowTests(TestCase):
    def setUp(self):
        self.estate = Estate.objects.create(name='Oak Ridge', location='Zone A')
        self.admin = User.objects.create_user(
            username='estate_admin',
            email='estate_admin@example.com',
            password='secret123',
            is_staff=True,
            is_active=True,
        )
        self.admin.is_active = True
        self.admin.save(update_fields=['is_active'])
        UserProfile.objects.filter(user=self.admin).update(estate=self.estate)
        EstateAdmin.objects.create(
            user=self.admin,
            estate=self.estate,
            is_subscribed=True,
            can_manage_services=True,
            can_manage_users=True,
            can_manage_requests=True,
            can_manage_alerts=True,
            can_manage_bills=True,
            can_manage_tabs=True,
            can_view_analytics=True,
            can_broadcast=True,
        )

        self.resident = User.objects.create_user(
            username='resident_one',
            email='resident_one@example.com',
            password='resident123',
            is_active=True,
        )
        self.resident.is_active = True
        self.resident.save(update_fields=['is_active'])
        UserProfile.objects.filter(user=self.resident).update(estate=self.estate)

        self.superuser = User.objects.create_superuser(
            username='superadmin',
            email='superadmin@example.com',
            password='super123',
        )

    def test_estate_admin_can_add_water_vendor_and_assign_user(self):
        self.client.force_login(self.admin)

        response = self.client.post(reverse('admin_add_water_vendor'), {
            'name': 'Blue Nile Water',
            'username': 'resident_one',
        })

        self.assertEqual(response.status_code, 302)
        water_vendor = WaterVendor.objects.get(name='Blue Nile Water', estate=self.estate)
        self.assertEqual(water_vendor.user, self.resident)
        self.assertTrue(water_vendor.is_subscribed)

    def test_vendor_delete_requires_admin_management_approval(self):
        self.client.force_login(self.admin)
        gas_vendor = GasVendor.objects.create(name='Glow Gas', estate=self.estate, is_subscribed=True)

        response = self.client.post(reverse('request_vendor_deletion', args=['gas', gas_vendor.id]))

        self.assertEqual(response.status_code, 302)
        deletion_request = VendorDeletionRequest.objects.get(vendor_type='gas', vendor_id=gas_vendor.id)
        self.assertEqual(deletion_request.status, 'pending')
        self.assertEqual(deletion_request.requested_by, self.admin)
        self.assertTrue(GasVendor.objects.filter(id=gas_vendor.id).exists())

        self.client.force_login(self.superuser)
        approve_response = self.client.post(reverse('approve_vendor_deletion', args=[deletion_request.id]), {
            'action': 'approve',
        })

        self.assertEqual(approve_response.status_code, 302)
        deletion_request.refresh_from_db()
        self.assertEqual(deletion_request.status, 'approved')
        self.assertFalse(GasVendor.objects.filter(id=gas_vendor.id).exists())

    def test_estate_admin_can_request_shop_owner_deletion_only(self):
        self.client.force_login(self.admin)
        shop_owner = ShopOwner.objects.create(name='Market Hub', estate=self.estate, is_subscribed=True)

        response = self.client.post(reverse('request_vendor_deletion', args=['shop', shop_owner.id]))

        self.assertEqual(response.status_code, 302)
        deletion_request = VendorDeletionRequest.objects.get(vendor_type='shop', vendor_id=shop_owner.id)
        self.assertEqual(deletion_request.status, 'pending')
        self.assertEqual(deletion_request.requested_by, self.admin)
        self.assertTrue(ShopOwner.objects.filter(id=shop_owner.id).exists())


class SuperuserDeploymentTests(TestCase):
    def test_ensure_superuser_command_restores_login_account(self):
        stale_user = User.objects.create_user(
            username='felixm',
            email='old@example.com',
            password='old-password',
            is_active=False,
            is_staff=False,
            is_superuser=False,
        )
        stale_user.refresh_from_db()
        self.assertFalse(stale_user.is_active)

        with patch.dict(os.environ, {
            'DJANGO_SUPERUSER_USERNAME': 'felixm',
            'DJANGO_SUPERUSER_EMAIL': 'felixochieng5785@gmail.com',
            'DJANGO_SUPERUSER_PASSWORD': '171630m@felix',
        }, clear=False):
            call_command('ensure_superuser', stdout=StringIO())

        stale_user.refresh_from_db()
        self.assertTrue(stale_user.is_active)
        self.assertTrue(stale_user.is_staff)
        self.assertTrue(stale_user.is_superuser)
        self.assertEqual(stale_user.email, 'felixochieng5785@gmail.com')
        self.assertTrue(stale_user.check_password('171630m@felix'))
        self.assertTrue(self.client.login(username='felixm', password='171630m@felix'))
