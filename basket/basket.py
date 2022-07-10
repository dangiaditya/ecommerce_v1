from store.models import Product


class Basket():
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request) -> None:
        
        self.session = request.session
        basket = self.session.get('skey')
        
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        
        self.basket = basket

    def add(self, product, product_qty):
        """
        Adding and Updating the users basket session data
        """
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = product_qty
        else:
            self.basket[product_id] = {'price': float(product.price),
                                       'qty': int(product_qty)}

        self.save()

    def update(self, product_id, product_qty):
        print(product_id, product_qty)
        product_id = str(product_id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = product_qty
        self. save()

    def delete(self, product_id):
        
        if str(product_id) in self.basket:
            del self.basket[str(product_id)]
        self.save()

    def save(self):

        self.session.modified = True

    def __iter__(self):
        """
        Collect the product_id in the session data to query the database and return products
        """
        products_ids = self.basket.keys()
        products = Product.products.filter(id__in=products_ids)
        basket = self.basket.copy()
        
        for product in products:
            basket[str(product.id)]['product'] = product
        
        for item in basket.values():
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        """
        Get the basket data and count the quantity of items
        """
        return sum(item['qty'] for item in self.basket.values())

    def get_total_price(self):
        return sum(item['price'] * item['qty'] for item in self.basket.values())
