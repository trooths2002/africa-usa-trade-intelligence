import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_monitoring_agent_imports():
    """Test that monitoring agent can be imported without syntax errors"""
    try:
        from monitoring.agent import MonitoringAgent
        assert True
    except SyntaxError:
        pytest.fail("Monitoring agent has syntax errors")
    except ImportError as e:
        pytest.fail(f"Monitoring agent import failed: {e}")

def test_monitoring_agent_initialization():
    """Test that monitoring agent initializes correctly"""
    try:
        from monitoring.agent import MonitoringAgent
        agent = MonitoringAgent()
        
        # Check that attributes are set
        assert hasattr(agent, 'api_url')
        assert hasattr(agent, 'check_interval')
        assert hasattr(agent, 'alert_threshold')
        
        # Check default values
        assert agent.check_interval == 300  # 5 minutes default
        assert agent.alert_threshold == 3   # 3 failures default
    except Exception as e:
        pytest.fail(f"Monitoring agent initialization failed: {e}")

def test_status_recording():
    """Test that status recording works correctly"""
    try:
        from monitoring.agent import MonitoringAgent
        agent = MonitoringAgent()
        
        # Record a status
        status = agent.record_status("test_component", True, {"test": "data"})
        
        # Check that status was recorded
        assert len(agent.status_history) == 1
        assert agent.status_history[0]["component"] == "test_component"
        assert agent.status_history[0]["healthy"] == True
        assert agent.status_history[0]["details"] == {"test": "data"}
    except Exception as e:
        pytest.fail(f"Status recording failed: {e}")