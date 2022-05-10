from django.shortcuts import render


def land(request):
    return render(request, '../templates/landing.html')
