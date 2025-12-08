import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
def test_bread_flow(page: Page, fastapi_server):
    page.on("console", lambda msg: print(f"Browser Console: {msg.text}"))
    
    # 1. Register
    import random
    import string
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    username = f"e2euser_{random_suffix}"
    email = f"e2e_{random_suffix}@example.com"
    password = "password123"

    try:
        page.goto("http://127.0.0.1:8000")
        page.click("text=Register")
        page.fill("#regUsername", username)
        page.fill("#regEmail", email)
        page.fill("#regPassword", password)
        
        # Handle alert
        def handle_dialog(dialog):
            assert dialog.message == "Registration successful! Please login."
            dialog.accept()
        
        page.on("dialog", handle_dialog)
        page.click("button:has-text('Register')")
        
        # 2. Login
        expect(page.locator("#loginForm")).to_be_visible()
        page.fill("#loginUsername", username)
        page.fill("#loginPassword", password)
        page.click("button:has-text('Login')")
        
        # 3. Verify Dashboard
        expect(page.locator("#dashboardSection")).to_be_visible()
    except Exception:
        page.screenshot(path="failure.png")
        error_text = page.inner_text("#authError")
        with open("error.txt", "w") as f:
            f.write(f"Auth Error: {error_text}")
        raise

    expect(page.locator("h2:has-text('My Calculations')")).to_be_visible()
    
    # 4. Add Calculation
    page.fill("#calcA", "10")
    page.fill("#calcB", "5")
    page.select_option("#calcType", "add")
    page.click("button:has-text('Calculate')")
    
    # 5. Verify in Table
    row = page.locator("table tbody tr").first
    expect(row).to_contain_text("10")
    expect(row).to_contain_text("5")
    expect(row).to_contain_text("add")
    expect(row).to_contain_text("15")
    
    # 6. Edit Calculation
    # We need to handle prompt for edit
    # Mocking prompt is tricky in Playwright directly without page.on('dialog')
    # But for edit we have multiple prompts.
    # Let's define a handler that returns values sequentially or checks message
    
    values = ["20", "4", "subtract"]
    value_index = 0
    
    def handle_edit_dialog(dialog):
        nonlocal value_index
        if dialog.type == "prompt":
            dialog.accept(values[value_index])
            value_index = (value_index + 1) % 3
        else:
            dialog.accept()

    # Remove previous listener and add new one
    page.remove_listener("dialog", handle_dialog)
    page.on("dialog", handle_edit_dialog)
    
    page.click(".edit-btn")
    
    # 7. Verify Update
    # Wait for table update - result should be 16 (20 - 4)
    expect(row).to_contain_text("20")
    expect(row).to_contain_text("4")
    expect(row).to_contain_text("subtract")
    expect(row).to_contain_text("16")
    
    # 8. Delete Calculation
    def handle_confirm(dialog):
        dialog.accept()
        
    page.remove_listener("dialog", handle_edit_dialog)
    page.on("dialog", handle_confirm)
    
    page.click(".delete-btn")
    
    # 9. Verify Gone
    expect(page.locator("table tbody tr")).to_have_count(0)
    
    # 10. Logout
    page.click("#logoutBtn")
    expect(page.locator("#authSection")).to_be_visible()
