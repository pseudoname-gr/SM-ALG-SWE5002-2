import random

class Member:
    def __init__(self, member_id):
        self.id = member_id
        self.followers = set()
        self.interactions = []

class SocialNetworkGraph:
    def __init__(self):
        self.members = {}

    def add_member(self, member_id):
        if member_id not in self.members:
            self.members[member_id] = Member(member_id)

    def add_relationship(self, member_id, follower_id=None):
        if follower_id:
            self.members[member_id].followers.add(follower_id)
        else:
            self.add_member(member_id)

    def add_interaction(self, receiver_id, sender_id, likes, comments):
        self.members[receiver_id].interactions.append({'receiver_id': receiver_id, 'sender_id': sender_id, 'likes': likes, 'comments': comments})

    def calculate_influence(self, member_a_id, member_b_id):
        total_engagement_rates = self.calculate_engagement_rate(member_a_id)
        total_engagement_rate_a = total_engagement_rates.get(member_a_id, 0)
        interactions_a_to_b = self.members[member_a_id].interactions
        likes_a_to_b = sum(interaction['likes'] for interaction in interactions_a_to_b if interaction['receiver_id'] == member_b_id)
        comments_a_to_b = sum(interaction['comments'] for interaction in interactions_a_to_b if interaction['receiver_id'] == member_b_id)
        total_engagement_rate_a = max(total_engagement_rate_a, 1)  # Avoid division by zero
        influence = (likes_a_to_b + comments_a_to_b) / total_engagement_rate_a
        return influence

    def calculate_engagement_rate(self, *args):
        engagement_rates = {}
        for member_id, member in self.members.items():
            total_likes = sum(interaction['likes'] for interaction in member.interactions)
            total_comments = sum(interaction['comments'] for interaction in member.interactions)
            num_followers = len(member.followers)
            engagement_rate = ((total_likes + total_comments) / max(num_followers, 1)) * 100
            engagement_rates[member_id] = engagement_rate
            print(engagement_rates)
        return engagement_rates

    def shortest_path(self, start, end):
        visited, queue = set(), [(start, [])]

        while queue:
            member, path = queue.pop(0)
            if member == end:
                return path + [member]
            visited.add(member)
            queue.extend((neighbor_id, path + [member]) for neighbor_id in self.members[member].followers if neighbor_id not in visited)
        return None

    def highest_engagement_path(self, start, end):
        max_engagement, max_path = float('-inf'), None

        def calculate_path_engagement(path):
            return sum((interaction['likes'] + interaction['comments']) for i in range(len(path) - 1) for interaction in self.members[path[i]].interactions if interaction['sender_id'] == path[i + 1])

        for member_a_id in self.members:
            for member_b_id in self.members:
                if member_a_id != member_b_id:
                    path = self.shortest_path(member_a_id, member_b_id)
                    if path:
                        path_engagement = calculate_path_engagement(path)
                        if path_engagement > max_engagement:
                            max_engagement, max_path = path_engagement, path
        return max_path

# Driver code:
social = SocialNetworkGraph()
engagement_rates = social.calculate_engagement_rate()
members = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']

for member in members:
    social.add_relationship(member)
    for _ in range(random.randint(0, len(members) - 1)):
        follower = random.choice(members)
        if follower != member:
            social.add_relationship(member, follower)

for _ in range(5):
    receiver, sender = random.choice(members), random.choice(members)
    likes = random.uniform(0.1, 10.0)
    comments = random.uniform(0.1, 5.0)
    social.add_interaction(receiver, sender, likes, comments)


start_member, end_member = random.choice(members), random.choice(members)
while start_member == end_member:
    end_member = random.choice(members)

for member_id, rate in engagement_rates:
    print(f"Engagement rate of {member_id}: {rate:.2f}%")

shortest_path = social.shortest_path(start_member, end_member)
print("Shortest path between", start_member, "and", end_member, ":", shortest_path)

highest_engagement_path = social.highest_engagement_path(start_member, end_member)
print("Path with highest engagement between", start_member, "and", end_member, ":", highest_engagement_path)

influence = social.calculate_influence(start_member, end_member)
print(f"Influence of {start_member} on {end_member}: {influence}")
