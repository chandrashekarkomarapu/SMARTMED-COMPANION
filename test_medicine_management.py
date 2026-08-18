from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_medicines_page_includes_add_medicine_form():
    response = client.get('/medicines')
    assert response.status_code == 200
    html = response.text
    assert 'id="medicine-form"' in html
    assert 'name="name"' in html
    assert 'data-i18n="add_medicine_button"' in html


def test_create_medicine_api_accepts_manual_entries():
    payload = {
        'name': 'Ibuprofen',
        'strength': '200 mg',
        'frequency': 'Twice daily',
        'duration': '5 days',
        'instructions': 'Take after food',
        'source': 'User-entered'
    }

    response = client.post('/medicines', json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body['status'] == 'success'
    assert body['medicine']['name'] == 'Ibuprofen'


def test_dashboard_has_editable_medicine_controls():
    response = client.get('/dashboard')
    assert response.status_code == 200
    html = response.text
    assert 'data-medicine-action="edit"' in html
    assert 'data-medicine-action="delete"' in html
    assert 'dashboard-medicine-form' in html


def test_reminders_page_includes_add_reminder_form():
    response = client.get('/reminders')
    assert response.status_code == 200
    html = response.text
    assert 'id="reminder-form"' in html
    assert 'name="medicine_name"' in html
    assert 'Add reminder' in html


def test_create_reminder_api_accepts_manual_entries():
    payload = {
        'medicine_name': 'Vitamin D',
        'time': '09:00',
        'frequency': 'Once daily',
        'notes': 'Take after breakfast'
    }

    response = client.post('/reminders', json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body['status'] == 'success'
    assert body['reminder']['medicine_name'] == 'Vitamin D'


def test_base_template_has_language_and_search_controls():
    response = client.get('/dashboard')
    assert response.status_code == 200
    html = response.text
    assert 'id="global-search-input"' in html
    assert 'id="language-select"' in html


def test_reminders_and_dashboard_forms_use_translation_hooks():
    response = client.get('/reminders')
    assert response.status_code == 200
    html = response.text
    assert 'data-i18n="medicine_name_field"' in html
    assert 'data-i18n="save_reminder_button"' in html

    dashboard_response = client.get('/dashboard')
    dashboard_html = dashboard_response.text
    assert 'data-i18n="active_status"' in dashboard_html
    assert 'data-i18n="save_changes_button"' in dashboard_html


def test_scanner_and_disclaimer_use_translation_hooks():
    response = client.get('/scanner')
    assert response.status_code == 200
    html = response.text
    assert 'data-i18n="prescription_intake"' in html
    assert 'data-i18n="scan_extract"' in html
    assert 'data-i18n="confirm_and_save"' in html
    assert 'data-i18n="disclaimer"' in html
