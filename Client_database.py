from Chatroom import chatroom


class client_database:

    chatrooms = []

    def add_chatroom(room):
        if room in self.chatrooms:
            return False
        self.chatrooms.append(room)
        return True

    def remove_chatroom(room):
        if room not in self.chatrooms:
            return False
        return True

    def list_chatrooms():
        return self.chatrooms[:]

    def add_message(message,room):
        if room not in self.chatrooms:
            return False
        i = self.chatrooms.index(room)
        self.chatrooms[i].add_message(message)

    def load_from_chatroom(room):
        if room not in self.chatrooms:
            return False
        i = self.chatrooms.index(room)
        return self.chatrooms[i].get_history()

if __name__ == "__main__":
    # tests
