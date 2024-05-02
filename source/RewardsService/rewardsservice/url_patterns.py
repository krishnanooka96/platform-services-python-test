from handlers.order_handler import OrderHandler
from handlers.customer_handler import CustomerHandler
from handlers.rewards_handler import RewardsHandler

url_patterns = [
    (r"/orders", OrderHandler),
    (r"/customers/([^/]+)", CustomerHandler),
    (r"/rewards", RewardsHandler),
]
