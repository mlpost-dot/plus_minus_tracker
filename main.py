from bakery import assert_equal
from dataclasses import dataclass
from drafter import *

@dataclass
class Player:
    name: str
    jersey_number: int
    team: str
    plus_minus: int

@dataclass
class State:
    players: list[Player]
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    message: str
    

@route
def index(state: State):
    return Page(state, [
        Header("Hockey Tracker"),
        Text("Welcome to the Hockey Tracker!"),
        Button("View Roster", view_roster),
        Button("Game Tracker", game_tracker),
        Button("Add Player", add_player_page),
        Button("Leaderboard", leaderboard)
    ])
        
@route
def view_roster(state:State):
    roster_display = []

    for player in state.players:
        roster_display.append(
            Text(
                player.name + " - Jersey #" +
                str(player.jersey_number) + " - " +
                player.team
            ))

    return Page(state, [
        Header("Player Roster"),
        Button("Home", index),
        Button("Add Player", add_player_page),
        Text("Here are all the players!"),
        *roster_display,
        Text(state.message)
    ])

@route
def add_player_page(state: State):
    return Page(state, [
        Header("Add Player"),
        Text("Player name:"),
        TextBox("name"),
        Text("Jersey Number:"),
        TextBox("jersey_number"),
        Text("Team"),
        SelectBox("team", ["Home", "Away"]),
        Button("Save Player", add_player),
        Button("Back to Roster", view_roster)
    ])

@route
def add_player(state: State, name: str, jersey_number: int, team: str):
    team_count = 0

    for player in state.players:
        if player.team == team:
            team_count += 1

            if player.jersey_number == jersey_number:
                state.message = "That jersey number is already taken by this team!"
                return view_roster(state)

    if team_count >= 21:
        state.message = "This team already has 21 players!"
        return view_roster(state)

    new_player = Player(name, jersey_number, team, 0)
    state.players.append(new_player)

    state.message = "Player added successfully!"

    return view_roster(state)
            

@route
def game_tracker(state: State):
    home_players = []
    away_players = []

    for player in state.players:
        if player.team == "Home":
            home_players.append(
                (player.name + " #" + str(player.jersey_number),
                 player.name)
            )
        elif player.team == "Away":
            away_players.append(
                (player.name + " #" + str(player.jersey_number),
                 player.name)
            )

    return Page(state, [
        Header("Game Tracker"),
        Button("Home", index),

        Header("Score"),
        Text(state.home_team + ": " + str(state.home_score)),
        Text(state.away_team + ": " + str(state.away_score)),

        Text("Scoring Team:"),
        SelectBox("scoring_team", ["Home", "Away"]),

        Header("Home Players on Ice"),
        *[CheckBox(name, name) for name, name in home_players],

        Header("Away Players on Ice"),
        *[CheckBox(name, name) for name, name in away_players],

        Button("Record Goal", record_goal),
        Button("View Leaderboard", leaderboard)
    ])


@route
def record_goal(state: State, scoring_team: str,
                **selected_players):

    if scoring_team == state.home_team:
        state.home_score += 1
    elif scoring_team == state.away_team:
        state.away_score += 1

    for player in state.players:
        if player.name in selected_players:
            if player.team == scoring_team:
                player.plus_minus += 1
            else:
                player.plus_minus -= 1

    return game_tracker(state)

@route
def leaderboard(state: State, scoring_team: str = "",
                **kwargs):
    return Page(state, [
        Header("Player Leaderboard"),
        Button("Home", index),
        Button("Game Tracker", game_tracker)
    ])


start_server(State(
    players=[],
    home_team="Home",
    away_team="Away",
    home_score= 0,
    away_score=0,
    message="Welcome to Hockey Tracker!"
))
