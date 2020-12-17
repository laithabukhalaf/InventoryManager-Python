from flaskinventory import app

if __name__ == '__main__':
    
    app.run()


# This system is built to simulate a warehouse
#  environment and handles balancing quantities over 
#  warehouses. It has 4 main views including Overview,
#  Products,Locations and Transfers. 
#  Products and Locations let you add,edit and 
#  delete entries from the system. 
#  Transfers lets you move items into the
#   central warehouse, out of the central warehouse; 
#   also to and from various locations.
#   It also displays transfer history. 
#   Overview will display products,
#   warehouses and their respective balanced quantities.
