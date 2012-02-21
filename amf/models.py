from django.db import models
from django.contrib.auth.models import User
import datetime
import logging


#internal imports
import server.logconfig
logger=logging.getLogger(name="amf_server")

# Create your models here.


class GameStatus(models.Model):
    """
    Status of the game.
    Possible values:
    0 - wait for players' confirmation
    1 - start of the game
    2 - pause of the first player
    3 - pause of the second player
    4 - turn of the first player
    5 - turn of the second player
    """

    AVALIABLE_GAME_STATUSES = (
        (0,"Wait for players's confirmation"),
        (1,"Start of the game"),
        (2,"Pause of the first player"),
        (3,"Pause of the second player"),
        (4,"Turn of the first player"),
        (5,"Turn of the second player"),
        )
    code = models.SmallIntegerField(choices=AVALIABLE_GAME_STATUSES) # status code
    changed = models.TimeField("time changed") # when status was changed last time

    def change_status(self,status_code):
        """
        Change status of the Game
        @type status_code: number
        @param status_code: status_code from Available Game statuses
        """
        if (status_code in self.AVALIABLE_STATUSES):
            self.code=status_code
            self.changed=datetime.now()
        else:
            logger.error("Wrong status received in GameStatus.change_status() wrong status_code: " + status_code)

class Status( models.Model):
    """
    Current User Status.
    Available options for status:
    0 - In menu
    1 - Wait for rival
    2 - In game

    """

    AVALIABLE_STATUSES = (
        (0,"In menu"),
        (1,"Wait for rival"),
        (2,"In game")
    )
    code = models.SmallIntegerField(choices=AVALIABLE_STATUSES) # status code
    changed = models.TimeField("time changed") # when status was changed last time

    def change_status(self,status_code):
        """
        Change status of the User
        @type status_code: number
        @param status_code: status_code from Available statuses
        """
        if (status_code in self.AVALIABLE_STATUSES):
            self.code=status_code
            self.changed=datetime.now()
        else:
            logger.error("Wrong status received in Status.change_status() wrong status_code: " + status_code)

class Cult(models.Model):
    """
     Cult information. Every player, except paid ones, has a cult to worship to  Yes, just name and description.
    """
    name = models.CharField(max_length=16) # name of the Cult
    desc = models.TextField() #description of the Cult

class Player(models.Model):
    """
    Player parameters
    Build similar to django profile
    """
    user = models.OneToOneField(User) # linked to django user profile
    name = self.user.user_name # player nickname
    avatar = models.URLField() # url to the players avatar picture
    experience = models.IntegerField() # player experience
    coins_golden = models.IntegerField() # players golden coins
    coins_silver = models.IntegerField() # players silver coins
    games_overall = models.IntegerField()# overall number of games
    games_won = models.IntegerField()#number of win games
    games_lost = models.IntegerField() #numver of lost games
    games_draw = games_overall-games_lost-games_won # number of draw games
    status = models.ForeignKey(Status)
    #player_deck is linked to it using ForeightKey
    #games are linked to it using ForeightKey
    #game_decksare linked to it using ForeightKey


class PlayerInfo(models.Model):
    """
    Temporary class for sending user info to the client
    """
    name = models.CharField(max_length=64) # player nickname
    avatar = models.URLField() # url to the players avatar picture
    experience = models.IntegerField() # player experience
    games_overall = models.IntegerField()# overall number of games
    games_won = models.IntegerField()#number of win games
    games_lost = models.IntegerField() #numver of lost games
    games_draw = games_overall-games_lost-games_won # number of draw games

    def __init__(self,Player):
        self.name=Player.name
        self.avatar=Player.avatar
        self.experience=Player.experience
        self.games_overall=Player.games_overall
        self.games_won=Player.games_won
        self.games_lost=Player.games_lost



class Card(models.Model):
    """
    Basic card.
    """
    name=models.TextField() #  name of the card
    avatar = models.URLField() # url path to the image of the card
    desc = models.TextField() # description of the card
    cost_in_gold = models.IntegerField() # cost in golden coins
    cost_in_silver = models.IntegerField() # cost in silver coins.  Value -1 means that it can be bought for gold.
    generation = models.SmallIntegerField # generation of the card
    hitpoints_base= models.SmallIntegerField #  basic hitpoints of the card
    damage_base = models.SmallIntegerField() # basic damage caused by the card
    feature = models.TextField() # description of the card's feature
    hitpoints_increase = models.SmallIntegerField() # increase of card's hitpoints per level
    damage_increase = models.SmallIntegerField() # increase of card's damage per level
    feature_super = models.TextField() # decription of the card's feature at the highest level
    
    def paid_players_only(self):
        """
        Returns Boolean: True if card can be bought only for gold
        @rtype:   boolean
        @return:  True for paid players, False in other cases
        """
        return self.cost_in_silver <0


class PlayerDeck():
    """
    Player's deck, i.e set of the Player's cards.
    It is empty class just to connect player and his/her set of cards
    """
    player = models.ForeignKey(Player) #linked to player


class PlayerCard(models.Model):
    """
     Player's card. Is a successor from one of the Basic cards, but adding some experience and level factors
    """
    card = models.ForeignKey(Card) # ancestor card for player's one READ-ONLY
    deck = models.ForeignKey(PlayerDeck) # linked to player's deck
    experience = models.SmallIntegerField() # player's card experience
    level = models.SmallIntegerField() # player's card level
    hitpoints = int(card.hitpoints_base+card.hitpoints_increase*level) # current card hitpoints
    damage = int(card.damage_base+card.damage_increase*level)# current cart damage
    #stumbs
    name=card.name
    desc=card.desc
    avatar=card.avatar
    cost_in_gold=card.cost_in_gold
    cost_in_silver=card.cost_in_silver
    generation=card.generation
    feature=card.feature
    feature_super=card.feature_super


class Game(models.Model):
    """
    Current game
    """
    player_first = models.ForeignKey(Player) # first player in the game
    player_second = models.ForeignKey(Player) # second player in the game
    status = models.ForeignKey(GameStatus) # game status
    player_first_approval=models.BooleanField() #approval of the first player
    player_second_approval=models.BooleanField() # approval of the second player
    log_game_status=models.TextField() # log of changes in game statuses
    log_game_turns=models.TextField() # log of game turns



