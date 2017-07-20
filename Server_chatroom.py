from Chatroom import chatroom

class server_chatroom(chatroom):
	userList = None
	
	def __init__(self, n):
		self.userList = []
		self.messageHistory = []
		self.length = 0
		self.name = n
	
	def add_user(self, u):
		self.userList.append(u)
		return True
		
	def get_user_list(self):
		return self.userList[:]
	
	def remove_user(self, u):
		try:
			self.userList.remove(u)
			return True
		except (ValueError):
			return False


# Basic test suite for chatroom
# Tests on the base chatroom are repeated here
def main():
	c = server_chatroom("testName")
	# Ensure that an empty chat room has the correct values
	assert (c.length == 0)
	assert (c.get_history() == [])
	assert (c.userList == [])
	assert (c.get_name() == "testName")
	
	c.add_message("test1")
	c.add_message("test2")
	
	# Ensure that messages are being added correctly and length is updating
	hist = c.get_history()
	assert (hist[0] == 'test1' and hist[1] == 'test2')
	assert (c.length == 2)
	
	for i in range(99):
		c.add_message("message")
	
	# Check that the list is removing old messages once length > 100
	hist = c.get_history()
	assert (hist[0] == 'test2')
	assert (hist[99] == 'message')
	assert (c.length == 100)

	#Check adding users
	c.add_user("Bob")
	c.add_user("Charlie")
	c.add_user("Bryan")
	
	li = c.get_user_list()
	assert(len(li) == 3)
	assert(li[0] == "Bob" and li[1] == "Charlie" and li[2] == "Bryan")
	
	#Check removing users (both normal and error behaviour)
	assert (c.remove_user("Bob"))
	assert not (c.remove_user("Timothy"))
	assert (len(c.get_user_list()) == 2)

main()