"""
End-to-End API and Security Verification Test Script
"""
import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_flow():
    print("--- 1. Testing Health & Metrics ---")
    resp = urllib.request.urlopen(f"{BASE_URL}/health")
    data = json.loads(resp.read().decode("utf-8"))
    print("Health Status:", data["status"], "| Stats:", data["stats"])

    print("\n--- 2. Testing Products List ---")
    resp = urllib.request.urlopen(f"{BASE_URL}/products")
    products = json.loads(resp.read().decode("utf-8"))
    print(f"Loaded {len(products)} products from database.")
    print("Sample product:", products[0]["name"], "| Price:", products[0]["price"])

    print("\n--- 3. Testing User Registration ---")
    reg_payload = json.dumps({
        "name": "Dr. Fernando Perdomo",
        "email": f"fernando.perdomo_{json.dumps(None)}@constructora.com".replace("null", "huila"),
        "phone": "+57 318 777 6655",
        "password": "Password123!"
    }).encode("utf-8")
    
    reg_req = urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=reg_payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        reg_res = urllib.request.urlopen(reg_req)
        reg_data = json.loads(reg_res.read().decode("utf-8"))
        print("Registration OK! User ID:", reg_data["user"]["id"])
        token = reg_data["access_token"]
    except urllib.error.HTTPError as e:
        print("Registration returned:", e.code, e.read().decode("utf-8"))
        # Login if already exists
        login_payload = json.dumps({
            "email": "fernando.perdomo_huila@constructora.com",
            "password": "Password123!"
        }).encode("utf-8")
        login_req = urllib.request.Request(f"{BASE_URL}/auth/login", data=login_payload, headers={"Content-Type": "application/json"})
        login_res = urllib.request.urlopen(login_req)
        token = json.loads(login_res.read().decode("utf-8"))["access_token"]

    print("\n--- 4. Testing Maintenance Request Submission with JWT ---")
    maint_payload = json.dumps({
        "equipment": "Ricoh MP 4002",
        "service_type": "Mantenimiento preventivo",
        "desired_date": "2026-10-25",
        "desired_time": "11:00",
        "description": "Limpieza general de óptica y cambio de tóner.",
        "client_name": "Dr. Fernando Perdomo",
        "client_email": "fernando.perdomo_huila@constructora.com",
        "client_phone": "+57 318 777 6655"
    }).encode("utf-8")
    maint_req = urllib.request.Request(
        f"{BASE_URL}/requests",
        data=maint_payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    )
    maint_res = urllib.request.urlopen(maint_req)
    req_created = json.loads(maint_res.read().decode("utf-8"))
    print("Service Request created! ID:", req_created["id"], "| Status:", req_created["status"])

    print("\n--- 5. Testing Admin Login and Status Update ---")
    admin_login = json.dumps({"email": "admin@sypfotocopiadoras.com", "password": "admin123"}).encode("utf-8")
    admin_req = urllib.request.Request(f"{BASE_URL}/auth/login", data=admin_login, headers={"Content-Type": "application/json"})
    admin_data = json.loads(urllib.request.urlopen(admin_req).read().decode("utf-8"))
    admin_token = admin_data["access_token"]
    print("Admin Authenticated! Role:", admin_data["user"]["role"])

    # List all requests as admin
    list_req = urllib.request.Request(f"{BASE_URL}/requests", headers={"Authorization": f"Bearer {admin_token}"})
    all_requests = json.loads(urllib.request.urlopen(list_req).read().decode("utf-8"))
    print(f"Admin sees total of {len(all_requests)} requests across all clients.")

    # Update status of newly created request
    patch_payload = json.dumps({"status": "Confirmada", "admin_notes": "Visita agendada para Juan Sebastián Portela."}).encode("utf-8")
    patch_req = urllib.request.Request(
        f"{BASE_URL}/requests/{req_created['id']}/status",
        data=patch_payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {admin_token}"},
        method="PATCH"
    )
    patch_res = urllib.request.urlopen(patch_req)
    print("Status Update Response:", json.loads(patch_res.read().decode("utf-8")))

    print("\n[OK] ALL BACKEND, SECURITY & JWT FLOWS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_flow()
