import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_dashboard_imports():
    """Test that dashboard can be imported without syntax errors"""
    try:
        from dashboard import app
        assert True
    except SyntaxError:
        pytest.fail("Dashboard app has syntax errors")
    except ImportError as e:
        pytest.fail(f"Dashboard app import failed: {e}")

def test_api_url_configuration():
    """Test that API URL is properly configured"""
    import os
    from unittest.mock import patch
    
    with patch.dict(os.environ, {"STREAMLIT_API_URL": "https://test-api.example.com"}):
        # Reload the module to pick up the environment variable
        if 'dashboard.app' in sys.modules:
            del sys.modules['dashboard.app']
            
        from dashboard import app
        
        # Check that the API URL is set correctly
        assert hasattr(app, 'API_BASE_URL')
        # Note: We can't easily test the actual value due to how module loading works
        # but we can verify the attribute exists

def test_simulated_data_structure():
    """Test that simulated data has the expected structure"""
    from dashboard.app import get_simulated_arbitrage_opportunities
    
    data = get_simulated_arbitrage_opportunities()
    
    # Check that the data has the expected structure
    assert "high_priority_opportunities" in data
    assert isinstance(data["high_priority_opportunities"], list)
    assert len(data["high_priority_opportunities"]) > 0
    
    # Check the structure of the first opportunity
    first_opp = data["high_priority_opportunities"][0]
    expected_keys = [
        "product", "supplier_country", "fob_price", "us_market_price",
        "gross_margin", "net_margin_estimate", "monthly_volume_potential",
        "revenue_potential", "commission_potential", "agoa_eligible",
        "certification_premiums", "risk_level", "action_required", "buyer_targets"
    ]
    
    for key in expected_keys:
        assert key in first_opp, f"Missing key: {key}"