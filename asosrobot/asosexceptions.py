class AsosRobotException(Exception): pass



class BagNotWorkingException(AsosRobotException): pass
class LoginFailedException(AsosRobotException): pass
class URLNotValidException(AsosRobotException): pass
class OutOfStockException(AsosRobotException): pass
class NoColorException(AsosRobotException): pass
class NoSizeException(AsosRobotException): pass
class SizeNotAvailableException(AsosRobotException): pass

