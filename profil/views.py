from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from login.views import role

response = {}
def index(request):
	cursor=connection.cursor()
    email = request.POST['email']
    password = request.POST['password']
    cursor.execute("SELECT nama from SION.RELAWAN where EMAIL='"+email+"'")
    select=cursor.fetchone()
    profile_user(select)

def profile_user(select)
	cursor=connection.cursor()
    if select:
    	cursor.execute("SELECT nama from SION.DONATUR where EMAIL='"+email+"'")
    	select=cursor.fetchone()
    	if select :
    		response['nama'] = select[0]
    		#........
    	cursor.execute("SELECT nama from SION.RELAWAN where EMAIL='"+email+"'")
    	select=cursor.fetchone()
    	elif select :
    		response['nama'] = select[0]
    		#....
    	cursor.execute("SELECT nama from SION.SPONSOR where EMAIL='"+email+"'")
    	select=cursor.fetchone()
    	elif select :
    		response['nama'] = select[0]

def 
	
    ######## Brian ##########



