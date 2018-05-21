from django.shortcuts import render

# Create your views here.
def donasi_org(request):
    if 'logged_in' not in request.session or not request.session['logged_in']:
        if(request.method == 'POST'):
            cursor = connection.cursor()
            cursor.execute("SELECT Nama from SION.ORGANISASI")
            selectnama = cursor.fetchone()
            response['selectnama'] = selectnama
            
            cursor.execute("SELECT Nominal from SION.DONATUR_ORGANISASI WHERE Organisasi = 'selected_name'")
            donasi = cursor.fetchone()
            donasi-=nominal
            cursor.execute("UPDATE DONATUR_ORGANISASI SET Nominal = donasi WHERE Organisasi = 'selected_name'")
    return render(request, 'donasi_org.html')