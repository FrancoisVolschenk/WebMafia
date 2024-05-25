from .models import Role

ROLE_INSERTIONS = [
    {"name" : 'Host', "description": 'Your job is to facilitate the game. Explain the rules, and narrate the day/night cycles.', "playable": False, "optional": False},
    {"name" : 'Pending', "description": 'You are in the lobby. Waiting for the game to start and roles to be assigned', "playable": False, "optional": False},
    {"name" : 'Mafia', "description": 'Once per night, you and any accomplices you may have, will be asked to vote for a player to eliminate from the game. Your objective is to get the number of villagers to equal the number of Mafia players.', "playable": True, "optional": False},
    {"name" : 'Villager', "description": 'Your objective is to figure out which of the other players are Mafia, and try to vote them out of the game during the daytime', "playable": True, "optional": False},
    {"name" : 'Doctor', "description": 'You are on the side of the villagers. Each night, you will be asked to choose a player who you think is in danger of being killed by the Mafia. If you choose correctly, you prevent that player from being eliminated.', "playable": True, "optional": True},
    {"name" : 'Cop', "description": 'You are on the side of the villagers. Each night, you will have the chance to investigate a player. The facilitator will tell you if that player is a Mafia or not. Your job, if you happen to find a Mafia, is to convince the other villagers to vote that person out.', "playable": True, "optional": True},
    {"name" : 'Vigilante', "description": 'You are on the side of the villagers. Once during the game, you will have the opportunity to choose another player to be killed. Choose carefully, because you might mistakenly kill a villager, but you might also take out one of the Mafia. Once your shot has been used, you become a normal villager.', "playable": True, "optional": True},
    {"name" : 'Blackmailer', "description": 'You are also a member of the Mafia. Each night, you will have the opportunity to blackmail one of the other players. This means that they are not allowed to speak for that daytime cycle. You may blackmail any player, including yourself or other Mafia members', "playable": True,  "optional": True},
]

def fill_missing_roles():
    existing_roles = list(Role.objects.all())
    roles_to_insert = [role["name"] for role in ROLE_INSERTIONS]

    for role in existing_roles:
        roles_to_insert.remove(role.name)

    for role in ROLE_INSERTIONS:
        if role['name'] in roles_to_insert:
            print(f"Adding {role['name']} to the database")
            new_role = Role(name = role['name'], description = role['description'], playable = role['playable'], optional = role['optional'])
            new_role.save()