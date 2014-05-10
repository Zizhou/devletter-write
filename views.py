from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from display.models import Letter, UserProfile, Template

# Create your views here.

def example(request):
    return render(request, 'write/example.html')
@login_required
def send(request):
    return render(request, 'write/send.html')

@login_required
def letter(request, letter_id):

    letter = get_object_or_404(Letter.objects.filter(id = letter_id))
    user_profile = UserProfile.objects.get(user_id = request.user.id)

    if request.method == 'POST':
        print "stage 1"
        if request.POST.get('template-drop'):
            print request.POST.get('template-drop')
            letter.template = Template.objects.get(name = request.POST.get('template-drop'))
            letter.save()

    devname = letter.developer.name
    fillin = {'devname':devname, 'sig':user_profile.signature,}
    template = preview_template(letter.template.template, fillin)
    gamelist = letter.developer.game_set.all().order_by('name')
    template_list = Template.objects.all().order_by('name')
    display_text2 = False
    if template.find('<span id = "text2">') != -1:
        display_text2 = True

    #there are waaaay too many here...
    context = {
    'letter': letter,
    'devname' : devname,
    'gamelist' : gamelist,
    'game' : letter.game,
    'sig' : user_profile.signature,
    'template': template,
    'text1': letter.text1,
    'text2': letter.text2,
    'display_text2': display_text2,
    'template_list': template_list,
    }
     
    return render(request, 'write/letter.html', context)

def preview_template(template, form):
    formated = template.replace('{text1}', '<span id = "text1">TEXT GOES HERE</span>')
    formated = formated.replace('{text2}', '<span id = "text2">MORE TEXT GOES HERE</span>')
    formated = formated.replace('{game}', '<span id = "game">GAME TITLE HERE</span>')
    return formated.format(**form)

