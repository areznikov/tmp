from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime
import logging


#internal imports
import server.settings_server as settings_server
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

    def __unicode__(self):
        return self.code

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
    code = models.SmallIntegerField(choices=AVALIABLE_STATUSES,default=AVALIABLE_STATUSES[0][0]) # status code
    changed = models.TimeField("time changed",default=0) # when status was changed last time
    #Player is linked via Foreign  key
    def __unicode__(self):
        return self.code

    def __init__(self):
        self.changed=datetime.now()

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

    #def create_user_status(sender, instance, created, **kwargs):
    #    if created:
    #        Status.objects.create(user=instance)
    #post_save.connect(create_user_status, sender=Player)


class Cult(models.Model):
    """
     Cult information. Every player, except paid ones, has a cult to worship to  Yes, just name and description.
    """
    name = models.CharField(max_length=16) # name of the Cult
    desc = models.TextField() #description of the Cult

    def __unicode__(self):
        return self.name

class Player(models.Model):
    """
    Player parameters
    Build similar to django profile
    """
    user = models.OneToOneField(User) # linked to django user profile
    #name = user.username # player nickname
    avatar = models.URLField(default=settings_server.Player_avatar_default) # url to the players avatar picture
    experience = models.IntegerField(default=settings_server.Player_experience_start) # player experience
    coins_golden = models.IntegerField(default=settings_server.Player_coins_golden_start) # players golden coins
    coins_silver = models.IntegerField(default=settings_server.Player_coins_silver_start) # players silver coins
    games_overall = models.IntegerField(default=0)# overall number of games
    games_won = models.IntegerField(default=0)#number of win games
    games_lost = models.IntegerField(default=0) #numver of lost games
    status = models.SmallIntegerField(choices=settings_server.Player_Statuses,default=settings_server.Player_Statuses[0][0])
    status_changed = models.DateTimeField(auto_now=True)
    #status = models.OneToOneField(Status,default=Status.AVALIABLE_STATUSES[0][0])
    #player_deck is linked to it using ForeightKey
    #games are linked to it using ForeightKey
    #game_decksare linked to it using ForeightKey


    def __unicode__(self):
        return self.user.username

    def _calc_draws(self):
        return self.games_overall-self.games_won-self.games_lost
    games_draw = property(_calc_draws)

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

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Player.objects.create(user=instance)
    post_save.connect(create_user_profile, sender=User)

#created to be able to access Player directly from django user
User.profile = property(lambda u: Player.objects.get_or_create(user=u)[0])



class PlayerInfo():
    """
    Temporary class for sending user info to the client
    """
    name = "" # player nickname
    avatar = "" # url to the players avatar picture
    experience = 0 # player experience
    games_overall = 0 # overall number of games
    games_won = 0 #number of win games
    games_lost = 0 #numver of lost games

    def __init__(self,Player):
        self.name=Player.user.username
        self.avatar=Player.avatar
        self.experience=Player.experience
        self.games_overall=Player.games_overall
        self.games_won=Player.games_won
        self.games_lost=Player.games_lost

    def __unicode__(self):
        return self.name

    def _calc_draws(self):
         return self.games_overall-self.games_won-self.games_lost
    games_draw = property(_calc_draws)


class Card(models.Model):
    """
    Basic card.
    """
    name=models.TextField() #  name of the card
    avatar = models.URLField() # url path to the image of the card
    desc = models.TextField() # description of the card
    cost_in_gold = models.IntegerField() # cost in golden coins
    cost_in_silver = models.IntegerField() # cost in silver coins.  Value -1 means that it can be bought for gold.
    generation = models.SmallIntegerField() # generation of the card
    hitpoints_base= models.SmallIntegerField() #  basic hitpoints of the card
    damage_base = models.SmallIntegerField() # basic damage caused by the card
    feature = models.TextField() # description of the card's feature
    hitpoints_increase = models.SmallIntegerField() # increase of card's hitpoints per level
    damage_increase = models.SmallIntegerField() # increase of card's damage per level
    feature_super = models.TextField() # decription of the card's feature at the highest level

    def __unicode__(self):
        return self.name

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
    name = models.CharField(max_length=64)# name of the deck
    player = models.ForeignKey(Player)#linked to player

    def __unicode__(self):
        return self.name



class PlayerCard(models.Model):
    """
     Player's card. Is a successor from one of the Basic cards, but adding some experience and level factors
    """
    card = models.ForeignKey(Card) # ancestor card for player's one READ-ONLY
    #deck = models.ForeignKey(PlayerDeck) # linked to player's deck
    experience = models.SmallIntegerField() # player's card experience
    level = models.SmallIntegerField() # player's card level

    def __unicode__(self):
        return self.name+"_"+self.generation
    #stumbs


    def _get_name(self):
        return self.card.name
    def _get_desc(self):
        return self.card.desc
    def _get_avatar(self):
        return self.card.avatar
    def _get_cost_in_gold(self):
        return self.card.cost_in_gold
    def _get_cost_in_silver(self):
        return self.card.cost_in_silver
    def _get_generation(self):
        return self.card.generation
    def _get_feature(self):
        return self.card.feature
    def _get_feature_super(self):
        return self.card.feature_super

    def _calc_hitpoints(self):
        return self.card.hitpoints_base+self.card.hitpoints_increase*self.level
    def _calc_damage(self):
        return self.card.damage_base+self.card.damage_increase*self.level

    name=property(_get_name)
    desc=property(_get_desc)
    avatar=property(_get_avatar)
    cost_in_gold=property(_get_cost_in_gold)
    cost_in_silver=property(_get_cost_in_silver)
    generation=property(_get_generation)
    feature=property(_get_feature)
    feature_super=property(_get_feature_super)
    hitpoints = property(_calc_hitpoints) # current card hitpoints
    damage = property(_calc_damage)# current cart damage

class Game(models.Model):
    """
    Current game
    """
    player_first = models.ForeignKey(Player,related_name='player_first') # first player in the game
    player_second = models.ForeignKey(Player,related_name='player_second') # second player in the game
    status = models.ForeignKey(GameStatus) # game status
    player_first_approval=models.BooleanField() #approval of the first player
    player_second_approval=models.BooleanField() # approval of the second player
    log_game_status=models.TextField() # log of changes in game statuses
    log_game_turns=models.TextField() # log of game turns

    def __unicode__(self):
        return self.status.code+"_"+self.player_first+" "+self.player_second



