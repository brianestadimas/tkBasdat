from django.db import connection
from django.shortcuts import render, redirect
from django.http import HttpResponse
from login.auth_utils import dictfetchall
from .forms import LoginForm, RegisterForm, DonaturForm, RelawanForm, SponsorForm, OrganisasiForm
import bcrypt


# Create your views here.

def index(request):
    if 'logged_in' in request.session and request.session['logged_in']:
        if 'user_data' not in request.session:
            return render(request, 'message.html', {'message': "Already logged in, yet no role found!"})
        else:
            return redirect_on_role(request, request.session['user_data']['role'])

    if request.method == 'POST':
        form_data = LoginForm(request.POST)

        #  GENERAL IDEA:
        #      do query here on password and username
        #      check if found return request with token session

        if form_data.is_valid():
            password = None
            user_id = None
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM sion.user WHERE sion.user.email = %s",
                               [form_data.cleaned_data['username']])
                rows = dictfetchall(cursor)
                if len(rows) == 0:
                    return render(request, 'login.html',
                                  {'message': "Username not found", 'form': LoginForm(initial=form_data.cleaned_data)})
                else:
                    user_id = rows[0]['email']
                    password = rows[0]['password']
                #  set hashed password if user with username found
                #  else return not found
            if password is not None and form_data.cleaned_data['password'] == password:
                # correct password > return to page wanted page and set session on request
                request.session['logged_in'] = True
                role = None
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM sion.donatur WHERE sion.donatur.email = %s",
                                   [user_id])
                    rows = dictfetchall(cursor)

                    if len(rows) > 0:
                        request.session['user_data'] = {'role': 'donatur', 'email': user_id}
                        role = 'donatur'

                    cursor.execute("SELECT * FROM sion.relawan WHERE sion.relawan.email = %s",
                                   [user_id])
                    rows = dictfetchall(cursor)

                    if len(rows) > 0:
                        request.session['user_data'] = {'role': 'relawan', 'email': user_id}
                        role = 'relawan'

                    cursor.execute("SELECT * FROM sion.sponsor WHERE sion.sponsor.email = %s",
                                   [user_id])
                    rows = dictfetchall(cursor)

                    if len(rows) > 0:
                        request.session['user_data'] = {'role': 'sponsor',
                                                        'email': user_id}
                        role = 'sponsor'

                    if role is not None:
                        return redirect_on_role(role)

                    return render(request, 'login.html', {'message': "Cannot determine role", 'form': LoginForm()})

            else:
                # do something if form data is not valid
                return render(request, 'login.html', {'message': ":p wrong password", 'form': LoginForm()})

        else:
            #  do something if form data is not valid
            return render(request, 'login.html', {'message': "Invalid data", 'form': LoginForm()})


    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def redirect_on_role(request, role):
    if role is None:
        return render(request, 'message.html', {'message': "Already logged in, yet no role found!"})
    else:
        return render(request, 'message.html', {'message': "Welcome {}".format(role)})


def register(request):
    # resolve form
    if 'selected_role' not in request.session:
        form = RegisterForm()
    else:
        role = request.session['selected_role']
        if role == 'donatur':
            form = DonaturForm()
        if role == 'relawan':
            form = RelawanForm()
        if role == 'sponsor':
            form = SponsorForm()

    if request.method == 'POST':
        if 'selected_role' not in request.session:
            form_data = RegisterForm(request.POST)
            if form_data.is_valid():

                name = form_data.cleaned_data['name']
                username = form_data.cleaned_data['username']
                password = form_data.cleaned_data['password']
                address = form_data.cleaned_data['address']
                role = form_data.cleaned_data['role_selection']

                # save here to db
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO sion.user (email, password, nama, alamat_lengkap) VALUES (%s,%s,%s,%s)", [
                            username, name, password, address
                        ])
                    request.session['selected_role'] = role
                    request.session['registrar_email'] = username
                    request.session['logged_in'] = True

                    if role == 'donatur':
                        form = DonaturForm()
                    if role == 'relawan':
                        form = RelawanForm()
                    if role == 'sponsor':
                        form = SponsorForm()

                return render(request, 'registrasi.html', {'form': form})
            else:
                return render(request, 'registrasi.html', {'form': form, 'message': 'Invalid data !'})
        else:
            role = request.session['selected_role']
            # register organization first
            org_data = OrganisasiForm(request.POST)
            if org_data.is_valid():
                username = org_data.cleaned_data['username']
                website = org_data.cleaned_data['website']
                name = org_data.cleaned_data['name']
                provinsi = org_data.cleaned_data['provinsi']
                kabupaten = org_data.cleaned_data['kabupaten']
                kecamatan = org_data.cleaned_data['kecamatan']
                kelurahan = org_data.cleaned_data['kelurahan']
                kodepos = org_data.cleaned_data['kodepos']

                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO sion.organisasi (email_organisasi, website, nama, provinsi, kabupaten_kota, kecamatan, kelurahan, kode_pos, status_verifikasi) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        [
                            username, website, name, provinsi, kabupaten, kecamatan, kelurahan, kodepos, 'Not Verified'
                        ])

            with connection.cursor() as cursor:
                user_email = request.session['registrar_email']

                if role == 'donatur':
                    form_data = DonaturForm(request.POST)
                    if (form_data.is_valid()):
                        saldo = form_data.cleaned_data['saldo']

                        with connection.cursor() as cursor:
                            cursor.execute(
                                "INSERT INTO sion.donatur (email, saldo) VALUES (%s,%s)",
                                [
                                    user_email, saldo
                                ])

                if role == 'relawan':
                    form_data = RelawanForm(request.POST)
                    if (form_data.is_valid()):
                        birthdate = form_data.cleaned_data['birthdate']
                        phonenumber = form_data.cleaned_data['phonenumber']
                        # skills = form_data.cleaned_data['skills']                  *harusnya ada 1 tabel lg keahlian karyawan

                        with connection.cursor() as cursor:
                            cursor.execute(
                                "INSERT INTO sion.relawan (email, no_hp, tanggal_lahir) VALUES (%s,%s,%s)",
                                [
                                    user_email, phonenumber, birthdate
                                ])

                if role == 'sponsor':
                    form_data = SponsorForm(request.POST)
                    if (form_data.is_valid()):
                        logo = form_data.cleaned_data['logo']

                        with connection.cursor() as cursor:
                            cursor.execute(
                                "INSERT INTO sion.relawan (email, logo) VALUES (%s,%s)",
                                [
                                    user_email, logo
                                ])

                request.session['user_data'] = {'role': role, 'email': user_email}
                return redirect_on_role(request, role)

    else:
        return render(request, 'registrasi.html', {'form': form})


def logout(request, *args, **kwargs):
    request.session.clear()
    request.session.modified = True
    return redirect('user/login/')

# FIXME : @brianestadimas why is it here? does it have anything related to login? is not even called anywhere (afaik,
#  cmiiw). Also read comment below Whats in response? it wont get returned on all occassion? (even on post request),
# are you sure it is intended that its for not logged in user? whats with connection without any initiation,
# im pretty sure it will get error on runtime!
# def donasi_org(request):
#     if 'logged_in' not in request.session or not request.session['logged_in']:
#         if (request.method == 'POST'):
#             cursor = connection.cursor()
#             cursor.execute("SELECT Nama from SION.ORGANISASI")
#             selectnama = cursor.fetchone()
#             response['selectnama'] = selectnama
#
#             cursor.execute("SELECT Nominal from SION.DONATUR_ORGANISASI WHERE Organisasi = 'selected_name'")
#             donasi = cursor.fetchone()
#             donasi -= nominal
#             cursor.execute("UPDATE DONATUR_ORGANISASI SET Nominal = donasi WHERE Organisasi = 'selected_name'")
#
#     return render(request, 'donasi_org.html')
