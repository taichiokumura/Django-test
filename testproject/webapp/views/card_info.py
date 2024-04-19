from django.shortcuts import render
from webapp.models import CardInformation

def CardListView(request):
    template_name = 'webtestapp/card.html'
    ctx = {}
    qs = CardInformation.objects.all()
    ctx['object_list'] = qs

    return render(request, template_name, ctx)