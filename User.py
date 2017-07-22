from Chatroom import chatroom

class user():	
	
	
	def __init__(self, username):
		self.username = username
		self.userStatus = None
		self.guestUser = None
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
		
	def add_user(self,user):
            if user in self.userList:
                return False
            self.userList.append(user)
            return True
		
	def leave_chatroom(self,user):
            if user not in self.userList:
                return False
            self.userList.remove(user)
            return True
			
if __name__ == "__main__":
	print ""
	u = user("BOB")
	
	
	u.userList.append("BOB")
	print u.userList
	
	print u.get_username()
	
	print "User Status:" + u.get_user_status("BOB")
	
	
	
	
		
	
		
	
	

	
