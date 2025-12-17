"""
Additional Test Cases for NIC Validator
This file contains comprehensive test cases for testing the DFA implementation.
"""

# Import the validator (adjust import based on your file structure)
# from nic_validator import NICValidatorDFA

def get_comprehensive_test_cases():
    """
    Returns a comprehensive list of test cases.
    
    Format: (nic_number, expected_valid, description)
    """
    
    test_cases = [
        # ===== VALID OLD FORMAT (9 digits + V) =====
        ("981234567V", True, "Valid old format - Male, 1998, day 123"),
        ("955201234V", True, "Valid old format - Female, 1995, day 520"),
        ("010156789V", True, "Valid old format - Male, 2001, day 015"),
        ("856782345V", True, "Valid old format - Female, 1985, day 678"),
        ("750012345V", True, "Valid old format - Male, 1975, day 001"),
        ("983661234V", True, "Valid old format - Female, 1998, day 866"),
        ("000123456V", True, "Valid old format - Male, 2000, day 123"),
        ("255011234V", True, "Valid old format - Female, 2025, day 501"),
        
        # ===== VALID NEW FORMAT (12 digits) =====
        ("199801234567", True, "Valid new format - Male, 1998, day 012"),
        ("200150112345", True, "Valid new format - Female, 2001, day 501"),
        ("198503456789", True, "Valid new format - Male, 1985, day 034"),
        ("200256798765", True, "Valid new format - Female, 2002, day 567"),
        ("195000123456", True, "Valid new format - Male, 1950, day 001"),
        ("202586612345", True, "Valid new format - Female, 2025, day 866"),
        ("200036612345", True, "Valid new format - Male, 2000, day 366 (leap year)"),
        ("197010098765", True, "Valid new format - Male, 1970, day 100"),
        
        # ===== INVALID - LENGTH ERRORS =====
        ("12345678V", False, "Too short - only 8 digits + V"),
        ("1234567V", False, "Too short - only 7 digits + V"),
        ("1998123456V", False, "Too long - 10 digits + V"),
        ("19981234567", False, "Too short - only 11 digits (new format incomplete)"),
        ("1998012345678", False, "Too long - 13 digits"),
        
        # ===== INVALID - CHARACTER ERRORS =====
        ("199812345X", False, "Invalid character - X instead of V"),
        ("199812345v", False, "Lowercase v (should be uppercase V)"),
        ("ABCD12345V", False, "Contains non-digit letters"),
        ("1998-12345V", False, "Contains hyphen"),
        ("1998 12345V", False, "Contains space"),
        ("199812.45V", False, "Contains period/dot"),
        ("199812345VV", False, "Double V at the end"),
        ("V123456789", False, "V at the beginning"),
        
        # ===== INVALID - FORMAT ERRORS =====
        ("199812345", False, "Missing V or additional digits"),
        ("", False, "Empty input"),
        ("V", False, "Only V character"),
        ("123456789", False, "9 digits without V"),
        ("12345678901", False, "11 digits - incomplete new format"),
        
        # ===== EDGE CASES =====
        ("000000001V", False, "All zeros except last digit"),
        ("999999999V", False, "All nines"),
        ("199900000V", False, "Day number 000 (invalid)"),
        ("000000000V", False, "All zeros"),
        ("   981234567V   ", True, "Valid with leading/trailing spaces (should be stripped)"),
        
        # ===== BOUNDARY TESTING - DAY NUMBERS =====
        ("199800112V", False, "Day 001 in old format - should use 3 digits not 4"),
        ("198536612V", True, "Day 853 in old format - valid female day (853-500=353)"),
        ("199886712V", False, "Day 867 (out of range) in old format - wrong position"),
        
        # ===== REAL-WORLD EXAMPLES (ANONYMIZED) =====
        ("923456789V", True, "Typical 90s birth - old format"),
        ("197812345V", True, "1978 birth - old format"),
        ("200012345V", True, "Born in 2000 - old format"),
        ("200000112345", True, "Born in 2000 - new format"),
        ("199512312345", True, "1995 birth - new format"),
    ]
    
    return test_cases


def run_all_tests():
    """
    Run all test cases and generate a report.
    """
    from nic_validator import NICValidatorDFA
    
    validator = NICValidatorDFA()
    test_cases = get_comprehensive_test_cases()
    
    passed = 0
    failed = 0
    
    print("=" * 80)
    print("COMPREHENSIVE NIC VALIDATOR TEST SUITE")
    print("=" * 80)
    print(f"\nTotal Test Cases: {len(test_cases)}\n")
    
    for i, (nic, expected_valid, description) in enumerate(test_cases, 1):
        result = validator.validate(nic)
        is_valid = result[0]
        
        # Check if test passed
        test_passed = (is_valid == expected_valid)
        
        if test_passed:
            passed += 1
            status = "✓ PASS"
        else:
            failed += 1
            status = "✗ FAIL"
        
        print(f"{i:3d}. [{status}] {description}")
        print(f"     Input: '{nic}' | Expected: {'VALID' if expected_valid else 'INVALID'} | Got: {'VALID' if is_valid else 'INVALID'}")
        
        if not test_passed:
            print(f"     Message: {result[1]}")
        print()
    
    # Summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {len(test_cases)}")
    print(f"Passed: {passed} ({passed/len(test_cases)*100:.1f}%)")
    print(f"Failed: {failed} ({failed/len(test_cases)*100:.1f}%)")
    print("=" * 80)
    
    return passed == len(test_cases)


if __name__ == "__main__":
    all_passed = run_all_tests()
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! 🎉")
    else:
        print("\n⚠️  SOME TESTS FAILED - Please review above")