from django.shortcuts import render

def index(request):
	return render(request, 'cpge_tw/index.html')