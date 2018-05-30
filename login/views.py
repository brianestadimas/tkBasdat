from django.db import connection
from django.shortcuts import render

from login.auth_utils import generate_token, dictfetchall
from .forms import LoginForm, RegisterForm
import bcrypt


# Create your views here.

def index(request):
    if request.method == 'POST':
        form_data = LoginForm(request.POST)

        #  GENERAL IDEA:
        #      do query here on password and username
        #      check if found return request with token session

        if form_data.is_valid():
            hashed_password = None
            user_id = None
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM sion.user WHERE sion.user.email = %s", [form_data.username])
                rows = dictfetchall(cursor)
                if len(rows) == 0:      #gaketemu
                    return
                else:
                    user_id = rows[0]['email']
                    hashed_password = rows[0]['password']
                #  set hashed password if user with username found
                #  else return not found

            if hashed_password is not None and bcrypt.checkpw(form_data.password, hashed_password):
                # correct password > return to page wanted page and set session on request
                pass
        else:
            #  do something if form data is not valid
            pass

        request.session['user_session'] = generate_token(user_id)
        return
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form_data = RegisterForm(request.POST)
        to_be_saved_username = form_data.username
        to_be_saved_password = bcrypt.hashpw(form_data.password, bcrypt.gensalt())

        # save here to db
        with connection.cursor() as cursor:
            pass

        #  return with session

    else:
        form = RegisterForm()
        return render(request, 'login.html', {'form': form})



# FIXME : @brianestadimas why is it here? does it have anything related to login? is not even called anywhere (afaik, cmiiw). Also read comment below
# Whats in response?
# it wont get returned on all occassion? (even on post request), are you sure it is intended that its for not logged in user?
# whats with connection without any initiation, im pretty sure it will get error on runtime!
def donasi_org(request):
    if 'logged_in' not in request.session or not request.session['logged_in']:
        if (request.method == 'POST'):
            cursor = connection.cursor()
            cursor.execute("SELECT Nama from SION.ORGANISASI")
            selectnama = cursor.fetchone()
            response['selectnama'] = selectnama

            cursor.execute("SELECT Nominal from SION.DONATUR_ORGANISASI WHERE Organisasi = 'selected_name'")
            donasi = cursor.fetchone()
            donasi -= nominal
            cursor.execute("UPDATE DONATUR_ORGANISASI SET Nominal = donasi WHERE Organisasi = 'selected_name'")

    return render(request, 'donasi_org.html')
