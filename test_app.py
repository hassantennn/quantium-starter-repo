import pytest

# Parametrize to check multiple element IDs
@pytest.mark.parametrize("id_value", ["app-header", "sales-chart", "region-picker"])
def test_elements_present(dash_duo, id_value):
    from app import app
    dash_duo.start_server(app)
    element = dash_duo.find_element(f"#{id_value}")
    assert element is not None

