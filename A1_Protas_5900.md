# CISC 327 Assigment 1


### Kayetan Protas
### Student ID: 20415900 
### Group 3 (TA-Mir Nasreen)




## Project Implementation Status:

| Functional Requirements       | Implementation status          | What’s missing                                   | 
|-------------------------------|--------------------------------|--------------------------------------------------|
| R1: Add Book to Catalog       | Partial                        | ISBN can include letters, needs to be digits only|
|                               |                                |                                                  |
| R2: Book Catalog Display      | Completed                      |                                                  |
| R3: Book Borrowing Interface  | Completed                      |                                                  |
| R4: Book Return Processing    | Partial                        |needs to verify borrow record, update return date,|
|                               |                                |increment copies, and calculate/display late fees |
|                               |                                |                                                  |
| R5: Late Fee Calculation API  | Partial                        |Missing Fee logic, and JSON response              |
|                               |                                |                                                  |
| R6: Book Search Functionality | Partial                        |Missing search for books in catalog logic         |
|                               |                                |                                                  |
| R7: Patron Status Report      | Partial                        |get_patron_status_report function not implemnted  |





## Summary of the tests scripts

I wrote unit tests for each functional requirement (R1–R7). The unit tests focus on simple logic checks or seeing if a field exists, i tried to create a unit test for every point, within the functional requirments. Most of my unit tests use the logic from libary_service.py, but a few required me to import and use database.py aswell.

### R1: Add Book To Catalog

For R1, i tested required fields, title/author length limits, ISBN must be exactly 13 digits, and total_copies must be a positive integer. All of my tests pass, and work well.

### R2: Book Catalog Display

For R2 i did not implement any tests as i was very confused by what there even is to test, from my understanding the R2 requirment is referencing the HTML code and i am unware of how to test that.

### R3: Book Borrowing Interface

For R3 i tested the patron ID vigoursly making sure it must be 6 digits, and exist. Ontop of that i tested the book avalability, making sure that books that dont exist dont show up in the borrow_book_by_patron function. All of my tests passed and work well.

### R4: Book Return Processing

The code for R4, R5, R6 and R7 has not yet been implemnted but i tried my best to simulate testing for it using the functional requirments section. For R4 specifcally I wrote tests that accept patron/book IDs, make sure the patron actually borrowed the book, and include any late fees in the result/message.

### R5: Late Fee Calculation API

For R5, i just tested the logic for overdue books, i made sure to test all the scenarios like the book being over due, 0,3,10 and a 100 days overdue. The logic for R5 has not yet been impleted so i cannot run my unit tests.

### R6: Book Search Functionality

R6 was defintly the trickiest to test as it was pretty much all dependent on the data base, i imported the data base and assumed that there are books within the data base already and i dont have to manualy input them. I tested for title/author searches being partial and case-insensitive, while ISBN requiring exactly a 13-digit match (partials should not match). 

### R7: Patron Status Report

For R7 i wrote unit tests to make sure all the proper feilds exist in the report, borrowed books have a due date, late fees have to be a postive number and made sure that the borrowed book list matches the borrowed book count. 