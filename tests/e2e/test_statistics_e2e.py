# tests/e2e/test_statistics_e2e.py
import pytest
from playwright.sync_api import Page, expect
import time


@pytest.mark.e2e
class TestStatisticsUI:
    """End-to-end tests for statistics display in the UI."""
    
    def register_and_login(self, page: Page) -> str:
        """Helper to register and login a user, returns token."""
        timestamp = str(int(time.time() * 1000))
        username = f"statuser_{timestamp}"
        email = f"statuser_{timestamp}@test.com"
        password = "testpass123"
        
        # Register
        page.goto("http://localhost:8000/static/register.html")
        page.fill("#username", username)
        page.fill("#email", email)
        page.fill("#password", password)
        page.click("#registerBtn")
        page.wait_for_timeout(1000)
        
        # Login
        page.goto("http://localhost:8000/static/login.html")
        page.fill("#username", username)
        page.fill("#password", password)
        page.click("#loginBtn")
        page.wait_for_timeout(1000)
        
        # Get token from localStorage
        token = page.evaluate("() => localStorage.getItem('token')")
        return token
    
    def test_statistics_display_with_no_calculations(self, page: Page):
        """Test that statistics show zeros when no calculations exist."""
        token = self.register_and_login(page)
        
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_timeout(1500)
        
        # Check basic stats
        total = page.locator("#statTotal").inner_text()
        assert total == "0"
        
        # Check detailed stats show dashes or zeros
        avg_a = page.locator("#statAvgA").inner_text()
        avg_b = page.locator("#statAvgB").inner_text()
        assert avg_a in ["-", "0"]
        assert avg_b in ["-", "0"]
    
    def test_statistics_update_after_calculation(self, page: Page):
        """Test that statistics update immediately after creating a calculation."""
        token = self.register_and_login(page)
        
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_timeout(1000)
        
        # Create a calculation
        page.fill("#a", "10")
        page.fill("#b", "5")
        page.select_option("#type", "add")
        page.click("#submitBtn")
        page.wait_for_timeout(1500)
        
        # Check that total updates
        total = page.locator("#statTotal").inner_text()
        assert total == "1"
        
        # Check last result
        last_result = page.locator("#statLast").inner_text()
        assert last_result == "15"
        
        # Check top type
        top_type = page.locator("#statType").inner_text()
        assert top_type == "add"
    
    def test_detailed_statistics_visibility(self, page: Page):
        """Test that detailed statistics section is visible and populated."""
        token = self.register_and_login(page)
        
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_timeout(1000)
        
        # Create multiple calculations
        calcs = [
            ("10", "5", "add"),
            ("20", "4", "multiply"),
            ("100", "10", "divide"),
        ]
        
        for a, b, op_type in calcs:
            page.fill("#a", a)
            page.fill("#b", b)
            page.select_option("#type", op_type)
            page.click("#submitBtn")
            page.wait_for_timeout(1000)
        
        # Wait for stats to load
        page.wait_for_timeout(2000)
        
        # Check detailed statistics are visible
        detailed_stats = page.locator("#detailedStats")
        expect(detailed_stats).to_be_visible()
        
        # Check average operand A is populated
        avg_a = page.locator("#statAvgA").inner_text()
        assert avg_a != "-"
        assert avg_a != ""
        
        # Check operations breakdown is visible
        operations_chart = page.locator("#operationsChart")
        expect(operations_chart).to_be_visible()
    
    def test_operations_breakdown_displays_bars(self, page: Page):
        """Test that operations breakdown shows visual bars."""
        token = self.register_and_login(page)
        
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_timeout(1000)
        
        # Create calculations of different types
        for _ in range(3):
            page.fill("#a", "10")
            page.fill("#b", "2")
            page.select_option("#type", "add")
            page.click("#submitBtn")
            page.wait_for_timeout(800)
        
        for _ in range(2):
            page.fill("#a", "10")
            page.fill("#b", "2")
            page.select_option("#type", "multiply")
            page.click("#submitBtn")
            page.wait_for_timeout(800)
        
        # Wait for statistics to update
        page.wait_for_timeout(2000)
        
        # Check that operations chart has content
        chart_content = page.locator("#operationsChart").inner_html()
        assert len(chart_content) > 100  # Should have some HTML content
        
        # Should show "add" and "multiply" in breakdown
        assert "add" in chart_content or "Add" in chart_content
        assert "multiply" in chart_content or "Multiply" in chart_content
    
    def test_min_max_results_display(self, page: Page):
        """Test that min and max results are displayed correctly."""
        token = self.register_and_login(page)
        
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_timeout(1000)
        
        # Create calculations with varying results
        calcs = [
            ("100", "10", "divide"),   # 10
            ("5", "5", "multiply"),     # 25
            ("10", "2", "subtract"),    # 8
        ]
        
        for a, b, op_type in calcs:
            page.fill("#a", a)
            page.fill("#b", b)
            page.select_option("#type", op_type)
            page.click("#submitBtn")
            page.wait_for_timeout(1000)
        
        # Wait for stats update
        page.wait_for_timeout(2000)
        
        # Check min result
        min_result = page.locator("#statMinResult").inner_text()
        assert min_result != "-"
        assert float(min_result) == 8.0
        
        # Check max result
        max_result = page.locator("#statMaxResult").inner_text()
        assert max_result != "-"
        assert float(max_result) == 25.0
    
    def test_statistics_persist_across_page_reload(self, page: Page):
        """Test that statistics are loaded correctly after page reload."""
        token = self.register_and_login(page)
        
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_timeout(1000)
        
        # Create a calculation
        page.fill("#a", "50")
        page.fill("#b", "10")
        page.select_option("#type", "multiply")
        page.click("#submitBtn")
        page.wait_for_timeout(1500)
        
        # Check total before reload
        total_before = page.locator("#statTotal").inner_text()
        assert total_before == "1"
        
        # Reload page
        page.reload()
        page.wait_for_timeout(2000)
        
        # Check total after reload
        total_after = page.locator("#statTotal").inner_text()
        assert total_after == "1"
        
        # Check detailed stats are still populated
        avg_a = page.locator("#statAvgA").inner_text()
        assert avg_a != "-"
    
    def test_advanced_operations_in_statistics(self, page: Page):
        """Test that advanced operations appear in statistics breakdown."""
        token = self.register_and_login(page)
        
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_timeout(1000)
        
        # Create percent_of calculation
        page.fill("#a", "15")
        page.fill("#b", "200")
        page.select_option("#type", "percent_of")
        page.click("#submitBtn")
        page.wait_for_timeout(1000)
        
        # Create nth_root calculation
        page.fill("#a", "16")
        page.fill("#b", "4")
        page.select_option("#type", "nth_root")
        page.click("#submitBtn")
        page.wait_for_timeout(1000)
        
        # Create log_base calculation
        page.fill("#a", "8")
        page.fill("#b", "2")
        page.select_option("#type", "log_base")
        page.click("#submitBtn")
        page.wait_for_timeout(2000)
        
        # Check operations chart
        chart = page.locator("#operationsChart").inner_html()
        
        # Should show all three advanced operations
        assert "percent_of" in chart or "Percent" in chart
        assert "nth_root" in chart or "Root" in chart
        assert "log_base" in chart or "Log" in chart
    
    def test_statistics_update_after_deletion(self, page: Page):
        """Test that statistics update when a calculation is deleted."""
        token = self.register_and_login(page)
        
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_timeout(1000)
        
        # Create two calculations
        page.fill("#a", "10")
        page.fill("#b", "5")
        page.select_option("#type", "add")
        page.click("#submitBtn")
        page.wait_for_timeout(1000)
        
        page.fill("#a", "20")
        page.fill("#b", "10")
        page.select_option("#type", "add")
        page.click("#submitBtn")
        page.wait_for_timeout(1500)
        
        # Check total is 2
        total = page.locator("#statTotal").inner_text()
        assert total == "2"
        
        # Delete one calculation
        delete_buttons = page.locator(".del")
        if delete_buttons.count() > 0:
            delete_buttons.first.click()
            page.wait_for_timeout(1500)
            
            # Check total updated to 1
            total_after = page.locator("#statTotal").inner_text()
            assert total_after == "1"
