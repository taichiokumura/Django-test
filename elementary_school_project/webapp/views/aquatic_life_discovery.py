from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import AquaticLifeEncyclopedia
from webapp.forms import AquaticLifeDiscoveryForm

def aquatic_discovery_view(request):
    form = AquaticLifeDiscoveryForm()
    discovered = False
    model_url = None
    searched_life = request.session.get('searched_life', [])
    max_items = 4

    if request.method == 'POST':
        form = AquaticLifeDiscoveryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            try:
                aquatic_life = AquaticLifeEncyclopedia.objects.get(name=name)
                if not any(item['name'] == name for item in searched_life):
                    aquatic_life.discovered = True
                    aquatic_life.save()
                    discovered = True
                    model_url = aquatic_life.model_file.url

                    searched_life.append({
                        'name': aquatic_life.name,
                        'model_url': aquatic_life.model_file.url
                    })
                    request.session['searched_life'] = searched_life
                else:
                    form.add_error('name', 'この生物は既に表示されています。')
            except AquaticLifeEncyclopedia.DoesNotExist:
                form.add_error('name', 'データベースに存在しない生物です。')
    
    model_data = [{'index': i, 'url': item['model_url']} for i, item in enumerate(searched_life)]
    
    context = {
        'form': form,
        'discovered': discovered,
        'model_url': model_url,
        'searched_life': searched_life,
        'model_data': model_data,
        'max_items': max_items,
    }

    return render(request, 'webtestapp/aquatic_life.html', context)

def reset_searched_life(request):
    if 'searched_life' in request.session:
        del request.session['searched_life']
    return redirect('webtestapp:aquatic_discovery_view')

