from django.shortcuts import render, get_object_or_404

from display.models import Letter, UserProfile, Template

# Create your views here.

def example(request):
    return render(request, 'write/example.html')

def letter(request, letter_id):
    letter = get_object_or_404(Letter.objects.filter(id = letter_id))
    user_profile = UserProfile.objects.get(user_id = request.user.id)
 
    devname = letter.developer.name
    fillin = {'devname':devname, 'sig':user_profile.signature,}
    template = preview_template(letter.template.template, fillin)
    gamelist = letter.developer.game_set.all().order_by('name')
    context = {
    'devname' : devname,
    'gamelist' : gamelist,
    'game' : letter.game,
    'sig' : user_profile.signature,
    'template': template,
    }
     
    return render(request, 'write/letter.html', context)

def preview_template(template, form):
    formated = template.replace('{text1}', '<span id = "text1">text1</span>')
    formated = formated.replace('{text2}', '<span id = "text2">text2</span>')
    formated = formated.replace('{game}', '<span id = "game">game</span>')
    return formated.format(**form)

    
