**Name:** Navya Bajwa
**Student Number:** 20417217

| Function Name                 | Implementation Status | What is Missing                          |
|-------------------------------|-----------------------|------------------------------------------|
| add_book_to_catalog()         |       Complete        |       N/A                                |
                                                                                             
| borrow_book_by_patron()       |       Complete        |       N/A                                |
                                                                                               
| return_book_by_patron()       |        Partial        | Accept patron id and ISBN to check if    |
                                |      (incomplete)     | the book was actually withdrawn.         |
                                |                       | Implement the update_book_availability() |
                                |                       | function in this function. Log return    |
                                |                       | date. Calculate/deisplay any late fees.  |
                                                                                                 
| calculate_late_fee_for_book() |        Partial        | Implement the api to calculate the late  |
                                |      (incomplete)     | fee.                                     |

| search_books_in_catalog()     |        Partial        | Accept a search term and search type. If |
                                |      (incomplete)     | a title, must be < than 200 chars. If an |
                                |                       | author, must be < than 200 chars. If an  |
                                |                       | ISBN, must be exactly 13 digits --> Use  |
                                |                       | the get_book_by_isbn() function. Return  |
                                |                       | the search results in same format as     |
                                |                       | catalog.                                 |

| get_patron_status_report()    |        Partial        | Accepting a patron id and checking if it |
                                |      (incomplete)     | is valid. Displaying number of           |
                                |                       | currently borrowed books with due dates  |
                                |                       | dates, total fees owed, borrow history.  |

| init_database()               |       Complete        |       N/A                                |

| add_sample_data()             |       Complete        |       N/A                                |



## Unit Testing Summary

## Tests for add_book_to_catalog()
The postive test cases include one for when the inputs are all valid (len of title and auther name is within range, isbn is 13 digits, total copies is a postive integer).
I also have cases that test positive when the length of the title is exactly 200 characters long and the length of the author's name is
exactly 100 characters long. 
The negative test cases test when the input lengths go beyond their accepted ranges, the ISBN in not completely numeric, and some arguments are not provided.

## Tests for borrow_book_by_patron()
The postive cases for this include one for when the patron id exists and is not at the limtit, and when the book id exists. The negative test cases test for when the patron id doesn't exist, the patron has withdrawn the max they are allowed to, the book id is invalid or doesn't exist. I know that the patron doesn't enter the book id themselves, but I'm still testing it in case there is a bug that changes the book id somehow. 

## Tests for return_book_by_patron()
Postive case: When the patron id is valid, and the patron has borrowed to book they want to return (book id is valid)
Negative Cases: When the patron hasn't withdrawn the book they want to return, when the patron does not exist, attempting to return a book that does not exist, attempting to return a book and not enteringg the patron or book id. 

## Tests for calculate_late_fee_for_book()
I have a test for no days overdue. I also have test for when the fee is $0.50 per day (1 day and 7 days overdue). I also have tests that test the increase in the fee after a week (9 days is tested). Finally, I have a test for that max fee being $15.

## Tests for search_books_in_catalog()
I have tests for when the title, author, and isbn searches have books in the catalog. I also test when the user enters a title, author, or isbn that does not exist in the catalog. I also included tests that will result in no books being displayed when the user enters whitespace because that's not a productive search, and many books have spaces in their title and author names. I have tests for when the isbn is invalid as well.

## Tests for get_patron_status_report()
I have a test that checks if the structure of what is returned by the function meets the requirements. I also test that the currently borrowed books is the same as what is returned by the get_patron_borrowed_books() function. I did the same check for the total_late_fees by iterating through each book in the borrowed_books key and calculating the individual calculate_late_fee and keeping a running sum. I also have a test for when a patron has not borrowed anything; the lists are empty, and the fees/number of books borrowed are 0.