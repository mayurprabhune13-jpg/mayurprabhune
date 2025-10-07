#!/usr/bin/env python3
"""
Schema Validation Tool for GEO Phase 1
Validates JSON-LD schema markup without requiring a live server
"""

import json
import re
from pathlib import Path


def extract_json_ld(file_path):
    """Extract JSON-LD blocks from HTML templates"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all JSON-LD script blocks
    pattern = r'<script type="application/ld\+json">\s*(.*?)\s*</script>'
    matches = re.findall(pattern, content, re.DOTALL)
    
    return matches


def validate_json_syntax(json_str):
    """Validate JSON syntax"""
    try:
        data = json.loads(json_str)
        return True, data, None
    except json.JSONDecodeError as e:
        return False, None, str(e)


def validate_person_schema(data):
    """Validate Person schema requirements"""
    required_fields = ['@context', '@type', 'name']
    recommended_fields = ['jobTitle', 'worksFor', 'url', 'email', 'telephone']
    
    errors = []
    warnings = []
    
    # Check required fields
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Check @type
    if data.get('@type') != 'Person':
        errors.append(f"Expected @type 'Person', got '{data.get('@type')}'")
    
    # Check recommended fields
    for field in recommended_fields:
        if field not in data:
            warnings.append(f"Missing recommended field: {field}")
    
    return errors, warnings


def validate_faq_schema(data):
    """Validate FAQ schema requirements"""
    errors = []
    warnings = []
    
    # Check required fields
    if data.get('@type') != 'FAQPage':
        errors.append(f"Expected @type 'FAQPage', got '{data.get('@type')}'")
    
    if 'mainEntity' not in data:
        errors.append("Missing required field: mainEntity")
        return errors, warnings
    
    # Validate each FAQ item
    main_entity = data['mainEntity']
    if not isinstance(main_entity, list):
        errors.append("mainEntity should be a list of Question items")
        return errors, warnings
    
    for i, item in enumerate(main_entity):
        if item.get('@type') != 'Question':
            errors.append(f"FAQ item {i+1}: Expected @type 'Question', got '{item.get('@type')}'")
        
        if 'name' not in item:
            errors.append(f"FAQ item {i+1}: Missing required field 'name'")
        
        if 'acceptedAnswer' not in item:
            errors.append(f"FAQ item {i+1}: Missing required field 'acceptedAnswer'")
        else:
            answer = item['acceptedAnswer']
            if answer.get('@type') != 'Answer':
                errors.append(f"FAQ item {i+1}: Expected acceptedAnswer @type 'Answer', got '{answer.get('@type')}'")
            if 'text' not in answer:
                errors.append(f"FAQ item {i+1}: Missing answer text")
    
    return errors, warnings


def validate_local_business_schema(data):
    """Validate LocalBusiness schema requirements"""
    required_fields = ['@context', '@type', 'name', 'address']
    recommended_fields = ['telephone', 'email', 'url', 'openingHours']
    
    errors = []
    warnings = []
    
    # Check required fields
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Check @type
    if data.get('@type') != 'LocalBusiness':
        errors.append(f"Expected @type 'LocalBusiness', got '{data.get('@type')}'")
    
    # Validate address structure
    if 'address' in data:
        address = data['address']
        if not isinstance(address, dict):
            errors.append("Address should be a PostalAddress object")
        else:
            if address.get('@type') != 'PostalAddress':
                warnings.append("Address should have @type 'PostalAddress'")
            
            address_fields = ['addressLocality', 'addressRegion', 'addressCountry']
            for field in address_fields:
                if field not in address:
                    warnings.append(f"Missing recommended address field: {field}")
    
    # Check recommended fields
    for field in recommended_fields:
        if field not in data:
            warnings.append(f"Missing recommended field: {field}")
    
    return errors, warnings


def main():
    """Main validation function"""
    print("🔍 GEO Phase 1 Schema Validation Tool")
    print("=" * 50)
    
    # Files to validate
    files_to_check = [
        ('app/templates/base.html', 'Person Schema'),
        ('app/templates/index.html', 'FAQ Schema'),
        ('app/templates/contact.html', 'LocalBusiness Schema'),
        ('app/templates/services.html', 'Service Schema'),
        ('app/templates/about.html', 'Review/Testimonial Schema')
    ]
    
    total_errors = 0
    total_warnings = 0
    
    for file_path, schema_type in files_to_check:
        print(f"\n📄 Checking {file_path} ({schema_type})")
        print("-" * 40)
        
        if not Path(file_path).exists():
            print(f"❌ File not found: {file_path}")
            continue
        
        # Extract JSON-LD blocks
        json_blocks = extract_json_ld(file_path)
        
        if not json_blocks:
            print(f"⚠️  No JSON-LD blocks found in {file_path}")
            continue
        
        for i, json_str in enumerate(json_blocks):
            print(f"\n  Block {i+1}:")
            
            # Validate JSON syntax
            valid, data, error = validate_json_syntax(json_str)
            
            if not valid:
                print(f"    ❌ JSON Syntax Error: {error}")
                total_errors += 1
                continue
            
            print(f"    ✅ Valid JSON syntax")
            print(f"    📋 Schema type: {data.get('@type', 'Unknown')}")
            
            # Schema-specific validation
            errors = []
            warnings = []
            
            if data.get('@type') == 'Person':
                errors, warnings = validate_person_schema(data)
            elif data.get('@type') == 'FAQPage':
                errors, warnings = validate_faq_schema(data)
            elif data.get('@type') == 'LocalBusiness':
                errors, warnings = validate_local_business_schema(data)
            
            # Report results
            if errors:
                print(f"    ❌ Errors ({len(errors)}):")
                for error in errors:
                    print(f"      • {error}")
                total_errors += len(errors)
            
            if warnings:
                print(f"    ⚠️  Warnings ({len(warnings)}):")
                for warning in warnings:
                    print(f"      • {warning}")
                total_warnings += len(warnings)
            
            if not errors and not warnings:
                print(f"    🎉 Perfect! No issues found")
    
    # Summary
    print(f"\n📊 Validation Summary")
    print("=" * 30)
    print(f"Total Errors: {total_errors}")
    print(f"Total Warnings: {total_warnings}")
    
    if total_errors == 0:
        print("🎉 All schemas are valid and ready for testing!")
        print("\nNext steps:")
        print("1. Test with Google Rich Results Test: https://search.google.com/test/rich-results")
        print("2. Validate with Schema.org validator: https://validator.schema.org/")
        print("3. Check live pages once deployed")
    else:
        print("❌ Please fix the errors before proceeding")
    
    return total_errors == 0


if __name__ == '__main__':
    main()