from Chatroom import chatroom

class user():	
	
	chatroom = ["room1", "room2"]
	
	def __init__(self, username):
		self.username = username
		self.userStatus = None
		self.guestUser = True
		self.userList = []
		
	def get_username(self):
		return self.username
	
	def get_user_status(self, user):
		if user in self.userList:
			return "Active"
		else: 
			self.guestUser = True
			return "Inactive"
	
	def get_chat_rooms(self):
		return self.chatroom[:]
		
	def add_chat_room(self,room):
            if room in self.chatroom:
                return False
            self.chatroom.append(room)
            return True
		
	def leave_chatroom(self,user):
            if user not in self.userList:
                return False
            self.userList.remove(user)
            return True
			
if __name__ == "__main__":

	print "Testing"
	u = user("BOB")
	print "Username:" + u.get_username()
	
	print ""
	print "Adding user to userList"
	u.userList.append("BOB")
	print "UserList:"
	print u.userList
	
	print ""	
	print "User Status:" + u.get_user_status("BOB")
	
	print ""
	print "Chatrooms:"
	print u.get_chat_rooms()
	print "Now adding another room:"
	u.add_chat_room("room4")	
	print u.get_chat_rooms()
	print ""
	
	
	print "Current UserList:"
	print u.userList	
	u.leave_chatroom("BOB")
	print "removing user from userList"
	print "new User List:"
	print u.userList
	
	
	
	
	
	
		
	
		
	
	

	
