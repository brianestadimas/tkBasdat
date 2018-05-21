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

    if cursorSelect('*','SION.RELAWAN'):

    	if cursorSelect('nama','SION.RELAWAN') :
    		response['nama'] = cursorSelect('nama','SION.RELAWAN')[0]

    	if selectcursorSelect('nama','SION.DONATUR') :
    		response['nama'] = cursorSelect('nama','SION.DONATUR')[0]
    		#....
    	if cursorSelect('nama','SION.SPONSOR') :
    		response['nama'] = cursorSelect('nama','SION.SPONSOR')[0]

def cursorSelect(param, database):
	cursor=connection.cursor()
	cursor.execute("SELECT " + param + " from " + database + " where EMAIL='"+email+"'")
	return cursor.fetchone()

def profile_org_all()
	
    ######## Brian ##########



