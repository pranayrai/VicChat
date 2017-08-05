from Chatroom import chatroom

class user():	
	
	chatrooms = []
	
	def __init__(self, username, conn):
		self.username = username
		self.connection = conn
		self.permanentUser = False
		self.chatrooms = []
		
	# Returns the name of this user
	def get_username(self):
		return self.username
	
	# Returns the socket of this user
	def get_connection(self):
		return self.connection
	
	# Sets the socket of this user
	# Used for when a permanent user goes offline (set to None) or comes back online
	def set_connection(self, conn):
		self.connection = conn
	
	# Returns true if permanent user, or false if guest
	def get_permanent_user(self):
		return self.permanentUser
	
	# Registers a user
	def make_permanent(self):
		self.permanentUser = True
	
	# Get a list of all chatrooms this user is part of
	def get_chatrooms(self):
		return self.chatrooms[:]
	
	# Appends the chatroom to the list of chatrooms.
	# Returns false if user is already in the room
	def add_chatroom(self,room):
		if room in self.chatrooms:
			return False
		self.chatrooms.append(room)
		return True
	
	# Removes the chatroom from this user's list of chatrooms
def leave_chatroom(self,room):
		if room not in self.chatrooms:
			return False
		self.chatrooms.remove(room)
		return True