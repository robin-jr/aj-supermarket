# AJ Supermarket
A console application to emulate a supermarket built in python.

### Getting started
To run this project, 
```
$ python3 ./aj_supermarket.py
```
To run python unittests
```
$ python3 -m unittest
```
### Sample output
Here is a sample output of the program
```
Good morning, Rajesh
--- AJ SuperMarket is going to sky rocket its sales today! ---


Waiting for your commands...
Enter your command here:
INVENTORY=>1|GoodDay250g|20|10
Inventory updated
Enter your command here: 
INVENTORY=>2|GoodDay500g|10|20
Inventory updated
Enter your command here:
STOCK=>1
GoodDay250g - 20
Enter your command here:
STOCK=>2
GoodDay500g - 10
Enter your command here:
SALE=>1|2;2|1
== Bill ==
1 - GoodDay250g - 2 - 10 - N/A - 20
2 - GoodDay500g - 1 - 20 - N/A - 20
== Total ==
40
============
Enter your command here:
STOCK=>1
GoodDay250g - 18
Enter your command here:
STOCK=>2
GoodDay500g - 9
Enter your command here:
NEW-OFFER=>BuyXMore|1|1|2|10
Offer Added
Enter your command here: 
SALE=>1|4;2|1
== Bill ==
1 - GoodDay250g - 4 - 10 - 1 - 36.0
2 - GoodDay500g - 1 - 20 - N/A - 20
== Total ==
56.0
============
Enter your command here:
STOCK=>1
GoodDay250g - 14
Enter your command here:
STOCK=>2
GoodDay500g - 8
Enter your command here:
NEW-OFFER=>BuyXMore|1|1|2|10
Offer Added
Enter your command here:
NEW-OFFER=>BuyXMore|2|1|4|20
Offer Added
Enter your command here: 
SALE=>1|4;2|1
== Bill ==
1 - GoodDay250g - 4 - 10 - 2 - 32.0
2 - GoodDay500g - 1 - 20 - N/A - 20
== Total ==
52.0
============
Enter your command here:
STOCK=>1
GoodDay250g - 10
Enter your command here:
STOCK=>2
GoodDay500g - 7
Enter your command here:
EXIT=>

Good bye! Rajesh
```