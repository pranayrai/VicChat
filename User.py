from Chatroom import chatroom

class User

	username = ''
	userStatus = None
	guestUser = None	
	chatrooms = []
	
	def __init__(self, username, userStatus):
		self.username = username
		self.userStatus = userStatus
		
	def get_username(self):
		return username
	
	def get_user_status(self, user):
		if user in self.chatrooms:
			return True
	
	def get_chat_rooms(self):
		return self.chatrooms[:]
		
	def add_chatroom(self,room):
        if room in self.chatrooms:
            return False
        self.chatrooms.append(room)
        return True
		
	def leave_chatroom(self,room):
        if room not in self.chatrooms:
            return False
        self.chatrooms.leave(room)
        return True
		
	
		
	
	

	