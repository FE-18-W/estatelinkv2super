from django import forms
from django.contrib.auth.models import User
from .models import (
    WaterOrder, GasOrder, ShopOrder, SecurityAlert, LostItem, Gig, MarketItem, Booking,
    WaterVendor, GasVendor, ShopOwner, Estate
)


KENYA_CONSTITUENCIES = [
    ('', '-- Select your constituency --'),
    ('Changamwe', 'Changamwe'), ('Jomvu', 'Jomvu'), ('Kisauni', 'Kisauni'),
    ('Nyali', 'Nyali'), ('Likoni', 'Likoni'), ('Mvita', 'Mvita'),
    ('Msambweni', 'Msambweni'), ('Lunga Lunga', 'Lunga Lunga'),
    ('Matuga', 'Matuga'), ('Kinango', 'Kinango'),
    ('Kilifi North', 'Kilifi North'), ('Kilifi South', 'Kilifi South'),
    ('Kaloleni', 'Kaloleni'), ('Rabai', 'Rabai'), ('Ganze', 'Ganze'),
    ('Malindi', 'Malindi'), ('Magarini', 'Magarini'),
    ('Garsen', 'Garsen'), ('Galole', 'Galole'), ('Bura', 'Bura'),
    ('Lamu East', 'Lamu East'), ('Lamu West', 'Lamu West'),
    ('Taveta', 'Taveta'), ('Wundanyi', 'Wundanyi'), ('Mwatate', 'Mwatate'), ('Voi', 'Voi'),
    ('Garissa Township', 'Garissa Township'), ('Balambala', 'Balambala'),
    ('Lagdera', 'Lagdera'), ('Dadaab', 'Dadaab'), ('Fafi', 'Fafi'), ('Ijara', 'Ijara'),
    ('Wajir North', 'Wajir North'), ('Wajir East', 'Wajir East'),
    ('Tarbaj', 'Tarbaj'), ('Wajir West', 'Wajir West'),
    ('Eldas', 'Eldas'), ('Wajir South', 'Wajir South'),
    ('Mandera West', 'Mandera West'), ('Banissa', 'Banissa'),
    ('Mandera North', 'Mandera North'), ('Mandera South', 'Mandera South'),
    ('Mandera East', 'Mandera East'), ('Lafey', 'Lafey'),
    ('Moyale', 'Moyale'), ('North Horr', 'North Horr'), ('Saku', 'Saku'), ('Laisamis', 'Laisamis'),
    ('Isiolo North', 'Isiolo North'), ('Isiolo South', 'Isiolo South'),
    ('Igembe Central', 'Igembe Central'), ('Igembe South', 'Igembe South'),
    ('Igembe North', 'Igembe North'), ('Tigania West', 'Tigania West'),
    ('Tigania East', 'Tigania East'), ('North Imenti', 'North Imenti'),
    ('Buuri', 'Buuri'), ('Central Imenti', 'Central Imenti'), ('South Imenti', 'South Imenti'),
    ('Tharaka', 'Tharaka'), ('Maara', 'Maara'), ('Chuka/Igambang\'ombe', 'Chuka/Igambang\'ombe'),
    ('Mbeere North', 'Mbeere North'), ('Mbeere South', 'Mbeere South'),
    ('Manyatta', 'Manyatta'), ('Runyenjes', 'Runyenjes'),
    ('Mwingi North', 'Mwingi North'), ('Mwingi West', 'Mwingi West'),
    ('Mwingi Central', 'Mwingi Central'), ('Kitui West', 'Kitui West'),
    ('Kitui Rural', 'Kitui Rural'), ('Kitui Central', 'Kitui Central'),
    ('Kitui East', 'Kitui East'), ('Kitui South', 'Kitui South'),
    ('Masinga', 'Masinga'), ('Yatta', 'Yatta'), ('Kangundo', 'Kangundo'),
    ('Matungulu', 'Matungulu'), ('Kathiani', 'Kathiani'), ('Mavoko', 'Mavoko'),
    ('Machakos Town', 'Machakos Town'), ('Mwala', 'Mwala'),
    ('Mbooni', 'Mbooni'), ('Kilome', 'Kilome'), ('Kaiti', 'Kaiti'),
    ('Makueni', 'Makueni'), ('Kibwezi West', 'Kibwezi West'), ('Kibwezi East', 'Kibwezi East'),
    ('Kinangop', 'Kinangop'), ('Kipipiri', 'Kipipiri'), ('Ol Kalou', 'Ol Kalou'),
    ('Ol Jorok', 'Ol Jorok'), ('Ndaragwa', 'Ndaragwa'),
    ('Tetu', 'Tetu'), ('Kieni', 'Kieni'), ('Mathira', 'Mathira'),
    ('Othaya', 'Othaya'), ('Mukurweini', 'Mukurweini'), ('Nyeri Town', 'Nyeri Town'),
    ('Kangema', 'Kangema'), ('Mathioya', 'Mathioya'), ('Kiharu', 'Kiharu'),
    ('Kigumo', 'Kigumo'), ('Maragwa', 'Maragwa'), ('Kandara', 'Kandara'), ('Gatanga', 'Gatanga'),
    ('Gatundu South', 'Gatundu South'), ('Gatundu North', 'Gatundu North'),
    ('Juja', 'Juja'), ('Thika Town', 'Thika Town'), ('Ruiru', 'Ruiru'),
    ('Kiambu', 'Kiambu'), ('Kiambaa', 'Kiambaa'), ('Kabete', 'Kabete'),
    ('Kikuyu', 'Kikuyu'), ('Limuru', 'Limuru'), ('Lari', 'Lari'),
    ('Turkana North', 'Turkana North'), ('Turkana West', 'Turkana West'),
    ('Turkana Central', 'Turkana Central'), ('Loima', 'Loima'),
    ('Turkana South', 'Turkana South'), ('Turkana East', 'Turkana East'),
    ('Kapenguria', 'Kapenguria'), ('Sigor', 'Sigor'), ('Kacheliba', 'Kacheliba'), ('Pokot South', 'Pokot South'),
    ('Samburu West', 'Samburu West'), ('Samburu North', 'Samburu North'), ('Samburu East', 'Samburu East'),
    ('Kwanza', 'Kwanza'), ('Endebess', 'Endebess'), ('Saboti', 'Saboti'),
    ('Kiminini', 'Kiminini'), ('Cherangany', 'Cherangany'),
    ('Soy', 'Soy'), ('Turbo', 'Turbo'), ('Moiben', 'Moiben'),
    ('Ainabkoi', 'Ainabkoi'), ('Kapseret', 'Kapseret'), ('Kesses', 'Kesses'),
    ('Marakwet East', 'Marakwet East'), ('Marakwet West', 'Marakwet West'),
    ('Keiyo North', 'Keiyo North'), ('Keiyo South', 'Keiyo South'),
    ('Tinderet', 'Tinderet'), ('Aldai', 'Aldai'), ('Nandi Hills', 'Nandi Hills'),
    ('Chesumei', 'Chesumei'), ('Emgwen', 'Emgwen'), ('Mosop', 'Mosop'),
    ('Baringo North', 'Baringo North'), ('Baringo South', 'Baringo South'),
    ('Baringo Central', 'Baringo Central'), ('Eldama Ravine', 'Eldama Ravine'),
    ('Mogotio', 'Mogotio'), ('Tiaty', 'Tiaty'),
    ('Laikipia West', 'Laikipia West'), ('Laikipia East', 'Laikipia East'), ('Laikipia North', 'Laikipia North'),
    ('Molo', 'Molo'), ('Njoro', 'Njoro'), ('Naivasha', 'Naivasha'), ('Gilgil', 'Gilgil'),
    ('Kuresoi South', 'Kuresoi South'), ('Kuresoi North', 'Kuresoi North'),
    ('Subukia', 'Subukia'), ('Rongai', 'Rongai'), ('Bahati', 'Bahati'),
    ('Nakuru Town West', 'Nakuru Town West'), ('Nakuru Town East', 'Nakuru Town East'),
    ('Narok North', 'Narok North'), ('Narok East', 'Narok East'),
    ('Narok South', 'Narok South'), ('Narok West', 'Narok West'),
    ('Emurua Dikirr', 'Emurua Dikirr'), ('Kilgoris', 'Kilgoris'),
    ('Kajiado North', 'Kajiado North'), ('Kajiado Central', 'Kajiado Central'),
    ('Kajiado East', 'Kajiado East'), ('Kajiado West', 'Kajiado West'), ('Kajiado South', 'Kajiado South'),
    ('Bomet East', 'Bomet East'), ('Bomet Central', 'Bomet Central'),
    ('Chepalungu', 'Chepalungu'), ('Sotik', 'Sotik'), ('Konoin', 'Konoin'),
    ('Kericho', 'Kericho'), ('Ainamoi', 'Ainamoi'), ('Bureti', 'Bureti'),
    ('Belgut', 'Belgut'), ('Sigowet-Soin', 'Sigowet-Soin'),
    ('Kipkelion East', 'Kipkelion East'), ('Kipkelion West', 'Kipkelion West'),
    ('Lugari', 'Lugari'), ('Likuyani', 'Likuyani'), ('Malava', 'Malava'),
    ('Lurambi', 'Lurambi'), ('Navakholo', 'Navakholo'),
    ('Mumias West', 'Mumias West'), ('Mumias East', 'Mumias East'),
    ('Matungu', 'Matungu'), ('Butere', 'Butere'), ('Khwisero', 'Khwisero'),
    ('Shinyalu', 'Shinyalu'), ('Ikolomani', 'Ikolomani'),
    ('Vihiga', 'Vihiga'), ('Sabatia', 'Sabatia'), ('Hamisi', 'Hamisi'), ('Luanda', 'Luanda'), ('Emuhaya', 'Emuhaya'),
    ('Teso North', 'Teso North'), ('Teso South', 'Teso South'),
    ('Nambale', 'Nambale'), ('Matayos', 'Matayos'), ('Butula', 'Butula'),
    ('Funyula', 'Funyula'), ('Budalangi', 'Budalangi'),
    ('Ugenya', 'Ugenya'), ('Ugunja', 'Ugunja'), ('Alego Usonga', 'Alego Usonga'),
    ('Gem', 'Gem'), ('Bondo', 'Bondo'), ('Rarieda', 'Rarieda'),
    ('Kisumu East', 'Kisumu East'), ('Kisumu West', 'Kisumu West'),
    ('Kisumu Central', 'Kisumu Central'), ('Seme', 'Seme'),
    ('Nyando', 'Nyando'), ('Muhoroni', 'Muhoroni'), ('Nyakach', 'Nyakach'),
    ('Kasipul', 'Kasipul'), ('Kabondo Kasipul', 'Kabondo Kasipul'),
    ('Karachuonyo', 'Karachuonyo'), ('Rangwe', 'Rangwe'),
    ('Homa Bay Town', 'Homa Bay Town'), ('Ndhiwa', 'Ndhiwa'),
    ('Suba North', 'Suba North'), ('Suba South', 'Suba South'), ('Mbita', 'Mbita'),
    ('Rongo', 'Rongo'), ('Awendo', 'Awendo'), ('Suna East', 'Suna East'),
    ('Suna West', 'Suna West'), ('Uriri', 'Uriri'), ('Nyatike', 'Nyatike'),
    ('Kuria West', 'Kuria West'), ('Kuria East', 'Kuria East'),
    ('Bonchari', 'Bonchari'), ('South Mugirango', 'South Mugirango'),
    ('Bomachoge Borabu', 'Bomachoge Borabu'), ('Bobasi', 'Bobasi'),
    ('Bomachoge Chache', 'Bomachoge Chache'), ('Nyaribari Masaba', 'Nyaribari Masaba'),
    ('Nyaribari Chache', 'Nyaribari Chache'), ('Kitutu Chache North', 'Kitutu Chache North'),
    ('Kitutu Chache South', 'Kitutu Chache South'), ('Kitutu Masaba', 'Kitutu Masaba'),
    ('West Mugirango', 'West Mugirango'), ('North Mugirango', 'North Mugirango'), ('Borabu', 'Borabu'),
    ('Dagoretti North', 'Dagoretti North'), ('Dagoretti South', 'Dagoretti South'),
    ('Lang\'ata', 'Lang\'ata'), ('Kibra', 'Kibra'), ('Kasarani', 'Kasarani'),
    ('Roysambu', 'Roysambu'), ('Ruaraka', 'Ruaraka'),
    ('Embakasi South', 'Embakasi South'), ('Embakasi North', 'Embakasi North'),
    ('Embakasi Central', 'Embakasi Central'), ('Embakasi East', 'Embakasi East'),
    ('Embakasi West', 'Embakasi West'), ('Makadara', 'Makadara'),
    ('Kamukunji', 'Kamukunji'), ('Starehe', 'Starehe'), ('Mathare', 'Mathare'), ('Westlands', 'Westlands'),
]


class OrderWaterForm(forms.ModelForm):
    litres = forms.IntegerField(min_value=1, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Litres needed'}))
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Price (KSh)'}))

    class Meta:
        model = WaterOrder
        fields = ['vendor', 'litres', 'price']

    def __init__(self, *args, **kwargs):
        estate = kwargs.pop('estate', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if estate:
            qs = WaterVendor.objects.filter(estate=estate)
            if self.user:
                qs = qs.exclude(user=self.user)
            self.fields['vendor'].queryset = qs


class OrderGasForm(forms.ModelForm):
    kgs = forms.DecimalField(min_value=0.5, max_digits=6, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'placeholder': 'KGs of gas'}))
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Price (KSh)'}))
    block_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Block name'}))
    house_number = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'House number'}))

    class Meta:
        model = GasOrder
        fields = ['vendor', 'kgs', 'price', 'block_name', 'house_number']

    def __init__(self, *args, **kwargs):
        estate = kwargs.pop('estate', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if estate:
            qs = GasVendor.objects.filter(estate=estate)
            if self.user:
                qs = qs.exclude(user=self.user)
            self.fields['vendor'].queryset = qs


class OrderShopForm(forms.ModelForm):
    item_name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'Item name'}))
    quantity = forms.IntegerField(min_value=1, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Quantity'}))
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Price (KSh)'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'Description', 'rows': 3}))

    class Meta:
        model = ShopOrder
        fields = ['owner', 'item_name', 'quantity', 'price', 'description']

    def __init__(self, *args, **kwargs):
        estate = kwargs.pop('estate', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if estate:
            qs = ShopOwner.objects.filter(estate=estate)
            if self.user:
                qs = qs.exclude(user=self.user)
            self.fields['owner'].queryset = qs


class ReportIncidentForm(forms.ModelForm):
    class Meta:
        model = SecurityAlert
        fields = ['title', 'description']


class ReportLostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = ['title', 'description']


class PostGigForm(forms.ModelForm):
    class Meta:
        model = Gig
        fields = ['title', 'description']


class SellItemForm(forms.ModelForm):
    class Meta:
        model = MarketItem
        fields = ['title', 'description', 'price', 'image']


class BookFundiForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['provider', 'description']


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Create a strong password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password'}))
    estate = forms.ModelChoiceField(queryset=Estate.objects.all(), required=False, empty_label="-- Select your estate --")
    custom_estate = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Or type a new estate name'}))
    location = forms.ChoiceField(choices=KENYA_CONSTITUENCIES, required=False)
    custom_location = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'Or type a custom location'}))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'e.g., 0712345678'}))

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_confirm_password(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return p2

    def clean(self):
        cd = super().clean()
        if not cd.get('estate') and not cd.get('custom_estate'):
            raise forms.ValidationError("Please select or type an estate.")
        if not cd.get('location') and not cd.get('custom_location'):
            raise forms.ValidationError("Please select or type a location.")
        return cd

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        if commit:
            user.save()
            ce = self.cleaned_data.get('custom_estate', '')
            se = self.cleaned_data.get('estate')
            if ce:
                estate = Estate.objects.get_or_create(
                    name=ce,
                    defaults={'location': self.cleaned_data.get('location') or self.cleaned_data.get('custom_location', '')}
                )[0]
            else:
                estate = se
            loc = self.cleaned_data.get('location') or self.cleaned_data.get('custom_location', '')
            if loc and estate:
                estate.location = loc
                estate.save()
            user.userprofile.estate = estate
            user.userprofile.phone = self.cleaned_data.get('phone', '')
            user.userprofile.save()
        return user