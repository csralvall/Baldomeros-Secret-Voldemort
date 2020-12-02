class NotEnoughProclamations(Exception):
    """ Raised when there are only two cards available
    to take on the deck. """
    def __init__(
        self,
        proclamations,
        message="proclamations in deck are less than 3"):
        self.proclamations = proclamations
        self.message = message

    def __str__(self):
        return f'Proclamations = {self.proclamations} -> {self.message}'

class ResourceNotFound(Exception):
    """ Raised when the resource searched does not exist. """
    pass

class DeckNotFound(ResourceNotFound):
    """ Raised when there is not deck with the parameters passed. """
    pass

class BoardNotFound(ResourceNotFound):
    """ Raised when there is not board with the parameters passed. """
    pass

class MatchNotFound(ResourceNotFound):
    """ Raised when there is not match with the parameters passed. """
    pass

class PlayerNotFound(ResourceNotFound):
    """ Raised when there is not player with the parameters passed. """
    pass

class UserNotFound(ResourceNotFound):
    """ Raised when there is not User with the parameters passed. """
    pass

class VoldemortNotFound(ResourceNotFound):
    """ Raised when there is not Voldemort within the game. """
    pass

class InvalidProclamation(Exception):
    """ Raised when the proclamation passed is invalid. """
    pass

class EmptySelectedProclamations(Exception):
    """ Raised when there aren't selected proclamations to remove. """
    pass

class BadIngameStatus(Exception):
    """ Raised when the ingame status passed is invalid. """
    pass

class NoDirector(Exception):
    """ Raised when moving director to ex-director, but there is no current director. """
    pass

class BadUsername(Exception):
    """ Raised when the username is longer than the accepted in the database. """
    pass 
