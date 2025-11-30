import pytest
from playwright.sync_api import Page, expect
from database import reset_database, add_sample_data

BASE_URL = "http://127.0.0.1:5000"

@pytest.fixture(autouse=True)
def reset_db():
    reset_database()        
    add_sample_data()       
    yield

def test_add_book_and_borrow(page: Page):
    # go to catalog
    page.goto(f"{BASE_URL}/catalog")

    # go to the add book page and check that is has the correct heading
    page.get_by_role("link", name="Add Book").click()
    expect(page.get_by_role("heading", name="Add New Book")).to_be_visible()
    
    # add a book
    page.fill("#title", "E2E Book 1")
    page.fill("#author", "E2E author 1")
    page.fill("#isbn", "9014832344837")
    page.fill("#total_copies", "4")
    page.click("button[type='submit']")

    #check that submitting redirects to catalog page and displays success message
    expect(page).to_have_url(f"{BASE_URL}/catalog")
    expect(page.locator(".flash-messages")).to_contain_text("E2E Book 1")

    # check that catalog displays the newly added book
    expect(page.locator("table")).to_contain_text("E2E Book 1")
    expect(page.locator("table")).to_contain_text("E2E author 1")
    expect(page.locator("table")).to_contain_text("9014832344837")

    # find the book you want to borrow 
    book_row = page.locator("table tbody tr", has_text="E2E Book 1")

    # input the patron id and press borrow
    book_row.locator("input[name='patron_id']").fill("482761")
    book_row.locator("button", has_text="Borrow").click()
    page.wait_for_timeout(500)

    # check that a successful borrow message shows up
    expect(page.get_by_text("Successfully borrowed 'E2E Book 1'."))
    

def test_search_title_and_borrow(page: Page):
    # go to catalog
    page.goto(f"{BASE_URL}/catalog")

    # got to the search page
    page.get_by_role("link", name="Search").click()
    expect(page.locator("h2")).to_contain_text("🔍 Search Books")

    # fill in search details
    page.fill("#q", "great")
    page.select_option("#type", label="Title (partial match)")
    page.click("button[type='submit']")
    page.wait_for_timeout(500)

    # check that the search result table has the correct title
    expect(page.locator("h3")).to_contain_text('Search Results for "great" (title)')

    # check that the table contains the correct data
    expect(page.locator("table")).to_contain_text("The Great Gatsby")
    expect(page.locator("table")).to_contain_text("F. Scott Fitzgerald")
    expect(page.locator("table")).to_contain_text("9780743273565")

    # borrow The Great Gatsby
    book_row = page.locator("table tbody tr", has_text="The Great Gatsby")
    book_row.locator("input[name='patron_id']").fill("480761")
    book_row.locator("button", has_text="Borrow").click()
    page.wait_for_timeout(500)

    # check that borrowing the book redirects to catalog and shows message
    expect(page).to_have_url(f"{BASE_URL}/catalog")
    expect(page.get_by_text('Successfully borrowed "The Great Gatsby".')).to_be_visible()

















