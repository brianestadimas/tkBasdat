from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from login.views import role

response = {}
def index(request):
	cursor=connection.cursor()
    email = request.POST['email']
    global email
    password = request.POST['password']

    if cursorSelect('*','SION.USER',email):

    	if cursorSelect('nama','SION.RELAWAN') :
    		response['nama'] = cursorSelect('nama','SION.RELAWAN',email,)[0]
			response['email'] = cursorSelect('email','SION.RELAWAN',email)[0]
			response['kecamatan'] = cursorSelect('kecamatan','SION.RELAWAN',email)[0]
			response['kabupaten'] = cursorSelect('kabupaten','SION.RELAWAN',email)[0]
			response['provinsi'] = cursorSelect('email','SION.RELAWAN',email)[0]
			response['kodepos'] = cursorSelect('kodepos','SION.RELAWAN',email)[0]
			response['kelurahan'] = cursorSelect('kelurahan','SION.RELAWAN',email)[0]
			return (request, 'profil_relawan.html', response)

    	elif selectcursorSelect('nama','SION.DONATUR') :
    		response['nama'] = cursorSelect('nama','SION.DONATUR',email)[0]
    		#....
    	elif cursorSelect('nama','SION.SPONSOR') :
    		response['nama'] = cursorSelect('nama','SION.SPONSOR',email)[0]

    	elif cursorSelect('nama','SION.PENGURUS') :
    		response['nama'] = cursorSelect('nama','SION.PENGURUS',email)[0]



     ######## Brian ##########
     if cursorSelect("*", 'SION.ORGANISASI'):
     	showAllOrg()


def cursorSelect(param, database, email):
	cursor=connection.cursor()
	cursor.execute("SELECT " + param + " from " + database + " where EMAIL= "+email+"")
	return cursor.fetchone()

def cursor(param, database):
	cursor=connection.cursor()
	cursor.execute("SELECT " + param + " from " + database)
	return cursor.fetchone()

def showAllOrg():
	response['nama_org'] = cursor('nama','SION.ORGANISASI')
	response['website_org'] = cursor('website','SION.ORGANISASI')

def showClickedOrg(email):
	response['nama_org'] = cursor('nama','SION.ORGANISASI', email)
	response['website_org'] = cursor('website','SION.ORGANISASI', email)
	response['provinsi_org'] = cursor('nama','SION.ORGANISASI', email)
	response['kabupaten_kota_org'] = cursor('kabupaten_kota','SION.ORGANISASI', email)
	response['kecamatan_org'] = cursor('kecamatan','SION.ORGANISASI', email)
	response['kelurahan_org'] = cursor('kelurahan','SION.ORGANISASI', email)
	response['kode_pos_org'] = cursor('kode_pos','SION.ORGANISASI', email)
	response['status_verifikasi_org'] = cursor('status_verifikasi','SION.ORGANISASI', email)

	for elem in cursorSelect('nama','')
		response['sponsor_list'] = cursor('status_verifikasi','SION.ORGANISASI', email)

	response['donatur_list'] = cursor('status_verifikasi','SION.ORGANISASI', email)
	response['donatur_list'] = cursor('status_verifikasi','SION.ORGANISASI', email)