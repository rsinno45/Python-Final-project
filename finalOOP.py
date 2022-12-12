class Product:
    def __init__(self, productName, productRate, productCount):
        self._productName = productName
        self._productRate = productRate
        self._productCount = productCount

    def __str__(self):
        printLine = "Name: {}, Rate: ${}, Count: {}".format(self.getProductName(), self.getProductRate(),
                                                            self.getProductCount())
        return printLine

    def __repr__(self):
        return f'Product(name={self._productName}, rate={self._productRate}, count={self._productCount})'

    def __eq__(self, other):
        if ((self._productName == other._productName) and (self._productRate == other._productRate)):
            return True
        else:
            return False

    def getProductName(self):
        return self._productName

    def getProductRate(self):
        return self._productRate

    def getProductCount(self):
        return self._productCount

    def setProductCount(self, count):
        self._productCount = count

    def reduceProductCount(self, count):
        self._productCount -= count


def readProductsFile(fileName):
    productsList = []
    productFile = open(fileName, "r")
    products = productFile.read().splitlines()
    for product in products:
        productInfo = product.split(',')
        name, price, count = productInfo
        price = float(price)
        count = int(count)
        theProduct = Product(name, price, count)
        productsList.append(theProduct)
    productFile.close()
    return productsList

def printCommand():
    print("List\nCart\nAdd\nRemove\nCheckout\nExit")
    command = input("Choose Option: ")
    return command


def printProductList(productsList):
    for product in productsList:
        print(product)

def displayShoppingCart(shoppingCart):
    count = 0
    if shoppingCart:
        print("Items in the cart are")
        for item in shoppingCart:
            count += 1
            print("{}. {}".format(count, item))
    else:
        print("No Items in the cart")


def addToCart(shoppingCart, productsList):
    productName = input("Enter the name: ")
    validQuantity = False
    while (validQuantity == False):
        productQuantity = input("Enter the quantity: ")
        try:
            productQuantity = int(productQuantity)
            itemUpdated = False
            for i in range(len(productsList)):
                pname = productsList[i].getProductName()
                prate = productsList[i].getProductRate()
                pcount = productsList[i].getProductCount()
                if pname.lower() == productName.lower():
                    if productQuantity > pcount:
                        print("Quantity exceeds the count in the Inventory")
                    else:
                        for i in range(len(shoppingCart)):
                            sname = shoppingCart[i].getProductName()
                            scount = shoppingCart[i].getProductCount()
                            if sname.lower() == productName.lower():
                                itemUpdated = True
                                shoppingCart[i].setProductCount(scount + productQuantity)
                                print("Item already in cart. Quantity Updated")
                        if itemUpdated == False:
                            cartProduct = Product(pname, prate, productQuantity)
                            shoppingCart.append(cartProduct)
                            print("Item added to cart")
            validQuantity = True
        except ValueError:
            validQuantity = False
            print("Only numeric whole numbers are allowed for product quantity")
    return shoppingCart, productsList


def removeFromCart(shoppingCart):
    productPresent = False
    removeProductName = input("Enter the product name: ")
    for product in shoppingCart:
        if product.getProductName().lower() == removeProductName.lower():
            productPresent = True
            productToDelete = product
    if productPresent:
        shoppingCart.remove(productToDelete)
        print("Below product removed from cart")
        print(productToDelete)
    else:
        print("Error: Item not in cart")
    return shoppingCart


def updateInventory(shoppingCart, productsList):
    if shoppingCart:
        for shoppingItem in shoppingCart:
            for inventoryItem in productsList:
                if (shoppingItem == inventoryItem):
                    updatedQuantity = inventoryItem.getProductCount() - shoppingItem.getProductCount()
                    inventoryItem.setProductCount(updatedQuantity)
    return shoppingCart, productsList


def checkout(shoppingCart):
    taxPercentage = (7/100)
    count = 0
    totalAmount = 0
    if shoppingCart:
        print("Cart Description: ")
        print("{}. {} {} {} {}".format("", "Name", "Quantity", "Price", "Tax"))
        for item in shoppingCart:
            count += 1
            name = item.getProductName()
            quantity = item.getProductCount()
            rate = item.getProductRate()
            price = quantity * rate
            tax = price * taxPercentage
            totalAmount = price + tax
            print("{}. {} {} {:.2f} {:.2f}".format(count, name, quantity, price, tax))
        finalAmount = totalAmount
        print("The total bill for items in the cart with taxes is " + str(finalAmount))
    else:
        print("No Items in the cart to checkout")
    return shoppingCart


def updateProductsFile(fileName, productsList):
    if productsList:
        ofile = open(fileName, "w")
        for product in productsList:
            name = product.getProductName()
            rate = product.getProductRate()
            count = product.getProductCount()
            writeLine = name + "," + str(rate) + "," + str(count) + "\n"
            ofile.write(writeLine)


def main():
    shoppingCart = []
    fileName = "products.csv"
    productsList = readProductsFile(fileName)
    userCommand = printCommand()
    validCommand = False
    while (validCommand == False):
        if userCommand.lower() in ['list', 'cart', 'add', 'remove', 'checkout', 'exit']:
            if userCommand.lower() == 'list':
                printProductList(productsList)
                userCommand = ""
                userCommand = printCommand()
            elif userCommand.lower() == 'cart':
                displayShoppingCart(shoppingCart)
                userCommand = ""
                userCommand = printCommand()
            elif userCommand.lower() == 'add':
                shoppingCart, productsList = addToCart(shoppingCart, productsList)
                userCommand = ""
                userCommand = printCommand()
            elif userCommand.lower() == 'remove':
                shoppingCart = removeFromCart(shoppingCart)
                userCommand = ""
                userCommand = printCommand()
            elif userCommand.lower() == 'checkout':
                shoppingCart = checkout(shoppingCart)
                shoppingCart, productsList = updateInventory(shoppingCart, productsList)
                shoppingCart = []
                userCommand = ""
                userCommand = printCommand()
            elif userCommand.lower() == 'exit':
                validCommand = True
        else:
            validCommand = False
            print("Error. Try Again")
            userCommand = ""
            userCommand = printCommand()
    updateProductsFile(fileName, productsList)


if __name__ == '__main__':
    main()