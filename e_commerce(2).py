import os
from collections import defaultdict
from prettytable import PrettyTable
import unittest

def file_reader(path, num_fields, expect, sep= '\t'):
    try:
        fp = open(path, 'r', encoding = 'utf-8')
    except FileNotFoundError:
        raise FloatingPointError("can't open:", path)
    else:
        with fp:
            for n, line in enumerate(fp):
                if n == 0 and line.strip() == expect:
                    continue
                else:
                    fields = line.strip()
                    fields = fields.split(sep)
                    if len(fields) != num_fields:
                        raise ValueError('Number of fields in file should be equal to expected number of fields')
                    else:
                        yield fields

class Ecommerce:
    def __init__(self, wdir, ptables=True):
        self._wdir = wdir
        self._customers = dict()
        self._products = dict()
        self._stores = dict()

        self._get_customers(os.path.join(wdir, "customers.txt"))
        self._get_stores(os.path.join(wdir, "stores.txt"))
        self._get_inventory(os.path.join(wdir, "inventory.txt"))
        self._get_products(os.path.join(wdir, "products.txt"))
        self._get_transactions(os.path.join(wdir, "transactions.txt"))

        if ptables:

            print("\n Store Summary")
            self.store_table()

            print("\n Customer Summary")
            self.customer_table()

    def _get_customers(self, path):
        try:
            for cust_id, cust_name in file_reader(path, 2, "cust_id, name", ','):
                if cust_id in self._customers:
                    print(f"Already exists {cust_id} ")
                else:
                    self._customers[cust_id] = Customer(cust_id, cust_name)
        except ValueError as err:
            print(err)

    def _get_stores(self, path):
        try:
            for store_id, store_name in file_reader(path, 2, "id*name", "*"):
                if store_id in self._stores:
                    print(f'Already exists {store_id} ')
                else:
                    self._stores[store_id] = Store(store_id, store_name)
        except ValueError as err:
            print(err)

    def _get_inventory(self, path):
        try:
            for store_id, available_quantity, product_id in file_reader(path, 3, "store_id|quantity|product_id", "|"):
                if store_id in self._stores:
                    self._stores[store_id].add_inv(available_quantity, product_id)
                else:
                    print(f'Warning: Store does not exists {store_id} ')
        except ValueError as err:
            print(err)

    def _get_products(self, path):
        try:
            for prod_id, store_id, prod_name in file_reader(path, 3, "prod_id, store_id, prod_name", "|"):
                if prod_id in self._products:
                    print(f'Already exists {prod_id} ')
                else:
                    self._stores[store_id].add_productname(prod_id, prod_name)
        except ValueError as e:
            print(e)

    def _get_transactions(self, path):
        try:
            for cust_id, quantity, prod_id, store_id in file_reader(path, 4, "cust_id|quantity|product_id|store_id", "|"):                
                if cust_id in self._customers:
                    available_product = self._stores[store_id].available_product(prod_id)

                    self._customers[cust_id].add_quantity(self._stores[store_id]._prod_name[prod_id], 
                    quantity if int(quantity) < available_product else available_product)
                else:
                    print(f"Warning: Customer Id {cust_id} not exist")

                if store_id in self._stores:
                    self._stores[store_id].update_inv(prod_id, quantity, self._customers[cust_id]._name)
                else:
                    print(f"Warning: Store Id {store_id} not exist")
        except ValueError as err:
            print(err)

    def customer_table(self):
        pt = PrettyTable(field_names=["Customer Name", "Product", "Sold Quantity"])
        for cust in self._customers.values():
            for row in cust.pt_row():
                pt.add_row(row)

        print(pt)

    def store_table(self):
        pt = PrettyTable(field_names=["Store Name", "Product Name ", "Customer Name", "Sold Quantity"])
        for store in self._stores.values():
            for row in store.pt_row():
                pt.add_row(row)
        print(pt)

class Customer:
    def __init__(self, cust_id, cust_name):
        self._cust_id = cust_id
        self._name = cust_name
        self._sold_quantity = dict()

    def add_quantity(self, prod_id, sold_quantity):
        if prod_id in self._sold_quantity:
            value = self._sold_quantity[prod_id]
            self._sold_quantity[prod_id] = value + int(sold_quantity)
        else:
            self._sold_quantity[prod_id] = int(sold_quantity)

    def pt_row(self):
        for prod_id, quantity in self._sold_quantity.items():
            if quantity > 0:
                yield [self._name, prod_id, quantity]

class Store:
    def __init__(self, store_id, store_name):
        self._store_id = store_id
        self._store_name = store_name
        self._prod_quantity = dict()
        self._prod_name = dict()
        self._product_sold_quantity = defaultdict(lambda: defaultdict(int))

    def add_inv(self, in_qty, prod_id):
        self._prod_quantity[prod_id] = int(in_qty)

    def add_productname(self, prod_id, prod_name):
        self._prod_name[prod_id] = prod_name

    def available_product(self, prod_id):
        return self._prod_quantity[prod_id]

    def update_inv(self, product_id, sold_quantity, cust_id ):
        sold_quantity = int(sold_quantity)
        available_product = self.available_product(product_id)

        if available_product < sold_quantity:
            sold_quantity = available_product

        self._prod_quantity[product_id] -= sold_quantity
        self._product_sold_quantity[product_id][cust_id] += sold_quantity

    def pt_row(self):
        for prod_id in self._product_sold_quantity.keys():
            yield [self._store_name, self._prod_name[prod_id], sorted(self._product_sold_quantity[prod_id].keys()), 
            sum(self._product_sold_quantity[prod_id].values())]


def main():
    wdir = ""
    Ecommerce(wdir)


if __name__ == "__main__":
    main()