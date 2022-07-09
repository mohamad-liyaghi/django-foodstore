from restaurant.models import Food

CART_SESSION_ID = 'cart'

class Cart:
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get(CART_SESSION_ID)
		if not cart:
			cart = self.session[CART_SESSION_ID] = {}
		self.cart = cart

	def __iter__(self):
		food_ids = self.cart.keys()
		foods = Food.objects.filter(id__in=food_ids)
		cart = self.cart.copy()
		for food in foods:
			cart[str(food.id)]['product'] = food

		for item in cart.values():
			item['total_price'] = int(item['price']) * item['quantity']
			yield item

	def add(self, food, quantity):
		food_id = str(food.id)
		if food_id not in self.cart:
			self.cart[food_id] = {'quantity':0, 'price':str(food.price)}
		self.cart[food_id]['quantity'] += quantity
		self.save()

	def save(self):
		self.session.modified = True