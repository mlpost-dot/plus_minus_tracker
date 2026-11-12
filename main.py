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
def home_page(state: State):
    return Page(state, [
        Header("Hockey Tracker"),
        Text("Welcome to the Hockey Tracker!"),
        Button("View Roster", view_roster),
        Button("Game Tracker", game_tracker),
        Button("Leaderboard", leaderboard)
    ])
        
@route
def view_roster(state: State):
    return Page (state, [
        Header("Player Roster"),
        Button("Home", home_page),
        Text("Here are all the players!")
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
    new_player = Player(name, jersey_number, team, 0)
    state.players.append(new_player)
    return(state)
            

@route
def game_tracker(state: State):
    return Page(state, [
        Header("Game Tracker"),
        Button("View Leaderboard", leaderboard),
        Button("Home", home_page),
        Button("Record Goal", record_goal),
        Text("Scoring Team:"),
        SelectBox("scoring_team", ["Home", "Away"])
    ])

@route
def record_goal(state: State, scoring_team: str):
    
    for player in state.players:
        if player.team == scoring_team:
            player.plus_minus += 1
        else:
            player.plus_minus -= 1

@route
def leaderboard(state: State):
    return Page(state, [
        Header("Player Leaderboard"),
        Button("home_page", home_page),
        Button("Game Tracker", game_tracker)
    ])

start_server(State(
    players=[]
    home_team="Home",
    away_team="Away",
    home_score= 0,
    away_score=0
    message="Welcome to Hockey Tracker!"
))
