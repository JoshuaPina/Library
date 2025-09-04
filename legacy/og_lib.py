books_to_buy = {
    "Real-World Python" : "Lee Vaughan",
    "48 Laws Of Power" : "Robert Green",
    "Dead Simple Python": "Jason McDonald",
    "Python Crash Course" : "Eric Matthes",
    "Python for Data Science for Dummies" : "John Paul Mueller"  
}
print("Today our library has the following books: ")

for x in books_to_buy:
    print(repr(x), ":", books_to_buy[x])
    
print()
class Library:
    def __init__(book, n_v=1, n_g=1, n_mc=1, n_ma=1, n_mu=1):
        book.n_vaughan = n_v
        book.n_green = n_g
        book.n_mcdonald = n_mc
        book.n_matthes = n_ma
        book.n_mueller = n_mu
        

    def inventory(book):
        print("This library has: ")
        print(f"Real-World Python:  {book.n_vaughan} copies")
        print(f"48 Laws Of Power: {book.n_green} copies")
        print(f"Dead Simple Python: {book.n_mcdonald} copies")
        print(f"Python Crash Course: {book.n_matthes} copies")
        print(f"Python for Data Science for Dummies: {book.n_mueller} copies")

    def rent(book, name_of_book):
            if name_of_book == "1":
                if book.n_vaughan == 0:
                    return -1
                book.n_vaughan -= 1
            if name_of_book == "2":
                if book.n_green == 0:
                    return -1
                book.n_green -= 1
            if name_of_book== "3":
                if book.n_mcdonald == 0:
                    return -1
                book.n_mcdonald -= 1
            if name_of_book== "4":
                if book.n_matthes == 0:
                    return -1
                book.n_matthes -= 1
            if name_of_book== "5":
                if book.n_mueller == 0:
                    return -1
                book.n_mueller -= 1
            return 0
    def restock(book, name_of_book, quantity):
            if name_of_book == "1":
                book.n_vaughan += quantity
            if name_of_book == "2":
                book.n_green += quantity
            if name_of_book == "3":
                book.n_mcdonald += quantity
            if name_of_book == "4":
                book.n_matthes += quantity
            if name_of_book == "5":
                book.n_mueller += quantity


def main():
    my_library = Library(5, 8, 10, 10, 6)
    quit_words = ["q" , "quit"]
    rent_words = ["b" , "borrowing"]
    restock_words = ["r", "restock"]
    inventory_words = ["i", "p"]
    while True:
        print("Please select an option: b for borrowing, r for restocking, i for inventory or print, q for quit")
        user_choice = input("Hurry up and decide: ")
        if user_choice in quit_words:
            break
        if user_choice in rent_words:
            print("Please select an option:\n 1 - Real-World Python \n 2 - 48 Laws of Power \n 3 - Dead Simple Python \n 4 - Python Crash Course\
                   \n 5 - Python for Data Science for Dummies")
            name_of_book = input("What would you like to borrow? Enter the number: ")
            if my_library.rent(name_of_book) == 0:
                print("Get to reading!")
            else:
                print("Why would you do this to me? I don't have that book in stock right now. Please try again later.")
            
        if user_choice in inventory_words:
            my_library.inventory()
        if user_choice in restock_words:
            print("Please select an option:\n 1 - Real-World Python \n 2 - 48 Laws of Power \n 3 - Dead Simple Python \n 4 - Python Crash Course\
                   \n 5 - Python for Data Science for Dummies")
            name_of_book = input("Enter it here: ")
            print("Input the number of books you finally decided to bring back: ")
            quantity = int(input("Enter it here: "))
            my_library.restock(name_of_book, quantity)


if __name__ == "__main__":
    main()