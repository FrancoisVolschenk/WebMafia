from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Game, Player, Role
import random
import string
from .populate_roles import *

def landing_page(request):
    if request.session.get("id", None) is not None:
        del request.session["id"]
    return render(request, 'web_ui/landing.html')

def verify_host(request) -> bool:
    try:
        player = Player.objects.get(id = request.session.get('id', 0))
        return player.is_host
    except:
        return False

def create_game(request, retry = False):
    if not retry:
        game_code = generate_game_code()
        game = Game.objects.create(code=game_code)
        try:
            role = Role.objects.get(name = "Host")
            Player.objects.create(name = f"Host {game_code}", game=game, is_host=True, role = role)
            request.session["id"] = Player.objects.get(name = f"Host {game_code}").id
            return render(request, 'web_ui/create_game.html', {"game": game})
        except:
            fill_missing_roles()
            return create_game(request, retry=True)
    else:
        return redirect("mafia-home")


def join_game(request):
    msg = ""
    if request.method == 'POST':
        try:
            game_code = request.POST.get('game_code')
            player_name = request.POST.get("player_name")
            game = Game.objects.filter(code=game_code).first()
            if game is not None:
                if Player.objects.filter(name = player_name).first() is None:
                    role = Role.objects.get(name = 'Pending')
                    Player.objects.create(name = player_name, game=game, role = role)
                    player = Player.objects.get(name = player_name)
                    request.session["id"] = player.id
                    return redirect('game_detail', game_code=game_code)
                else:
                    msg = "That name is already taken"
            else:
                msg = "Please ensure that your game token was entered correctly"
        except:
            msg = "Something went wrong. Please try again"
    return render(request, 'web_ui/join_game.html', {"msg": msg})

def game_detail(request, game_code):
    try:
        game = Game.objects.get(code=game_code, ended=False)
        players = game.player_set.all()
        return render(request, 'web_ui/game_detail.html', {'game': game, 'players': players})
    except:
        return redirect("mafia-home")

def start_game(request, game_code):
    if verify_host(request):
        try:
            game = Game.objects.get(code=game_code)
            if request.method == 'POST':
                selected_roles = request.POST.getlist('roles')
                num_mafia = int(request.POST.get("num_mafia", 1))
                distribute_roles(game, selected_roles, num_mafia)
                game.started = True
                game.save()
        except:
            return redirect("mafia-home")
        return render(request, 'web_ui/create_game.html', {"game": game})
    else:
        return redirect("game_detail", game_code)

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
        
def reset(request, game_code):
    try:
        print(f"Getting game {game_code} from DB")
        game = Game.objects.get(code=game_code)
        print(f"Got game {game.code}. Checking host")
        if verify_host(request):
            print("Host is ending game")
            for player in Player.objects.filter(game = game):
                print(f"Deleting player {player.name}")
                player.delete()
            game.ended = True
            game.save()
            return redirect("mafia-home")
        else:
            return redirect("game_detail", game_code)
    except:
        return redirect("mafia-home")
    
def get_players(request, game_code):
    try:
        game = Game.objects.get(code=game_code, ended=False)
        players = game.player_set.all()
        player_data = [{"name": player.name, "role": player.role.name} for player in players]
        return JsonResponse({"players": player_data, "started": game.started})
    except:
        return JsonResponse({"msg": "Game code not recognised"})

def get_role(request):
    player_id = int(request.session.get("id", -1))
    if player_id != -1:
        try:
            player = Player.objects.get(id = player_id)
            if not player.game.ended:
                return JsonResponse({"name": player.name, "role": player.role.name, "description": player.role.description})
        except:
            del request.session["id"]
            return redirect("mafia-home")
    return JsonResponse({"role": "not assigned", "description": ""}) 