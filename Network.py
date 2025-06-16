import networkx as nx
from User import User
import matplotlib.pyplot as plt
from uuid import uuid4
import json

class UserNetwork:

    def __init__(self):
        self.G = nx.Graph()  # Create a new graph
        self.users = {}
        self.user_count = 0
        self.labelDict = {}
        self.freqDict = {}

    def add_user(self, name, handle):
        #checks if the user is already in the network
        if handle in self.users:
            user_id = self.users[handle]
            self.freqDict[user_id] += 50
            return user_id
        
        """Add a user to the network."""
        user_id = uuid4()
        user = User(user_id, name, handle)
        self.users[handle] = user.user_id
        self.G.add_node(user_id, user=user)  # Add user as a node in the graph
        self.labelDict[user_id] = handle
        self.freqDict[user_id] = 50
        self.user_count += 1
        return user_id

    def add_friendship(self, user_id1, user_id2):
        """Create a friendship between two users."""
        if user_id1 in self.G and user_id2 in self.G:
            self.G.add_edge(user_id1, user_id2)
            # Add each other as friends in their User objects
            user1 = self.G.nodes[user_id1]['user']
            user2 = self.G.nodes[user_id2]['user']
            user1.add_friend(user2)
            user2.add_friend(user1)
        else:
            raise ValueError("Both users must exist in the network to create a friendship.")

    def remove_friendship(G, user_id1, user_id2):
        """Remove a friendship between two users."""
        if G.has_edge(user_id1, user_id2):
            G.remove_edge(user_id1, user_id2)
            # Remove each other as friends in their User objects
            user1 = G.nodes[user_id1]['user']
            user2 = G.nodes[user_id2]['user']
            user1.remove_friend(user2)
            user2.remove_friend(user1)

    def remove_user(self, user_id):
        """Remove a user from the network."""
        if user_id in self.G:
            # Remove all friendships associated with the user
            self.user_count -= 1
            self.G.remove_node(user_id)

    def display_network(self, focus_user=None):
        self.prune_network(focus_user, 150)
        node_sizes = [1000 if node==focus_user else self.freqDict[node] for node in self.G.nodes()]
        """Display the network's nodes and edges."""
        print("Users in the network:" + str(self.G.number_of_nodes()))
        print(len(self.freqDict))
        print(self.G.edges)
        self.save_network("musk.json", focus_user)
        subax1 = plt.subplot(121)
        nx.draw(self.G, node_size=node_sizes, labels=self.labelDict, with_labels=True, node_color='lightblue', font_size=10, font_color='black', ax=subax1)
        subax1.set_title("User Network")
        plt.show()

    def prune_network(self, focus_user, threshold):
        for node in list(self.G.nodes()):
            if node != focus_user and self.freqDict[node] < threshold:
                del self.freqDict[node]
                del self.labelDict[node]
                self.remove_user(node)

    def save_network(self, filename, focus_user) :
        output_json = {}
        """Save the network to a file."""
        with open (filename, 'a') as f:
            output_json[focus_user] = []
            for node in self.G.nodes():
                user = self.G.nodes[node]['user']
                user_obj = {
                    "name": user.name,
                    "handle": user.handle,
                    "strength": self.freqDict.get(node, 0)
                }
                output_json[focus_user].append(user_obj)
            json.dump(output_json, f, indent=4)