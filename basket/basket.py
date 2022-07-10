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
        product_id = product.id

        if product_id not in self.basket:
            self.basket[product_id] = {'price': float(product.price),
                                       'qty': int(product_qty)}

        self.session.modified = True


    def __len__(self):
        """
        Get the basket data and count the quantity of items
        """
        return sum(item['qty'] for item in self.basket.values())
