class User:
    def __init__(self, user_id, name, handle):
        self.user_id = user_id
        self.name = name
        self.handle = handle
        self.friends = set()  # Using a set to avoid duplicate friendships

    def add_friend(self, friend_user):
        """Add a friend to the user's friend list."""
        if isinstance(friend_user, User):
            self.friends.add(friend_user.user_id)

    def remove_friend(self, friend_user):
        """Remove a friend from the user's friend list."""
        if isinstance(friend_user, User):
            self.friends.discard(friend_user.user_id)

    def get_friends(self):
        """Return a list of friends' user IDs."""
        return list(self.friends)