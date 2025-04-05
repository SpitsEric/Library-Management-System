# Library Management System

A web-based Library Management System built using Django.
It provides functionalities for managing books, authors, borrowers, and book loans, including features for searching, checking out, and checking in books, as well as managing fines.


## Features

* **Book Management:**
    * Add, view, update, and delete book records (ISBN, title).
    * Associate books with authors.
* **Author Management:**
    * Add, view, update, and delete author records (name).
* **Borrower Management:**
    * Register new borrowers (name, SSN, address, phone).
    * View a list of registered borrowers.
* **Book Loan Management:**
    * Check out available books to registered borrowers.
    * Record the date out and due date for loans.
    * Check in returned books, recording the return date.
* **Search Functionality:**
    * Search for books by ISBN, title, or author.
* **Fine Management:**
    * Automatically calculate fines for overdue books.
    * Display total fines for each borrower.
    * Option to mark fines as paid.
* **User Interface:**
    * Intuitive and user-friendly web interface built with Django templates.

## Screenshots

### Homepage (/library/)

![Homepage Screenshot](![HomePage](https://github.com/user-attachments/assets/5be7b124-ca8b-46a1-8ee8-1a93cf05a357)
)
*Description of the homepage: Briefly explain what the user sees upon first accessing the application.*

### Book Search Page (/library/search/)

![Book Search Page Screenshot](![SearchPage](https://github.com/user-attachments/assets/42899e30-e297-4539-ae79-c81194bfe552)
)
![Book List Screenshot](![SearchResultsPage](https://github.com/user-attachments/assets/c689de69-f9c9-42c6-8414-15ced1723d83)
)
*Description of the book list: Show how books are displayed, including relevant information like title and author. If there's a details page for individual books, include that too.*

### Borrower List Page (/library/borrowers/)

![Borrower Page Screenshot](![BorrowerPage](https://github.com/user-attachments/assets/70a2035c-4f4f-4424-bbff-3e8c0a7a78d3)
)
*Description of the borrower registration form: Explain the fields required to register a new borrower (Name, SSN, Address, Phone).*

### Borrower Registration Page (/library/borrowers/new)

![Borrower Registration Page Screenshot](![RegisterBorrowerPage](https://github.com/user-attachments/assets/51adb92a-1be2-4211-8fa2-a5413dbe3440)
)
*Description of the borrower registration form: Explain the fields required to register a new borrower (Name, SSN, Address, Phone).*

### Check In/Out Page (/library/check)

![Check In/Out Page Screenshot](![CheckPage](https://github.com/user-attachments/assets/1b2f7a34-d7ef-430f-94af-db15993dcc8c)
)
![Check In/Out Results Page Screenshot](![CheckResultsPage](https://github.com/user-attachments/assets/9d8bb8a0-d490-449a-a6c8-cf26ff1056f9)
)
*Description of the check-out process: Explain how a user can check out a book by providing the ISBN and Borrower ID.*

### Fines Page (/library/fines/)

![Fines Page Screenshot](![FinesPage](https://github.com/user-attachments/assets/92da8459-4cb2-48f6-a504-267f1d831d77)
)
*Description of the fines page: Explain how total fines are displayed for each borrower and the option to show paid fines.*
