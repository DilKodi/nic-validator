# Sri Lankan NIC Validator - DFA Implementation

**Automata Theory**

A Deterministic Finite Automaton (DFA) implementation for validating Sri Lankan National Identity Card (NIC) numbers.

---

## 📋 Project Overview

This project implements a DFA-based validator that accepts Sri Lankan NIC numbers in two formats:
- **Old Format:** 9 digits + 'V' (e.g., `199812345V`)
- **New Format:** 12 digits (e.g., `199801234567`)

The validator uses automata theory principles to parse and validate NIC numbers, ensuring they conform to the official format specifications.

---

## 🎯 National Relevance

The Sri Lankan NIC is a critical identification document used for:
- Banking and financial services
- Government service applications
- Voter registration
- Healthcare services
- Educational enrollment

Automated validation helps prevent data entry errors in systems that process NIC numbers, improving efficiency and reducing fraud.

---

## 🔧 Project Structure

```
nic-validator/
├── nic_validator.py          # Main DFA implementation
├── test_cases.py              # Comprehensive test suite
├── README.md                  # This file
└── requirements.txt           # Python dependencies (if any)
```

---

## 🚀 Installation & Usage

### Prerequisites
- Python 3.7 or higher
- No external libraries required (pure Python implementation)

### Running the Validator

```bash
# Run the main validator with built-in tests
python nic_validator.py

# Run comprehensive test suite
python test_cases.py
```

### Interactive Mode

The validator includes an interactive mode where you can test NIC numbers:

```
Enter NIC number to validate: 199812345V
Input: 199812345V
Status: ✓ ACCEPT
Message: Valid NIC - Old Format (9 digits + V)

Extracted Information:
  - Format: Old
  - Birth Year: 1998
  - Gender: Male
  - Day of Year: 123
```

---

## 📐 DFA Design

### Formal Definition

**Alphabet (Σ):** `{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, V}`

**States (Q):** `{q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, qAccept, qReject}`

**Start State (q₀):** `q0`

**Accepting States (F):** `{qAccept}`

**Transition Function (δ):**
- States q0-q9: Accept digits 0-9 sequentially
- From q9: Accept 'V' → qAccept (old format), OR digit → q10 (new format)
- States q10-q12: Accept digits 0-9 (new format continuation)
- From q12: Accept digit → qAccept (new format complete)

### State Diagram

```
           0-9        0-9        0-9        0-9        0-9
q0 -----> q1 -----> q2 -----> q3 -----> q4 -----> q5 -----> ...
                                                              
... q6 -----> q7 -----> q8 -----> q9 -----> qAccept
       0-9       0-9       0-9       |  V (old format)
                                     |
                                     | 0-9 (new format)
                                     v
                                    q10 -----> q11 -----> q12 -----> qAccept
                                          0-9       0-9       0-9
```

---

## ✅ Features

- ✓ Full DFA implementation with state transitions
- ✓ Validates both old and new NIC formats
- ✓ Extracts information (birth year, gender, day of year)
- ✓ Comprehensive error messages
- ✓ State path tracking for debugging
- ✓ Interactive testing mode
- ✓ 50+ test cases included
- ✓ Gender detection (day > 500 = Female)
- ✓ Input sanitization (strips spaces, converts to uppercase)

---

## 🧪 Test Cases

The project includes comprehensive test coverage:

### Valid Old Format Examples
```
199812345V  ✓  Male, born 1998, day 123
955201234V  ✓  Female, born 1995, day 520
200156789V  ✓  Male, born 2001, day 567
```

### Valid New Format Examples
```
199801234567  ✓  Male, born 1998, day 012
200150112345  ✓  Female, born 2001, day 501
198503456789  ✓  Male, born 1985, day 034
```

### Invalid Examples
```
12345678V      ✗  Too short
199812345X     ✗  Invalid character
19981234567    ✗  Incomplete new format
ABCD12345V     ✗  Contains letters
```

---

## 📊 NIC Format Specification

### Old Format (Pre-2016): `YYDDDDDDDDV`
- **YY:** Last 2 digits of birth year
- **DDDDDDD:** 7-digit day number
  - 001-366: Male
  - 501-866: Female (day + 500)
- **V:** Literal character 'V'

### New Format (2016+): `YYYYDDDDDDDDC`
- **YYYY:** Full 4-digit birth year
- **DDDDDDD:** 7-digit day number (same rules as old)
- **C:** Check digit

---

## 🎯 Learning Objectives Achieved

1. ✓ **Problem Definition:** Real-world application with national relevance
2. ✓ **Automata Design:** Complete DFA with formal definition
3. ✓ **Implementation:** Working Python code with proper structure
4. ✓ **Testing:** Comprehensive test suite with edge cases
5. ✓ **Documentation:** Clear README and code comments

---

## 📝 Project Components

- [x] Python project with complete implementation
- [x] State diagram and formal definition
- [x] Test cases with ACCEPT/REJECT outcomes
- [x] Code comments and documentation

---

## 🤝 Contributing

This is an academic project. For educational purposes only.

---

## 📄 License

Educational use only - Automata Theory

---

## 👨‍💻 Author

**Dilini Kodituwakku**  
Automata Theory

---

## 📚 References

1. Department of Registration of Persons - Sri Lanka
2. Introduction to the Theory of Computation (Sipser)
3. Automata Theory, Languages, and Computation (Hopcroft, Ullman)
