'''Author: Anirudh Das Bezzam'''


from prettytable import PrettyTable         # importing prettytable
from Abezzam10 import file_reader                  # from my file reader importing my file reader
import os

from collections import defaultdict     



class Stores:
    '''Defines the store name and ID and uses add_products and rempove_products to add 
    and remove products from the available repsectively'''

    pt_labels = ["Store", "Product", "Customers", "Quantity sold"]              #  labels for pretty Table reference
    
    def __init__(self, store_id, store_name):
        self._store_id = store_id
        self._store_name = store_name
        
        self._items = defaultdict(int)                          # storing the items to be added in a defaultdict
        
    def add_products(self, product_id, quantities):         # add_products to add items using product id as key and quantities as value
        
        self._items[product_id] += quantities               
    
    def remove_product(self, product_id, quantities):
        self._items[product_id] -= quantities               # to calculate the remaining quantity avaialable by using productid as key again and quantity as value 

    
class Product:
    '''Uses this to define the product_id, store_id, product_name
     and a defaultdict of entity to add  entities'''

    def __init__(self,product_id,store_id,product_name):
        self._product_id = product_id
        self._store_id = store_id
        self._product_name = product_name
        self._entity = defaultdict(int)
    
    def add_entities(self,customer_id,quantity):
        self._entity[customer_id] += quantity



class Customer:
    '''Specifies the customer name, id and uses customer_cart to add items to
     it using the product as key and value as quantity'''

    pt_labels = ["Customer name", "Product", "Quantity"]

    def __init__(self,customer_name,customer_id):
        self._customer_name = customer_name
        self._customer_id = customer_id
        self._customer_cart = defaultdict(int)          # customer_cart as default dict
    
    def add_customer_cart(self,productID,quantity):     # add_customer cart uses the key as product Id and specifies the quantity to add
        self._customer_cart[productID] += quantity



class Repo:
    '''This is the main class of the program! Used to read files from
     the following given and generates prettytables'''

    def __init__(self, wdir, ptables=True):
        self._wdir = wdir
        self._stores = dict()       # storing all of the respective as dictionaries
        self._products = dict()
        self._customers = dict()


        self.read_stores(os.path.join(wdir, 'stores.txt'))
        self.read_products(os.path.join(wdir, 'products.txt'))
        self.read_customers(os.path.join(wdir, 'customers.txt'))
        self.read_inventory(os.path.join(wdir, 'inventory.txt'))          # joining the wdir with the files to read
        self.read_transactions(os.path.join(wdir, 'transactions.txt'))

        if ptables:
                print("\n Stores Summary")
                self.stores_prettytable()              # checking conditions for prettytables (if it is present)

                print("\n Customer Summary")
                self.customer_prettytable()


    def read_stores(self, path):
        try:
            for store_id, store_name in file_reader(path, 2, sep ='*', header=True): # specifies the header and seperater using my file reader
                if store_id in self._stores.keys():             # store id checker
                    print(f"Already exists {store_id}")
                else:
                    self._stores[store_id] = Stores(store_id, store_name) # generate the store id and store name using store id as key
        except ValueError as err:
            print(err)

                
    def read_products(self, path):              # reads the product file
        try:
            for product_id, store_id, product_name in file_reader(path, 3, sep ='|', header=False):
                if product_id in self._products.keys():                 # using product id as key to generate the product id, store id and product name as mentioned below
                    print(f"Already exists {product_id}")
                else:
                    self._products[product_id] = Product(product_id, store_id, product_name)
        except ValueError as err:
            print(err)

    def read_customers(self, path):             # reads the customers file
        try:
            for customer_id, customer_name in file_reader(path, 2, sep = ",", header = True):
                if customer_id in self._customers.keys():
                    print(f"ALready exists {customer_id}")
                else:
                    self._customers[customer_id] = Customer(customer_name, customer_id)
        except ValueError as err:
            print(err)   

    def read_inventory(self, path):
        '''Inventory reader keeps a track of the quantity as well as
        links the store id and product id using the keys'''
        
        try:
            for store_id, quantity, product_id in file_reader(path, 3, sep ='|', header = True):
                track = int(quantity)           # using the tracker object to specify the type of quantity as by default it takes quantity as a string
                if store_id in self._stores.keys():
                    if product_id in self._stores[store_id]._items.keys():
                        print(f"Warning: instructor cwid {product_id} is not in the instructor file")      
                    else:
                        self._stores[store_id].add_products(product_id,track)           # as the values are specified as in the store dictionary, this used the store id to add products and quantity using the product key
                
                else:
                    print(f"Warning: Store_id {store_id} is not in the stores file")
            
        except ValueError as erf:
            print(erf)

    

    def read_transactions(self,path):
        for customer_id, quantity, product_id, store_id in file_reader(path, 4, sep ='|', header = True):                
            remain = self._stores[store_id]._items[product_id]
            track = int(quantity)
            if customer_id in self._customers.keys():
                if remain >= track:
                    self._customers[customer_id].add_customer_cart(product_id, track)      # using the student cwid as key
                    self._stores[store_id].remove_product(product_id,track)
                else:
                    self._customers[customer_id].add_customer_cart(product_id,remain)
                    self._stores[store_id].remove_product(product_id,remain)
                    
            else:
                print(f"Warning: customer_id {customer_id} is not in the customers file")
                
                
                

            if product_id in self._products.keys():
                if remain > track:
                    self._products[product_id].add_entities(customer_id,track)
                else:
                    self._products[product_id].add_entities(customer_id,remain)    
            else:
                print(f"Warning: instructor cwid {customer_id} is not in the instructor file")

    def stores_prettytable(self):
        pt = PrettyTable(field_names=Stores.pt_labels)
        todo = list()
        for product in sorted(self._products.values(), key=lambda product: product._product_name):         # printing pretty table for stores 
            store = self._stores[product._store_id]._store_name
            item = product._product_name
            customer = [self._customers[key]._customer_name for key in sorted(product._entity.keys())]
            track = sum(product._entity.values())
            row = store, item, customer, track
            pt.add_row(row) 
            todo.append(row)      
        print(pt)

        return todo
    
    def customer_prettytable(self):
        pt = PrettyTable(field_names=Customer.pt_labels)
        append_doc = list()    
        for customer in sorted(self._customers.values(), key=lambda customer: customer._customer_id):
            name = customer._customer_name
            for key, value in customer._customer_cart.items():
                product = self._products[key]._product_name
                row = name,product,value
                pt.add_row(row)
                append_doc.append(row)
        print(pt)
        return append_doc

def main():
    repo = Repo('./store')        # create a main function to store the directory

        
if __name__ == "__main__":
    main()                      # call the main function
