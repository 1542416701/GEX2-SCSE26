## This module contains the user interface for the library system.
# It allows users to search for books, borrow books, and return books.

## Import the necessary functions from the admin module.
# Replace "function_name1" with the actual function names you want to import.

from admin import (
    load_library,
    save_library,
    find_book,
    display_books,
)



## Search books by category.
## This function should return book IDs that match the given category.
def books_in_category(
    books,
    category
):
    if not isinstance(category, str) or not category.strip():
        return []

    category_lower = category.strip().lower()
    result = []
    for book_id, book in books.items():
        if book["category"].lower() == category_lower:
            result.append(book_id)
    return result



## Search books by full or partial title.
## This function should return book IDs that match the given title or part of the title.
def search_by_title(
    books,
    search_text
):
    if not isinstance(search_text, str) or not search_text.strip():
        return []

    text_lower = search_text.strip().lower()
    result = []
    for book_id, book in books.items():
        if text_lower in book["title"].lower():
            result.append(book_id)
    return result



## Create logic to let users borrow books.
## The function should check if the book is available or on loan, or if the borrower name is provided.
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not available, then return "NOT_AVAILABLE"
## If the book is successfully borrowed, then return "OK"
def borrow_book(
    books,
    loans,
    search_text,
    borrower
):
    book_id = find_book(books, search_text)
    if book_id is None:
        return "BOOK_NOT_FOUND"

    if not isinstance(borrower, str) or not borrower.strip():
        return "EMPTY_NAME"

    if not books[book_id]["available"]:
        return "NOT_AVAILABLE"

    books[book_id]["available"] = False
    loans.append({
        "book_id": book_id,
        "borrower": borrower.strip()
    })
    return "OK"



## Create logic to let users return books.
## The function should check if the book is on loan, or if the borrower name is provided
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not on loan, then return "NOT_ON_LOAN"
## If the book is successfully returned, then return "OK"

def return_book(
    books,
    loans,
    book_title,
    borrower
):
    book_id = find_book(books, book_title)
    if book_id is None:
        return "BOOK_NOT_FOUND"

    if not isinstance(borrower, str) or not borrower.strip():
        return "EMPTY_NAME"

    if books[book_id]["available"]:
        return "NOT_ON_LOAN"

    books[book_id]["available"] = True
    for i, loan in enumerate(loans):
        if loan["book_id"] == book_id:
            loans.pop(i)
            break
    return "OK"



## The main function that runs the user interface for the library system.
## The function must first load the library data from a JSON file, then display a menu for the user to select options.
## The options include searching for books by title or category, borrowing a book, returning a book, and exiting the program.
## When the user selects an option, the corresponding function is called to perform the action.
## The program continues to display the menu until the user chooses to exit, at which point the library data is saved back to the JSON file.
## The main function should also handle invalid selections by displaying an error message and prompting the user to select again.
def main():
    data = load_library("library.json")
    books = data["books"]
    loans = data["loans"]

    while True:
        print()
        print("LIBRARY USER SYSTEM")
        print("-" * 60)
        print("1. Search books by title")
        print("2. Search books by category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            search_text = input("Enter title or part of title: ").strip()
            results = search_by_title(books, search_text)
            if results:
                for book_id in results:
                    book = books[book_id]
                    status = "AVAILABLE" if book["available"] else "ON LOAN"
                    print(f"{book_id} | {book['title']} | {book['category']} | {status}")
            else:
                print("No books found.")

        elif choice == "2":
            category = input("Enter category: ").strip()
            results = books_in_category(books, category)
            if results:
                for book_id in results:
                    book = books[book_id]
                    status = "AVAILABLE" if book["available"] else "ON LOAN"
                    print(f"{book_id} | {book['title']} | {book['category']} | {status}")
            else:
                print("No books found in this category.")

        elif choice == "3":
            search_text = input("Enter book title, author, or ID: ").strip()
            borrower = input("Enter your name: ").strip()
            result = borrow_book(books, loans, search_text, borrower)
            if result == "OK":
                print("Book borrowed successfully.")
            elif result == "BOOK_NOT_FOUND":
                print("Book not found.")
            elif result == "EMPTY_NAME":
                print("Borrower name cannot be empty.")
            elif result == "NOT_AVAILABLE":
                print("Book is not available.")
            else:
                print(result)

        elif choice == "4":
            book_title = input("Enter book title, author, or ID: ").strip()
            borrower = input("Enter your name: ").strip()
            result = return_book(books, loans, book_title, borrower)
            if result == "OK":
                print("Book returned successfully.")
            elif result == "BOOK_NOT_FOUND":
                print("Book not found.")
            elif result == "EMPTY_NAME":
                print("Borrower name cannot be empty.")
            elif result == "NOT_ON_LOAN":
                print("Book is not on loan.")
            else:
                print(result)

        elif choice == "5":
            save_library(data, "library.json")
            print("Library data saved. Goodbye!")
            break

        else:
            print("Invalid selection, please try again.")


if __name__ == "__main__":
    main()
