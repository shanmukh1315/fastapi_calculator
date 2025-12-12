# tests/e2e/test_statistics_e2e.py
import pytest
from playwright.async_api import Page, expect
import time


@pytest.mark.e2e
class TestStatisticsUI:
    """End-to-end tests for statistics display in the UI."""
    
    async def register_and_login(self, page: Page) -> str:
        """Helper to register and login a user, returns token."""
        timestamp = str(int(time.time() * 1000))
        username = f"statuser_{timestamp}"
        email = f"statuser_{timestamp}@test.com"
        password = "testpass123"
        
        # Register
        await page.goto("http://127.0.0.1:8000/register")
        await page.fill('input[name="username"]', username)
        await page.fill('input[name="email"]', email)
        await page.fill('input[name="password"]', password)
        await page.fill('input[name="confirm"]', password)
        await page.click('button[type="submit"]')
        await page.wait_for_load_state("networkidle")
        
        # Login (if redirected to login page)
        if "/login" in page.url:
            await page.fill('input[name="username"]', username)
            await page.fill('input[name="password"]', password)
            await page.click('button[type="submit"]')
            await page.wait_for_load_state("networkidle")
        
        # Wait for token to be stored in localStorage
        await page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=5000)
        
        # Get token from localStorage
        token = await page.evaluate("() => localStorage.getItem('token')")
        return token
    
    @pytest.mark.asyncio
    async def test_statistics_display_with_no_calculations(self, page: Page):
        """Test that statistics show zeros when no calculations exist."""
        token = await self.register_and_login(page)
        
        await page.goto("http://127.0.0.1:8000/calculations")
        await page.wait_for_timeout(1500)
        
        # Check basic stats
        total = await page.locator("#statTotal").inner_text()
        assert total == "0"
        
        # Check detailed stats show dashes or zeros
        avg_a = await page.locator("#statAvgA").inner_text()
        avg_b = await page.locator("#statAvgB").inner_text()
        assert avg_a in ["-", "0"]
        assert avg_b in ["-", "0"]
    
    @pytest.mark.asyncio
    async def test_statistics_update_after_calculation(self, page: Page):
        """Test that statistics update immediately after creating a calculation."""
        token = await self.register_and_login(page)
        
        await page.goto("http://127.0.0.1:8000/calculations")
        await page.wait_for_timeout(1000)
        
        # Create a calculation
        await page.fill("#a", "10")
        await page.fill("#b", "5")
        await page.select_option("#type", "add")
        await page.click("#submitBtn")
        await page.wait_for_timeout(1500)
        
        # Check that total updates
        total = await page.locator("#statTotal").inner_text()
        assert total == "1"
        
        # Check last result
        last_result = await page.locator("#statLast").inner_text()
        assert last_result == "15"
        
        # Check top type
        top_type = await page.locator("#statType").inner_text()
        assert top_type == "add"
    
    @pytest.mark.asyncio
    async def test_detailed_statistics_visibility(self, page: Page):
        """Test that detailed statistics section is visible and populated."""
        token = await self.register_and_login(page)
        
        await page.goto("http://127.0.0.1:8000/calculations")
        await page.wait_for_timeout(1000)
        
        # Create multiple calculations
        calcs = [
            ("10", "5", "add"),
            ("20", "4", "multiply"),
            ("100", "10", "divide"),
        ]
        
        for a, b, op_type in calcs:
            await page.fill("#a", a)
            await page.fill("#b", b)
            await page.select_option("#type", op_type)
            await page.click("#submitBtn")
            await page.wait_for_timeout(1000)
        
        # Wait for stats to load
        await page.wait_for_timeout(2000)
        
        # Check detailed statistics are visible
        detailed_stats = page.locator("#detailedStats")
        await expect(detailed_stats).to_be_visible()
        
        # Check average operand A is populated
        avg_a = await page.locator("#statAvgA").inner_text()
        assert avg_a != "-"
        assert avg_a != ""
        
        # Check operations breakdown is visible
        operations_chart = page.locator("#operationsChart")
        await expect(operations_chart).to_be_visible()
    
    @pytest.mark.asyncio
    async def test_operations_breakdown_displays_bars(self, page: Page):
        """Test that operations breakdown shows visual bars."""
        token = await self.register_and_login(page)
        
        await page.goto("http://127.0.0.1:8000/calculations")
        await page.wait_for_timeout(1000)
        
        # Create calculations of different types
        for _ in range(3):
            await page.fill("#a", "10")
            await page.fill("#b", "2")
            await page.select_option("#type", "add")
            await page.click("#submitBtn")
            await page.wait_for_timeout(800)
        
        for _ in range(2):
            await page.fill("#a", "10")
            await page.fill("#b", "2")
            await page.select_option("#type", "multiply")
            await page.click("#submitBtn")
            await page.wait_for_timeout(800)
        
        # Wait for statistics to update
        await page.wait_for_timeout(2000)
        
        # Check that operations chart has content
        chart_content = await page.locator("#operationsChart").inner_html()
        assert len(chart_content) > 100  # Should have some HTML content
        
        # Should show "add" and "multiply" in breakdown
        assert "add" in chart_content or "Add" in chart_content
        assert "multiply" in chart_content or "Multiply" in chart_content
    
    @pytest.mark.asyncio
    async def test_min_max_results_display(self, page: Page):
        """Test that min and max results are displayed correctly."""
        token = await self.register_and_login(page)
        
        await page.goto("http://127.0.0.1:8000/calculations")
        await page.wait_for_timeout(1000)
        
        # Create calculations with varying results
        calcs = [
            ("100", "10", "divide"),   # 10
            ("5", "5", "multiply"),     # 25
            ("10", "2", "subtract"),    # 8
        ]
        
        for a, b, op_type in calcs:
            await page.fill("#a", a)
            await page.fill("#b", b)
            await page.select_option("#type", op_type)
            await page.click("#submitBtn")
            await page.wait_for_timeout(1000)
        
        # Wait for stats update
        await page.wait_for_timeout(2000)
        
        # Check min result
        min_result = await page.locator("#statMinResult").inner_text()
        assert min_result != "-"
        assert float(min_result) == 8.0
        
        # Check max result
        max_result = await page.locator("#statMaxResult").inner_text()
        assert max_result != "-"
        assert float(max_result) == 25.0
    
    @pytest.mark.asyncio
    async def test_statistics_persist_across_page_reload(self, page: Page):
        """Test that statistics are loaded correctly after page reload."""
        token = await self.register_and_login(page)
        
        await page.goto("http://127.0.0.1:8000/calculations")
        await page.wait_for_timeout(1000)
        
        # Create a calculation
        await page.fill("#a", "50")
        await page.fill("#b", "10")
        await page.select_option("#type", "multiply")
        await page.click("#submitBtn")
        await page.wait_for_timeout(1500)
        
        # Check total before reload
        total_before = await page.locator("#statTotal").inner_text()
        assert total_before == "1"
        
        # Reload page
        await page.reload()
        await page.wait_for_timeout(2000)
        
        # Check total after reload
        total_after = await page.locator("#statTotal").inner_text()
        assert total_after == "1"
        
        # Check detailed stats are still populated
        avg_a = await page.locator("#statAvgA").inner_text()
        assert avg_a != "-"
    
    @pytest.mark.asyncio
    async def test_advanced_operations_in_statistics(self, page: Page):
        """Test that advanced operations appear in statistics breakdown."""
        token = await self.register_and_login(page)
        
        await page.goto("http://127.0.0.1:8000/calculations")
        await page.wait_for_timeout(1000)
        
        # Create percent_of calculation
        await page.fill("#a", "15")
        await page.fill("#b", "200")
        await page.select_option("#type", "percent_of")
        await page.click("#submitBtn")
        await page.wait_for_timeout(1000)
        
        # Create nth_root calculation
        await page.fill("#a", "16")
        await page.fill("#b", "4")
        await page.select_option("#type", "nth_root")
        await page.click("#submitBtn")
        await page.wait_for_timeout(1000)
        
        # Create log_base calculation
        await page.fill("#a", "8")
        await page.fill("#b", "2")
        await page.select_option("#type", "log_base")
        await page.click("#submitBtn")
        await page.wait_for_timeout(2000)
        
        # Check operations chart
        chart = await page.locator("#operationsChart").inner_html()
        
        # Should show all three advanced operations
        assert "percent_of" in chart or "Percent" in chart
        assert "nth_root" in chart or "Root" in chart
        assert "log_base" in chart or "Log" in chart
    
    @pytest.mark.asyncio
    async def test_statistics_update_after_deletion(self, page: Page):
        """Test that statistics update when a calculation is deleted."""
        token = await self.register_and_login(page)
        
        await page.goto("http://127.0.0.1:8000/calculations")
        await page.wait_for_timeout(1000)
        
        # Create two calculations
        await page.fill("#a", "10")
        await page.fill("#b", "5")
        await page.select_option("#type", "add")
        await page.click("#submitBtn")
        await page.wait_for_timeout(1000)
        
        await page.fill("#a", "20")
        await page.fill("#b", "10")
        await page.select_option("#type", "add")
        await page.click("#submitBtn")
        await page.wait_for_timeout(1500)
        
        # Check total is 2
        total = await page.locator("#statTotal").inner_text()
        assert total == "2"
        
        # Delete one calculation
        delete_buttons = page.locator(".del")
        if await delete_buttons.count() > 0:
            await delete_buttons.first.click()
            await page.wait_for_timeout(1500)
            
            # Check total updated to 1
            total_after = await page.locator("#statTotal").inner_text()
            assert total_after == "1"
