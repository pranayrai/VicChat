from Chatroom import chatroom


class client_database:

    chatrooms = []

    def add_chatroom(self,room):
        if room in self.chatrooms:
            return False
        self.chatrooms.append(room)
        return True

    def remove_chatroom(self,room):
        if room not in self.chatrooms:
            return False
        self.chatrooms.remove(room)
        return True

    def list_chatrooms(self):
        return self.chatrooms[:]

    def add_message(self,message,room):
        if room not in self.chatrooms:
            return False
        i = self.chatrooms.index(room)
        self.chatrooms[i].add_message(message)
        return True

    def load_from_chatroom(self,room):
        if room not in self.chatrooms:
            return False
        i = self.chatrooms.index(room)
        return self.chatrooms[i].get_history()

if __name__ == "__main__":
    print ""
    cd = client_database()

    print "Listing chatrooms:"
    print cd.list_chatrooms()
    print ""

    print "Adding message to room that's not in the list:"
    room = chatroom("general")
    print cd.add_message("testing...?",room)
    print ""

    print "Adding new chatroom called 'general'"
    print cd.add_chatroom(room)
    print ""

    print "Adding 'hello' as a message to general"
    print cd.add_message("hello",room)
    print ""

    print "Listing chatrooms"
    print cd.list_chatrooms()
    print ""

    print "Printing history"
    print cd.load_from_chatroom(room)
    print ""

    print "Removing general"
    print cd.remove_chatroom(room)
    print ""

    print "Listing chatrooms"
    print cd.list_chatrooms()
    print ""
