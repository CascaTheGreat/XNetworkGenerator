import networkx as nx
from User import User
import matplotlib.pyplot as plt
import json
from datetime import datetime

class UserNetwork:

    def __init__(self):
        self.G = nx.Graph()  # Create a new graph
        self.users = {}
        self.user_count = 0
        self.labelDict = {}
        self.freqDict = {}

    def add_user(self, name, handle):
        #checks if the user is already in the network
        if handle.lower() in self.users:
            user_id = self.users[handle]
            self.freqDict[user_id] += 50
            return user_id
        
        """Add a user to the network."""
        user_id = handle.lower()  # Using handle as user_id for simplicity
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
        self.prune_network(focus_user, 100)
        node_sizes = [1000 if node==focus_user else self.freqDict[node] for node in self.G.nodes()]
        """Display the network's nodes and edges."""
        print("Users in the network:" + str(self.G.number_of_nodes()))
        print(len(self.freqDict))
        print(self.G.edges)
        self.save_network("data.json")
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

    def save_network(self, filename) :
        """Save the network to a file."""
        with open (filename, 'r+') as f:
            output_json = json.load(f)
            for node in self.G.nodes():
                user = self.G.nodes[node]['user']
                user_obj = {
                    "id": user.handle,
                    "label": user.handle,
                    "real_name": user.name,
                }
                output_json["nodes"].append(user_obj)
                f.seek(0)
            for edge in self.G.edges():
                edge_obj = {
                    "source": edge[0],
                    "target": edge[1],
                    "id": str(edge[0]) + "_" + str(edge[1]),
                    "label": "interaction",
                    "created": str(datetime.now())
                }
                output_json["edges"].append(edge_obj)
            json.dump(output_json, f, indent=4)