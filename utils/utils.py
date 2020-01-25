from merge_test import start as s

def get_start(platform, vendor, name, number):
    return s.start(platform, vendor, name, number)


class InvalidInputException(Exception):
    def __init__(self, message):
        self.message = 'Invalid Input Exception. ' + message

    def __str__(self):
        return self.message


class GenericAPIException(Exception):
    def __init__(self, message):
        self.message = 'Generic API Exception. ' + message

    def __str__(self):
        return self.message
