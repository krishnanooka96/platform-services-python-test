from handlers.order_handler import OrderHandler
from handlers.rewards_handler import RewardsHandler

url_patterns = [
    (r"/orders", OrderHandler),
    (r"/rewards", RewardsHandler),
]
