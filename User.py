#Tests incomplete due to changes in class behaviour********

from Chatroom import chatroom

class user():	
	
	chatrooms = []
	
	def __init__(self, username, conn):
		self.username = username
		self.connection = conn
		self.permanentUser = False
		self.chatrooms = []
		
	def get_username(self):
		return self.username
	
	def get_connection(self):
		return self.connection
	
	def set_connection(self, conn):
		self.connection = conn
	
	#Returns true if permanent user, or false if guest
	def get_permanent_user(self):
		return self.permanentUser
	
	def make_permanent(self):
		self.permanentUser = True
	
	def get_chat_rooms(self):
		return self.chatrooms[:]
	
	#Appends the chatroom to the list of chatrooms.
	#Returns false if user is already in the room
	def add_chat_room(self,room):
            if room in self.chatrooms:
                return False
            self.chatrooms.append(room)
            return True
		
	def leave_chatroom(self,room):
            if room not in self.chatrooms:
                return False
            self.chatrooms.remove(room)
            return True
			
if __name__ == "__main__":

	print "Testing"	
	u = user("BOB", "conn") #Dummy testing for connection.
	print "Username:" + u.get_username()
	
	u.chatrooms.append("room1")
	print ""
	print "Chatrooms:"
	print u.get_chat_rooms()
	print "Now adding another room:"
	u.add_chat_room("room4")
	print u.get_chat_rooms()
	print ""
	
	
	
	
	
	
	
		
	
		
	
	

	
