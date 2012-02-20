__author__ = 'artur.reznikov'


def hitpoints(self):
    """
    Returns player's card current hitpoint based on card level and ancestor card characteristics
    @rtype:   integer
    @return:  returns hitppoint_base+hitpoints_increase*level
    """
    return self.card.hitpoints_base+self.card.hitpoints_increase*self.level

def damage(self):
    """
    Returns player's card current damage based on card level and ancestor card characteristics
    @rtype:   integer
    @return:  returns damage_base+damage_increase*level
    """
    return self.card.damage_base+self.card.damage_increase*self.level

    #stumbs
def name(self):
    return self.card.name
def desc(self):
    return self.card.desc
def avatar(self):
    return self.card.avatar
def cost_in_gold(self):
    return self.card.cost_in_gold
def cost_in_silver(self):
    return self.card.cost_in_silver
def generation(self):
    return self.card.generation
def feature(self):
    return self.card.feature
def feature_super(self):
    return self.card.feature_super