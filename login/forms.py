from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


ROLE_CHOICES = (
    ('donatur', 'Donatur'),
    ('sponsor', 'Sponsor'),
    ('relawan', 'Relawan'),
)


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Alamat Lengkap', widget=forms.Textarea(attrs={'class': 'form-control'}))
    role_selection = forms.ChoiceField(
        required=True,
        choices=ROLE_CHOICES,
        label='Role',
        widget=forms.Select(attrs={'class': 'form-control'}))


class OrganisasiForm(forms.Form):
    kecamatan = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    kabupaten = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    provinsi = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    kodepos = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    kelurahan = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    website = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))


class DonaturForm(OrganisasiForm):
    saldo = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-contol'}))



class SponsorForm(OrganisasiForm):
    logo = forms.FileField()



class RelawanForm(OrganisasiForm):
    birthdate = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y', attrs={'class': 'form-control', 'type': 'date'}))
    phonenumber = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    skills = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

