from playwright.sync_api import Page, expect
import random

def make_isbn():
    isbn = ""
    for i in range(13):
        isbn += str(random.randint(0, 9))
    return isbn


def extension():
    ext = ""
    for i in range(5):
        ext += str(random.randint(0, 9))
    return ext
        


url = "http://localhost:5000"



def test_add_book_shows_in_catalog_and_borrow(page: Page):
    page.goto(url)
    
    expect(page.get_by_text("Library Management System")).to_be_visible()
    
    page.click("text=➕ Add Book")
    expect(page.get_by_text("Add New Book")).to_be_visible()

    title = "Test Book-" + extension()
    page.fill("#title", title)
    author = "Test Author-" + extension()
    page.fill("#author", author)
    isbn = make_isbn()
    page.fill("#isbn", isbn)
    page.fill("#total_copies", "1")
    
    page.click("text=Add Book to Catalog")
    expect(page.get_by_text("Library Management System")).to_be_visible()
    
    row = page.locator("tbody tr", has_text=title)
    expect(row).to_contain_text(title)
    expect(row).to_contain_text(author)
    expect(row).to_contain_text(isbn)
    expect(row).to_have_count(1)
    
    row.locator("input[name='patron_id']").fill("123456")
    row.get_by_role("button", name="Borrow").click()
    
    expect(page.get_by_text("Successfully borrowed")).to_be_visible()


    
    
    
def test_add_book_and_search(page: Page):
    page.goto(url)

    expect(page.get_by_text("Library Management System")).to_be_visible()
    
    page.click("text=➕ Add Book")
    expect(page.get_by_text("Add New Book")).to_be_visible()

    title = "Test Book-" + extension()
    page.fill("#title", title)
    author = "Test Author-" + extension()
    page.fill("#author", author)
    isbn = make_isbn()
    page.fill("#isbn", isbn)
    page.fill("#total_copies", "1")
    
    page.click("text=Add Book to Catalog")
    expect(page.get_by_text("Library Management System")).to_be_visible()
    
    page.click("text= Search")
    expect(page.get_by_text("Search Books")).to_be_visible()
    
    page.fill("#q", title)
    page.select_option("#type", "title")
    page.get_by_role("button", name="Search").click()
    
    row = page.locator("tbody tr", has_text=title)
    expect(row).to_contain_text(title)
    expect(row).to_contain_text(author)
    expect(row).to_contain_text(isbn)
    expect(row).to_have_count(1)
    
    
        
