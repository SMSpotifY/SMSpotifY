class ProgramError(Exception):
	# Base class for other exceptions
	pass

class UserNotFoundException(ProgramError):
	# Raised when a user is not found with a given phone number
	pass

class MoreThanOneUserFoundException(ProgramError):
	# Raised when more than one user is found in a given query
	pass

class InsufficientPermsException(ProgramError):
	# Raised when a user doesn't have sufficient permissions for their request
	pass

class UnrecognizedServiceException(ProgramError):
	# Raised when the operator class receives a malformed request
	pass

class UnrecognizedRequestException(ProgramError):
	# Raised when the request type is unknown
	pass

class NoActiveDevices(ProgramError):
	# Raised when no active devies are found
	pass