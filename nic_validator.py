"""
Sri Lankan National Identity Card (NIC) Validator
Automata Theory - Make-Up Assignment

This program implements a Deterministic Finite Automaton (DFA) to validate
Sri Lankan NIC numbers in both old and new formats.

Author: [Your Name]
Date: December 2025
"""

class NICValidatorDFA:
    """
    DFA-based validator for Sri Lankan NIC numbers.
    
    Accepts two formats:
    - Old Format: 9 digits + 'V' (e.g., 199812345V)
    - New Format: 12 digits (e.g., 199801234567)
    """
    
    def __init__(self):
        # Alphabet
        self.alphabet = set('0123456789V')
        
        # States
        self.states = {
            'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 
            'q7', 'q8', 'q9', 'q10', 'q11',
            'qAccept', 'qReject'
        }
        
        # Start state
        self.start_state = 'q0'
        
        # Accepting states
        self.accept_states = {'qAccept'}
        
        # Transition function (state, input) -> next_state
        self.transitions = self._build_transitions()
    
    def _build_transitions(self):
        """Build the complete transition table for the DFA."""
        transitions = {}
        
        # Digits 0-9
        digits = '0123456789'
        
        # q0 to q1: First digit
        for d in digits:
            transitions[('q0', d)] = 'q1'
        
        # q1 to q2: Second digit
        for d in digits:
            transitions[('q1', d)] = 'q2'
        
        # q2 to q3: Third digit
        for d in digits:
            transitions[('q2', d)] = 'q3'
        
        # q3 to q4: Fourth digit
        for d in digits:
            transitions[('q3', d)] = 'q4'
        
        # q4 to q5: Fifth digit
        for d in digits:
            transitions[('q4', d)] = 'q5'
        
        # q5 to q6: Sixth digit
        for d in digits:
            transitions[('q5', d)] = 'q6'
        
        # q6 to q7: Seventh digit
        for d in digits:
            transitions[('q6', d)] = 'q7'
        
        # q7 to q8: Eighth digit
        for d in digits:
            transitions[('q7', d)] = 'q8'
        
        # q8 to q9: Ninth digit
        for d in digits:
            transitions[('q8', d)] = 'q9'
        
        # q9 has two paths:
        # Path 1 (Old format): q9 + 'V' -> qAccept
        transitions[('q9', 'V')] = 'qAccept'
        
        # Path 2 (New format): q9 + digit -> q10
        for d in digits:
            transitions[('q9', d)] = 'q10'
        
        # q10 to q11: Tenth digit (new format)
        for d in digits:
            transitions[('q10', d)] = 'q11'
        
        # q11 to qAccept: Eleventh digit (new format)
        for d in digits:
            transitions[('q11', d)] = 'qAccept'
        
        return transitions
    
    def validate(self, nic):
        """
        Validate a NIC number using the DFA.
        
        Args:
            nic (str): The NIC number to validate
            
        Returns:
            tuple: (is_valid, message, path)
        """
        if not nic:
            return (False, "Empty input", [])
        
        # Strip whitespace but preserve case for validation
        nic = nic.strip()
        
        # Check for lowercase 'v' - only uppercase 'V' is valid
        if 'v' in nic:
            return (False, "Invalid character 'v' - only uppercase 'V' is allowed", [])
        
        # Now convert to uppercase for processing
        nic = nic.upper()
        
        # Track the path through states
        path = [self.start_state]
        current_state = self.start_state
        
        # Process each character
        for i, char in enumerate(nic):
            # Check if character is in alphabet
            if char not in self.alphabet:
                return (
                    False, 
                    f"Invalid character '{char}' at position {i+1}", 
                    path
                )
            
            # Get next state
            transition_key = (current_state, char)
            
            if transition_key in self.transitions:
                current_state = self.transitions[transition_key]
                path.append(current_state)
            else:
                # No valid transition - go to reject
                path.append('qReject')
                return (
                    False, 
                    f"Invalid transition at position {i+1} (state: {current_state}, input: {char})", 
                    path
                )
        
        # Check if we ended in an accepting state
        if current_state in self.accept_states:
            # Perform semantic validation for day numbers
            if not self._validate_day_number(nic):
                return (False, "Invalid day number (must be 001-366 for males, 501-866 for females)", path)
            
            format_type = "Old Format (9 digits + V)" if nic[-1] == 'V' else "New Format (12 digits)"
            return (True, f"Valid NIC - {format_type}", path)
        else:
            return (
                False, 
                f"Incomplete NIC - ended in state {current_state}", 
                path
            )
    
    def _validate_day_number(self, nic):
        """
        Validate the day number portion of the NIC.
        
        Args:
            nic (str): The NIC number (already uppercase)
            
        Returns:
            bool: True if day number is valid
        """
        try:
            if nic[-1] == 'V':
                # Old format: YY + DDD (positions 2-4 for day, 3 digits)
                day_number = int(nic[2:5])
            else:
                # New format: YYYY + DDD (positions 4-6 for day, 3 digits)
                day_number = int(nic[4:7])
            
            # Males: 001-366, Females: 501-866
            if day_number >= 1 and day_number <= 366:
                return True  # Male
            elif day_number >= 501 and day_number <= 866:
                return True  # Female
            else:
                return False
        except:
            return False
    
    def extract_info(self, nic):
        """
        Extract information from a valid NIC number.
        
        Args:
            nic (str): Valid NIC number
            
        Returns:
            dict: Extracted information
        """
        nic = nic.strip().upper()
        
        is_valid, _, _ = self.validate(nic)
        if not is_valid:
            return None
        
        info = {}
        
        # Determine format
        if nic[-1] == 'V':
            # Old format: YYDDDSSSSSV (YY=year, DDD=day, SSSSS=serial, V=suffix)
            info['format'] = 'Old'
            year_digits = nic[0:2]
            day_number = int(nic[2:5])
            
            # Determine century (assume 1900s for 00-99)
            year = int(year_digits)
            if year >= 0 and year <= 25:
                info['birth_year'] = 2000 + year
            else:
                info['birth_year'] = 1900 + year
        else:
            # New format: YYYYDDDSSSSS (YYYY=year, DDD=day, SSSSS=serial)
            info['format'] = 'New'
            info['birth_year'] = int(nic[0:4])
            day_number = int(nic[4:7])
        
        # Determine gender and day of year
        if day_number > 500:
            info['gender'] = 'Female'
            info['day_of_year'] = day_number - 500
        else:
            info['gender'] = 'Male'
            info['day_of_year'] = day_number
        
        # Validate day of year
        if info['day_of_year'] < 1 or info['day_of_year'] > 366:
            info['note'] = 'Day number out of valid range (1-366)'
        
        return info


def print_separator():
    """Print a visual separator."""
    print("=" * 70)


def print_validation_result(nic, result):
    """
    Print validation result in a formatted way.
    
    Args:
        nic (str): The NIC number tested
        result (tuple): Result from validate()
    """
    is_valid, message, path = result
    
    print(f"\nInput: {nic}")
    print(f"Status: {'✓ ACCEPT' if is_valid else '✗ REJECT'}")
    print(f"Message: {message}")
    print(f"State Path: {' → '.join(path)}")
    
    if is_valid:
        validator = NICValidatorDFA()
        info = validator.extract_info(nic)
        if info:
            print(f"\nExtracted Information:")
            print(f"  - Format: {info['format']}")
            print(f"  - Birth Year: {info['birth_year']}")
            print(f"  - Gender: {info['gender']}")
            print(f"  - Day of Year: {info['day_of_year']}")
            if 'note' in info:
                print(f"  - Note: {info['note']}")


def main():
    """Main function to demonstrate the NIC validator."""
    
    print_separator()
    print("SRI LANKAN NIC VALIDATOR - DFA IMPLEMENTATION")
    print_separator()
    
    # Create validator instance
    validator = NICValidatorDFA()
    
    # Test cases
    test_cases = [
        # Valid old format NICs
        ("199812345V", True, "Valid old format - Male born 1998"),
        ("955201234V", True, "Valid old format - Female born 1995"),
        ("200156789V", True, "Valid old format - Male born 2000"),
        ("856782345V", True, "Valid old format - Female born 1985"),
        
        # Valid new format NICs
        ("199801234567", True, "Valid new format - Male born 1998"),
        ("200150112345", True, "Valid new format - Female born 2001"),
        ("198503456789", True, "Valid new format - Male born 1985"),
        ("200256798765", True, "Valid new format - Female born 2002"),
        
        # Invalid NICs
        ("12345678V", False, "Too short (8 digits + V)"),
        ("1998123456V", False, "Too long (10 digits + V)"),
        ("19981234567", False, "11 digits (incomplete new format)"),
        ("199812345X", False, "Invalid character X"),
        ("ABCD12345V", False, "Contains letters other than V"),
        ("199812345", False, "Missing V or additional digits"),
        ("", False, "Empty input"),
        ("199812345VV", False, "Extra V at the end"),
    ]
    
    print("\n🔍 RUNNING TEST CASES:\n")
    
    for i, (nic, expected_valid, description) in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {description} ---")
        result = validator.validate(nic)
        print_validation_result(nic, result)
        
        # Verify expected result
        is_valid = result[0]
        status = "✓ PASS" if is_valid == expected_valid else "✗ FAIL"
        print(f"Test Result: {status}")
    
    print("\n" + "=" * 70)
    print("INTERACTIVE MODE")
    print("=" * 70)
    print("\nYou can now test your own NIC numbers!")
    print("Enter 'quit' to exit.\n")
    
    while True:
        user_input = input("Enter NIC number to validate: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\nThank you for using the NIC Validator!")
            break
        
        if not user_input:
            print("Please enter a valid NIC number.\n")
            continue
        
        result = validator.validate(user_input)
        print_validation_result(user_input, result)
        print()


if __name__ == "__main__":
    main()