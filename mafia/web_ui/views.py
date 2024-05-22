from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Game, Player, Role
import random
import string

roles = ["Mafia", "Villager", "Doctor", "Cop"]

def landing_page(request):
    return render(request, 'web_ui/landing.html')

def create_game(request):
    game_code = generate_game_code()
    game = Game.objects.create(code=game_code)
    role = Role.objects.get(id = 6)
    Player.objects.create(name = "Host", game=game, is_host=True, role = role)
    request.session["id"] = Player.objects.get(name = "Host").id
    return render(request, 'web_ui/create_game.html', {"game": game})

def join_game(request):
    msg = ""
    if request.method == 'POST':
        game_code = request.POST.get('game_code')
        player_name = request.POST.get("player_name")
        game = Game.objects.filter(code=game_code).first()
        if game is not None:
            if Player.objects.filter(name = player_name).first() is None:
                role = Role.objects.get(id = 7)
                Player.objects.create(name = player_name, game=game, role = role)
                player = Player.objects.get(name = player_name)
                request.session["id"] = player.id
                return redirect('game_detail', game_code=game_code)
            else:
                msg = "That name is already taken"
        else:
            msg = "Please ensure that your game token was entered correctly"
    return render(request, 'web_ui/join_game.html', {"msg": msg})

def game_detail(request, game_code):
    try:
        game = Game.objects.get(code=game_code)
        players = game.player_set.all()
        return render(request, 'web_ui/game_detail.html', {'game': game, 'players': players})
    except:
        return redirect("mafia-home")

def start_game(request, game_code):
    game = Game.objects.get(code=game_code)
    if request.method == 'POST':
        selected_roles = request.POST.getlist('roles')
        num_mafia = int(request.POST.get("num_mafia", 1))
        distribute_roles(game, selected_roles, num_mafia)
        game.started = True
        game.save()
    return render(request, 'web_ui/create_game.html', {"game": game})

def generate_game_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def distribute_roles(game, selected_roles, num_mafia):
    players = list(Player.objects.filter(is_host = False))

    random.shuffle(players)

    mafia = Role.objects.get(name = 'Mafia')
    # Assign Mafia roles
    for i in range(num_mafia):
        players[i].role = mafia
        players[i].save()

    remaining_roles = selected_roles.copy()
    print(remaining_roles)

    # Assign the remaining roles
    for player in players[num_mafia:]:
        if remaining_roles:
            role = remaining_roles.pop(0)
            player_role = Role.objects.get(name = role)
            player.role = player_role
            player.save()
        else:
            player_role = Role.objects.get(name = 'Villager')
            player.role = player_role
            player.save()
        
def reset(request):
    Player.objects.all().delete()
    Game.objects.all().delete()
    return redirect("mafia-home")

def get_players(request, game_code):
    game = Game.objects.get(code=game_code)
    players = game.player_set.all()
    player_data = [{"name": player.name, "role": player.role.name} for player in players]
    return JsonResponse({"players": player_data, "started": game.started})

def get_role(request):
    player_id = int(request.session.get("id", -1))
    if player_id != -1:
        player = Player.objects.get(id = player_id)
        return JsonResponse({"name": player.name, "role": player.role.name, "description": player.role.description})
    return JsonResponse({"role": "not assigned", "description": ""}) 
# TODO: Handle incorrect game pins