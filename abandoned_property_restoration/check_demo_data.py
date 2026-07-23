"""
Demo Data Verification Script
Run with: bench --site apr.bizaxl.local execute abandoned_property_restoration.check_demo_data.check_all
"""

import frappe


def check_all():
    """Check all demo data records and print a summary."""
    print("=" * 60)
    print("📊 DEMO DATA VERIFICATION REPORT")
    print("=" * 60)

    checks = [
        ("📍 LOCATIONS", [
            ("Country", "country_name", "United States"),
            ("State", "state_name", "California"),
            ("State", "state_name", "Texas"),
            ("District", "district_name", "Los Angeles County"),
            ("District", "district_name", "Harris County"),
            ("City", "city_name", "Los Angeles"),
            ("City", "city_name", "Houston"),
        ]),
        ("👥 PEOPLE & ENTITIES", [
            ("Client", "client_id", "sarah_johnson"),
            ("Client", "client_id", "michael_chen"),
            ("Client", "client_id", "emily_rodriguez"),
            ("Contractor", "contractor_name", "Premier Builders Inc"),
            ("Contractor", "contractor_name", "Heritage Restoration LLC"),
            ("Engineer", "engineer_id", "david_wilson"),
            ("Engineer", "engineer_id", "lisa_thompson"),
            ("Field Agent", "field_agent_id", "james_martinez"),
            ("Field Agent", "field_agent_id", "amanda_lee"),
            ("Department", "department_id", "property_acquisitions"),
            ("Department", "department_id", "restoration_operations"),
        ]),
        ("🏚️ PROPERTIES", [
            ("Abandoned Property", "property_name", "Oakwood Manor"),
            ("Abandoned Property", "property_name", "Maple Warehouse"),
            ("Abandoned Property", "property_name", "Pine Street Apartments"),
            ("Abandoned Property", "property_name", "Cedar Mill"),
            ("Abandoned Property", "property_name", "Birchwood Villa"),
        ]),
        ("📋 CLIENT REPORTS", [
            ("Client Property Report", "report_id", "CPR-001"),
            ("Client Property Report", "report_id", "CPR-002"),
            ("Client Property Report", "report_id", "CPR-003"),
        ]),
        ("🔍 INSPECTIONS", [
            ("Property Inspection", "inspection_id", "INS-001"),
            ("Property Inspection", "inspection_id", "INS-002"),
            ("Property Inspection", "inspection_id", "INS-003"),
        ]),
        ("🛠️ PROJECTS", [
            ("Restoration Project", "project_name", "Oakwood Manor Restoration"),
            ("Restoration Project", "project_name", "Birchwood Villa Restoration"),
        ]),
        ("📈 PROGRESS", [
            ("Restoration Progress", "restoration_project", "Oakwood Manor Restoration"),
            ("Restoration Progress", "restoration_project", "Oakwood Manor Restoration"),
            ("Restoration Progress", "restoration_project", "Oakwood Manor Restoration"),
        ]),
        ("♻️ MATERIAL SALVAGE", [
            ("Material Salvage", "material_name", "Vintage Hardwood Flooring"),
            ("Material Salvage", "material_name", "Brass Door Handles"),
            ("Material Salvage", "material_name", "Clay Roof Tiles"),
            ("Material Salvage", "material_name", "Steel Beams"),
        ]),
        ("🏛️ TIME CAPSULE & HISTORY", [
            ("Digital Time Capsule", "capsule_name", "Oakwood Manor History"),
            ("Historical Record", "record_title", "Oakwood Manor - Historical Assessment"),
        ]),
        ("💰 REWARD CLAIMS", [
            ("Reward Claim", "claim_id", "RWD-001"),
            ("Reward Claim", "claim_id", "RWD-002"),
        ]),
    ]

    total_exists = 0
    total_missing = 0

    for section_name, items in checks:
        print(f"\n📁 {section_name}")
        print("-" * 40)
        section_ok = 0
        section_missing = 0
        for doctype, field, value in items:
            filters = {field: value}
            exists = frappe.db.exists(doctype, filters)
            if exists:
                print(f"  ✅ {value} — found ({doctype})")
                section_ok += 1
                total_exists += 1
            else:
                print(f"  ❌ {value} — NOT FOUND ({doctype})")
                section_missing += 1
                total_missing += 1
        if section_missing == 0:
            print(f"  ✅ All {section_ok}/{section_ok} records present")
        else:
            print(f"  ⚠️  {section_ok} present, {section_missing} missing")

    print("\n" + "=" * 60)
    print(f"📊 SUMMARY: {total_exists} records found ✅, {total_missing} missing ❌")
    if total_missing == 0:
        print("🎉 Demo data created successfully!")
    else:
        print(f"⚠️  {total_missing} records missing — demo data may not have run correctly.")
    print("=" * 60)


def populate():
    """Run demo data creation directly via bench execute."""
    from abandoned_property_restoration.install import create_demo_data
    create_demo_data()
    print("✅ Demo data creation function executed.")
