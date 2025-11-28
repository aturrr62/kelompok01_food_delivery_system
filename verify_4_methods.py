"""
Quick Endpoint Count Verification Script
Verifies that each microservice has exactly 4 HTTP methods (GET, POST, PUT, DELETE)
"""

import re
import os

def count_endpoints(file_path, service_name):
    """Count HTTP method endpoints in a service file"""
    
    if not os.path.exists(file_path):
        print(f"{service_name}: File not found - {file_path}")
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all @app.route decorators with methods
    route_pattern = r"@app\.route\(['\"]([^'\"]+)['\"]\s*,\s*methods=\[([^\]]+)\]"
    routes = re.findall(route_pattern, content)
    
    # Count unique HTTP methods (excluding /health)
    methods_count = {
        'GET': 0,
        'POST': 0,
        'PUT': 0,
        'DELETE': 0,
        'PATCH': 0
    }
    
    business_endpoints = []
    
    for route, methods_str in routes:
        # Skip health check endpoint
        if '/health' in route or route == '/':
            continue
        
        # Parse methods
        methods = [m.strip().strip("'\"") for m in methods_str.split(',')]
        
        for method in methods:
            method = method.upper()
            if method in methods_count:
                methods_count[method] += 1
                business_endpoints.append(f"{method:6} {route}")
    
    return methods_count, business_endpoints

def main():
    print("=" * 70)
    print("  MICROSERVICES ENDPOINT VERIFICATION")
    print("  Target: 4 HTTP Methods (GET, POST, PUT, DELETE) per service")
    print("=" * 70)
    print()
    
    base_path = r"c:\xampp\htdocs\food_delivery_system\microservices"
    
    services = [
        ("User Service", "user-service", 5001),
        ("Restaurant Service", "restaurant-service", 5002),
        ("Order Service", "order-service", 5003),
        ("Delivery Service", "delivery-service", 5004),
        ("Payment Service", "payment-service", 5005)
    ]
    
    all_passed = True
    
    for service_name, folder, port in services:
        file_path = os.path.join(base_path, folder, "app.py")
        
        result = count_endpoints(file_path, service_name)
        
        if result is None:
            all_passed = False
            continue
        
        methods_count, endpoints = result
        
        # Check if exactly 4 methods
        get_count = methods_count['GET']
        post_count = methods_count['POST']
        put_count = methods_count['PUT']
        delete_count = methods_count['DELETE']
        patch_count = methods_count['PATCH']
        
        total_endpoints = len(endpoints)
        
        # Validation
        has_get = get_count >= 1
        has_post = post_count >= 1
        has_put = put_count >= 1
        has_delete = delete_count >= 1
        has_patch = patch_count == 0  # Should NOT have PATCH
        
        # All 4 methods should be present
        has_all_4 = has_get and has_post and has_put and has_delete and has_patch
        
        status = "PASS" if has_all_4 else "FAIL"
        
        print(f"{status} {service_name} (Port {port})")
        print(f"     GET: {get_count} | POST: {post_count} | PUT: {put_count} | DELETE: {delete_count} | PATCH: {patch_count}")
        
        if not has_all_4:
            all_passed = False
            
            if not has_get:
                print(f"      Missing GET method!")
            if not has_post:
                print(f"      Missing POST method!")
            if not has_put:
                print(f"      Missing PUT method!")
            if not has_delete:
                print(f"      Missing DELETE method!")
            if patch_count > 0:
                print(f"      Should NOT have PATCH method! Found {patch_count}")
        
        # Show endpoints
        print(f"     Endpoints ({total_endpoints}):")
        for endpoint in endpoints:
            print(f"       {endpoint}")
        
        print()
    
    print("=" * 70)
    if all_passed:
        print("ALL SERVICES PASSED - Each has GET, POST, PUT, DELETE (no PATCH)")
    else:
        print("SOME SERVICES FAILED - Check details above")
    print("=" * 70)

if __name__ == "__main__":
    main()
