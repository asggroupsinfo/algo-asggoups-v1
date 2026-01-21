# Scripts Directory Organization

This directory contains all development, testing, and verification scripts organized by purpose.

## Directory Structure

### 📁 verification/
**Purpose:** Scripts that verify implementation correctness  
**Files:** 13 verification scripts (verify_*.py)  
**Usage:** Run these to verify specific features are implemented correctly

### 📁 testing/
**Purpose:** Test scripts for comprehensive testing  
**Files:** 24 test scripts (test_*.py)  
**Usage:** Automated and manual test scripts for various components

### 📁 checks/
**Purpose:** Reality check and status verification scripts  
**Files:** 12 check scripts (check_*.py)  
**Usage:** Check current status of features and implementations

### 📁 database/
**Purpose:** Database-related scripts  
**Files:** 6 database scripts  
**Usage:** Database testing, verification, and reports

### 📁 analysis/
**Purpose:** Analysis and audit scripts  
**Files:** 4 analysis scripts  
**Usage:** Bot analysis, reality checks, and improvement roadmaps

### 📁 generators/
**Purpose:** Code generation and certificate scripts  
**Files:** 3 generator scripts  
**Usage:** Generate implementations and verification certificates

### 📁 utilities/
**Purpose:** Helper and utility scripts  
**Files:** 8 utility scripts  
**Usage:** Various helper functions and demo scripts

## Usage

Each subfolder contains related scripts. Navigate to the specific folder to run scripts:

```bash
# Example: Run a verification script
cd scripts/verification
python verify_menu_systems.py

# Example: Run a test
cd scripts/testing
python test_complete_implementation.py
```

## Organization Benefits

✅ Easy to find specific type of script  
✅ Clear separation of concerns  
✅ Better maintainability  
✅ Faster development workflow
