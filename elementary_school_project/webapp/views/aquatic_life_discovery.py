from django.shortcuts import render, get_object_or_404
from webapp.models import AquaticLifeEncyclopedia
from webapp.forms import AquaticLifeDiscoveryForm

def aquatic_discovery_view(request):
    form = AquaticLifeDiscoveryForm()
    discovered = False
    model_url = None
    searched_life = request.session.get('searched_life', [])

    if request.method == 'POST':
        form = AquaticLifeDiscoveryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            try:
                aquatic_life = AquaticLifeEncyclopedia.objects.get(name=name)
                aquatic_life.discovered = True
                aquatic_life.save()
                discovered = True
                model_url = aquatic_life.model_file.url
                searched_life.append({
                    'name': aquatic_life.name,
                    'model_url': aquatic_life.model_file.url
                })
                request.session['searched_life'] = searched_life
            except AquaticLifeEncyclopedia.DoesNotExist:
                form.add_error('name', 'Organism not found in the database.')
    
    context = {
        'form': form,
        'discovered': discovered,
        'model_url': model_url,
        'searched_life': searched_life,
    }

    return render(request, 'webtestapp/aquatic_life.html', context)