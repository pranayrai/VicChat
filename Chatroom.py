#Simple chatroom object for the client side
#Stores the most recent 100 messages in the chatroom
class chatroom:
	messageHistory = []
	length = None
	
	def __init__(self):
		self.messageHistory = []
		self.length = 0
	
	#Add a message
	#Returns True if completed successfully
	def add_message(self, m):
		#Remove the oldest message if the maximum length is reached
		if self.length >= 100:
			self.length -= 1
			self.messageHistory.pop(0)
		self.messageHistory.append(m)
		self.length += 1
		return True
	
	#Returns the chatroom contents in the form of a string list
	def get_history(self):
		return self.messageHistory[:]
	

#Basic test suite for chatroom
def main():
	c = chatroom()
	#Ensure that an empty chat room has the correct values
	assert(c.length == 0)
	assert (c.get_history() == [])
	
	c.add_message("test1")
	c.add_message("test2")
	
	#Ensure that messages are being added correctly and length is updating
	hist = c.get_history()
	assert(hist[0] == 'test1' and hist[1] == 'test2')
	assert(c.length == 2)
	
	for i in range(99):
		c.add_message("message")
	
	#Check that the list is removing old messages once length > 100
	hist = c.get_history()
	assert(hist[0] == 'test2')
	assert(hist[99] == 'message')
	assert(c.length == 100)
	
	
main()