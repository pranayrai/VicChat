from Chatroom import chatroom

# Called by client_networking, this class is a list of all joined chatrooms and
# their message history.
class client_data:

    chatrooms = []

    def __init__(self):
        self.chatrooms = []

    # Adds a new chatroom. Can have 1 or 2 parameters (not including self).
    def add_chatroom(self,*args):

        if len(args) == 1:
            for r in self.chatrooms:
                if args[0] == r.get_name():
                    return False
            self.chatrooms.append(chatroom(args[0]))
            return True
        elif len(args) == 2:
            if args[0] in self.chatrooms:
                return False
            temproom = chatroom(args[0])
            for i in args[1]:
                temproom.add_message(i)
            self.chatrooms.append(temproom)
            return True
        else:
            raise TypeError

    # Deletes a chatroom from the list, removing all history from that room.
    def remove_chatroom(self,room):
        for i in self.chatrooms:
            if i.get_name() == room:
                self.chatrooms.remove(i)
                return True
        return False

    # Returns a list of all chatrooms currently stored.
    def list_chatrooms(self):
        temp = []
        for i in self.chatrooms:
            temp.append(i.get_name())
        return temp

    # Adds a new message to a chatroom.
    def add_message(self,message,room):
        for i in self.chatrooms:
            if i.get_name() == room:
                i.add_message(message)
                return True
        return False

    # Tries to load the message history of a chatroom.
    # Returns False if the chatroom could not be found.
    def load_from_chatroom(self,room):
        for i in self.chatrooms:
            if i.get_name() == room:
                return i.get_history()
        return False


if __name__ == "__main__":
    # A set of simple tests, outputting the results from each.

    print ""
    cd = client_data()

    print "Listing chatrooms:"
    print cd.list_chatrooms()
    print ""

    print "Adding message to room that's not in the list:"
    print cd.add_message("testing...?","general")
    print ""

    print "Adding new chatroom called 'general'"
    print cd.add_chatroom("general")
    print ""

    print "Adding new chatroom called 'random'"
    print cd.add_chatroom("random")
    print ""

    print "Adding 'hello' as a message to general"
    print cd.add_message("hello","general")
    print ""

    print "Adding 'test123' as a message to general"
    print cd.add_message("test123","general")
    print ""

    print "Listing chatrooms"
    print cd.list_chatrooms()
    print ""

    print "Printing general history"
    print cd.load_from_chatroom("general")
    print ""

    print "Removing general"
    print cd.remove_chatroom("general")
    print ""

    print "Listing chatrooms"
    print cd.list_chatrooms()
    print ""
