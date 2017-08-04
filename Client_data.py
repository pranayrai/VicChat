from Chatroom import chatroom


class client_data:

    chatrooms = []
    
    def __init__(self):
        self.chatrooms = []

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

    def remove_chatroom(self,room):
        for i in self.chatrooms:
            if i.get_name() == room:
                self.chatrooms.remove(i)
                return True
        return False

    def list_chatrooms(self):
        temp = []
        for i in self.chatrooms:
            temp.append(i.get_name())
        return temp

    def add_message(self,message,room):
        for i in self.chatrooms:
            if i.get_name() == room:
                i.add_message(message)
                return True
        return False

    def load_from_chatroom(self,room):
        for i in self.chatrooms:
            if i.get_name() == room:
                return i.get_history()
        return False






    '''def add_chatroom(*args):
        if len(args) == 1:
            if room in self.chatrooms:
                return False
            self.chatrooms[room] = chatroom()
        elif len(args) == 2:
            if room in self.chatrooms:
                return False
            self.chatrooms[room] = chatroom()
            for i in history:
                chatrooms[room].add_message(i)




    def remove_chatroom(self,room):
        if room not in self.chatrooms:
            return False
        del self.chatrooms[room]
        return True

    def list_chatrooms(self):
        return list(self.chatrooms.keys())

    def add_message(self,message,room):
        if room not in self.chatrooms:
            return False
        #i = self.chatrooms.index(room)
        self.chatrooms[name].add_message(message)
        return True

    def load_from_chatroom(self,room):
        if room not in self.chatrooms:
            return False
        #i = self.chatrooms.index(room)
        return self.chatrooms[room].get_history()'''












if __name__ == "__main__":
    print ""
    cd = client_database()

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
