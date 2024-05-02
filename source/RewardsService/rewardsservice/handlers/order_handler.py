import json
import tornado.web
from pymongo import MongoClient
from tornado.gen import coroutine

"""
Endpoint 1 Specs::

* Accept a customer's order data: email adress (ex. "customer01@gmail.com") and order total (ex. 100.80).
* Calculate and store the following customer rewards data into MongoDB. For each dollar a customer spends, the customer will earn 1 reward point. For example, an order of $100.80 earns 100 points. Once a customer has reached the top rewards tier, there are no more rewards the customer can earn.
    Email Address: the customer's email address (ex. "customer01@gmail.com")
    Reward Points: the customer's rewards points (ex. 100)
    Reward Tier: the rewards tier the customer has reached (ex. "A")
    Reward Tier Name: the name of the rewards tier (ex. "5% off purchase")
    Next Reward Tier: the next rewards tier the customer can reach (ex. "B")
    Next Reward Tier Name: the name of next rewards tier (ex. "10% off purchase")
    Next Reward Tier Progress: the percentage the customer is away from reaching the next rewards tier (ex. 0.5)
"""


class OrderHandler(tornado.web.RequestHandler):
    """
    Endpoint for accepting customer's order data and calculating rewards.

    Request Payload:
    {
        "email": "customer01@gmail.com",
        "total_amount": 100.80
    }

    Response:
    {
        "message": "Reward data stored successfully"
    }
    """

    @coroutine
    def post(self):
        """
        Accepts customer's order data and calculates rewards.

        Parameters:
            email (str): Customer's email address.
            total_amount (float): Total amount of the order.

        Returns:
            None
        """
        data = json.loads(self.request.body)
        email = data.get("email")
        total_amount = data.get("total_amount")

        # Validate email and order total
        if not email or not total_amount or total_amount <= 0:
            self.set_status(400)
            self.write("Invalid email or order total")
            return

        # Calculate reward points
        reward_points = int(total_amount)
        rewards_tier = chr(65 + (reward_points - 1) // 100)
        reward_tier_name = f"{(reward_points - 1) % 100}% off purchase"
        next_reward_tier = (
            chr(65 + reward_points // 100 + 1) if reward_points < 1000 else None
        )
        next_reward_tier_name = (
            f"{(reward_points % 100)}% off purchase" if next_reward_tier else None
        )
        next_reward_tier_progress = (
            (reward_points % 100) / 100 if next_reward_tier else None
        )

        # Connect to MongoDB
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        # Store rewards data
        db.customers.insert_one(
            {
                "email": email,
                "reward_points": reward_points,
                "reward_tier": rewards_tier,
                "reward_tier_name": reward_tier_name,
                "next_reward_tier": next_reward_tier,
                "next_reward_tier_name": next_reward_tier_name,
                "next_reward_tier_progress": next_reward_tier_progress,
            }
        )

        self.set_status(201)
        self.write({"message": "Reward data stored successfully"})
