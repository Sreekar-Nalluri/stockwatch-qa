"""
Simplified UI Test: Complete Dashboard Workflow
Single test using the complete_ui_workflow() method
Demonstrates clean async/await pattern with server auto-start and auto-cleanup
"""

import pytest


@pytest.mark.asyncio
@pytest.mark.scenario("UI: Dashboard - Complete workflow with comprehensive verification")
async def test_dashboard_complete_workflow(test_context):
    """
    Single unified test: Launch -> Enter Key -> Load -> Verify All

    Features:
    - Server auto-starts via conftest fixture (session-scoped, autouse=True)
    - Server auto-closes after all tests via fixture cleanup
    - Uses complete_ui_workflow() method for streamlined UI interaction
    - Verifies data is loaded and displayed correctly
    """
    from src.pages.dashboard_page import DashboardPage

    page = test_context['page']
    api_key = "d83kpmpr01qkm5c8hb1gd83kpmpr01qkm5c8hb20"

    dashboard = DashboardPage(page)

    print("\n" + "="*70)
    print("UI TEST: Complete Dashboard Workflow")
    print("="*70)
    
    # Execute complete workflow
    print("\nExecuting complete UI workflow...")
    result = await dashboard.complete_ui_workflow(api_key, wait_time=5000)
    
    # Verify workflow succeeded
    assert result['success'], f"UI workflow failed: {result['error']}"
    assert result['market_status'] in ["MARKET OPEN", "MARKET CLOSED"]
    assert result['last_updated'] != "—"
    assert result['cards_count'] >= 3
    assert result['table_rows'] >= 3
    assert "$" in result['aapl_price']
    
    print("\n[Results]:")
    print(f"  Market Status: {result['market_status']}")
    print(f"  Last Updated: {result['last_updated']}")
    print(f"  Stock Cards: {result['cards_count']}")
    print(f"  Table Rows: {result['table_rows']}")
    print(f"  AAPL Price: {result['aapl_price']}")
    
    print("\n" + "="*70)
    print("[PASS] UI TEST PASSED: Complete workflow verified")
    print("="*70)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

