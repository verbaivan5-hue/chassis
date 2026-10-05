from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('file:///app/index.html')

    # Select Telescopic strut
    page.select_option('#strutType', 'telescopic')

    # Increase limits so calculation succeeds
    page.fill('#p0amMax', '16')
    page.fill('#SamMax', '700')

    # Click calculate
    page.click('#solveBtn')

    page.wait_for_timeout(2000)

    # Take a screenshot
    page.screenshot(path='/home/jules/verification/verification_error2.png', full_page=True)
    browser.close()
