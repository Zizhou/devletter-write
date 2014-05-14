from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from submit.models import Game, Developer
from display.models import Letter, UserProfile, Template

# Create your views here.

def example(request):
    return render(request, 'write/example.html')

@login_required
def send(request):
    if request.method == 'POST' and request.POST.get('letter_id'):
        letter = Letter.objects.get(id = request.POST.get('letter_id'))
        letter.game = Game.objects.get(name = request.POST.get('game-drop'))
        letter.text1 = request.POST.get('text_1')
        if request.POST.get('text_2'):
            letter.text2 = request.POST.get('text_2')
        letter.written = True
        letter.save()

        complete_letter = send_template(letter)
        next_in_queue = False
        next_letter = 0
        #user profile shortcut
        up = UserProfile.objects.get(user_id = request.user.id) 
        if up.devlist.exclude(written = True).count() > 0:
            next_in_queue = True
            next_letter = up.devlist.exclude(written = True)[0].id

        print 'next_letter is ' + str(next_letter)
        context = {
        'next_in_queue': next_in_queue,
        'next_letter': next_letter,
        'letter' : complete_letter,
        }

        return render(request, 'write/send.html', context)

    return render(request, 'write/example.html')
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

def send_template(letter):
    
    return '''TODO temporary letter'''
