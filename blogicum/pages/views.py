from django.shortcuts import render


def about(request):
    tamplate = 'pages/about.html'
    return render(request, tamplate)


def rules(request):
    tamplate = 'pages/rules.html'
    return render(request, tamplate)
