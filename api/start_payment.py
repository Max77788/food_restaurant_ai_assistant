from functions import start_payment

items = [{"name":"Lamb Shawarma Arabic Plates","quantity":2,"amount":2290,"published":False},{"name":"Hummus","quantity":1,"amount":890,"published":False}]

link = start_payment(items)

print(link)