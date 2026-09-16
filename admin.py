##Import the necessary module
import json


## This function should load the library data from a JSON file and return it as a suitable Python data structure.
def load_library(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)



## This function should save the library data to a JSON file.
## This function does not need to return anything, but it should ensure that the data is saved correctly to the specified file.
def save_library(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)




## This function should find a book by its title, author, or ID.
## If the book is found, it should return the book ID.
## If the book is not found, it should return None.
def find_book(books, search_text):
    if not isinstance(search_text, str) or not search_text.strip():
        return None

    search = search_text.strip()

    # 1. Exact ID match
    if search in books:
        return search

    # 2. Case-insensitive ID match
    for book_id in books:
        if book_id.lower() == search.lower():
            return book_id

    # 3. Case-insensitive exact title match
    search_lower = search.lower()
    for book_id, book in books.items():
        if book["title"].lower() == search_lower:
            return book_id

    # 4. Case-insensitive exact author match
    for book_id, book in books.items():
        if book["author"].lower() == search_lower:
            return book_id

    return None



## This function should display the list of books in a user-friendly format.
## It should show the book ID, title, category, and availability status (available or on loan).
## If the book is available, it should display "AVAILABLE", and if it is on loan, it should display "ON LOAN".
## The function should not return anything, but it should print the information to the console.
## The heading for this display should be "BOOK CATALOGUE".
def display_books(books):
    print("BOOK CATALOGUE")
    print("-" * 60)
    for book_id, book in books.items():
        status = "AVAILABLE" if book["available"] else "ON LOAN"
        print(f"{book_id} | {book['title']} | {book['category']} | {status}")


## This function should display the list of current loans in a user-friendly format.
## It should show the book ID, title, and the name of the borrower.
## The heading for this display should be "CURRENT LOANS".
## The function should not return anything, but it should print the information to the console.
def display_loans(loans, books):
    print("CURRENT LOANS")
    print("-" * 60)
    for loan in loans:
        book_id = loan["book_id"]
        borrower = loan["borrower"]
        title = books[book_id]["title"] if book_id in books else "Unknown"
        print(f"{book_id} | {title} | Borrower: {borrower}")


## This function should calculate and return the library statistics
## The statsitics should include the total number of books, the number of available books, and the number of borrowed books.
## The function should return these three values in the order: total, available, borrowed. Use a suitable data structure to return these values, such as a tuple or a dictionary.

def library_statistics(books):
    total = len(books)
    available = sum(1 for book in books.values() if book["available"])
    borrowed = total - available
    return (total, available, borrowed)


## This function should display the library statistics in a user-friendly format.
## It should first load the library data from a JSON file,
## Then calculate the statistics, and finally print the information to the console.
## The heading for this display should be "LIBRARY STATISTICS".
## It should print the total number of books, the number of available books, and the number of borrowed books.
## The function should not return anything, but it should print the information to the console.
def main():
    data = load_library("library.json")

    library = data["library"]
    categories = data["categories"]
    books = data["books"]
    loans = data["loans"]

    print("LIBRARY ADMINISTRATION")
    print("=" * 60)
    print(f"Library: {library['name']}")
    print(f"Branch: {library['branch']}")
    print(f"Year: {library['year']}")
    print(f"Categories: {', '.join(categories)}")
    print()

    display_books(books)
    print()
    print()

    display_loans(loans, books)
    print()

    total, available, borrowed = library_statistics(books)
    print("LIBRARY STATISTICS")
    print("-" * 60)
    print(f"Total books: {total}")
    print(f"Available: {available}")
    print(f"Borrowed: {borrowed}")


if __name__ == "__main__":
    main()
