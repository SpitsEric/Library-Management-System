# Library Management System

A web-based Library Management System built using Python's Django, HTML, CSS, and MySQL Database.
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

![Homepage Screenshot](https://github.com/user-attachments/assets/5be7b124-ca8b-46a1-8ee8-1a93cf05a357
)


### Book Search Page (/library/search/)

![Book Search Page Screenshot](https://github.com/user-attachments/assets/42899e30-e297-4539-ae79-c81194bfe552
)
![Book List Screenshot](https://github.com/user-attachments/assets/c689de69-f9c9-42c6-8414-15ced1723d83
)


### Borrower List Page (/library/borrowers/)

![Borrower Page Screenshot](https://github.com/user-attachments/assets/70a2035c-4f4f-4424-bbff-3e8c0a7a78d3
)


### Borrower Registration Page (/library/borrowers/new)

![Borrower Registration Page Screenshot](https://github.com/user-attachments/assets/51adb92a-1be2-4211-8fa2-a5413dbe3440
)


### Check In/Out Page (/library/check)

![Check In/Out Page Screenshot](https://github.com/user-attachments/assets/1b2f7a34-d7ef-430f-94af-db15993dcc8c
)
![Check In/Out Results Page Screenshot](https://github.com/user-attachments/assets/9d8bb8a0-d490-449a-a6c8-cf26ff1056f9
)


### Fines Page (/library/fines/)

![Fines Page Screenshot](https://github.com/user-attachments/assets/92da8459-4cb2-48f6-a504-267f1d831d77
)
