# ETL Pipeline Development Task

Welcome to our technical assessment! This task will evaluate your ability to develop a robust ETL (Extract-Transform-Load) pipeline for processing accounting data.

## 📋 Task Overview

You need to develop a small ETL pipeline that reads accounting journal entries from a SQLite database, transforms and validates them according to an XSD schema, and outputs a properly formatted XML file.

## 🎯 Learning Objectives

By completing this task, you will demonstrate:
- Database connectivity and data extraction
- Data transformation and normalization techniques
- XML generation and schema compliance
- Error handling and logging
- Unit testing practices
- Code organization and documentation

## 📁 Project Structure

Your solution should include the following files:
```
solution/
├── solution.py          # Main ETL pipeline implementation
├── test_solution.py     # Comprehensive test suite
sources/
├── schema.xsd          # XML schema definition (provided)
├── journal_entries.db  # Sample SQLite database (provided)
./
├── README.md           # Documentation
└── requirements.txt    # Python dependencies
```

## 🔧 Technical Requirements

### Part 1: Core ETL Pipeline

#### 1. Extract
- Connect to a SQLite database containing a `journal_entries` table
- Table structure:
  ```sql
  CREATE TABLE journal_entries (
      Date TEXT,
      Account TEXT,
      Amount TEXT,
      Description TEXT
  );
  ```
- Handle database connection errors gracefully

#### 2. Transform
Transform the raw data according to these rules:

**Date Normalization:**
- Convert all dates to ISO format (YYYY-MM-DD)
- Handle various input formats:
  - ISO date: `2024-01-01`
  - ISO datetime: `2024-01-01T14:30:00` or `2024-01-01 14:30:00`
  - US format: `12/31/2024`
  - European format: `31-12-2024`
- Skip records with invalid dates

**Amount Normalization:**
- Convert to decimal format with exactly 2 decimal places
- Handle various input formats:
  - Whole numbers: `100` → `100.00`
  - Single decimal: `100.5` → `100.50`
  - Multiple decimals: `100.567` → `100.57` (rounded)
  - European comma decimals: `1,20` → `1.20`
  - Negative amounts: `-42.1` → `-42.10`
- Skip records with invalid amounts

**Account Validation:**
- Must be 3-12 digits only
- Skip records with invalid account numbers

**Description Processing:**
- Trim whitespace
- Truncate to 255 characters if longer
- Can be empty (optional field)

#### 3. Load
- Generate XML conforming to the provided XSD schema
- Include schema reference in the XML
- Validate XML against schema before saving
- Handle file I/O errors gracefully

### Part 2: XML Schema Compliance

Your output XML must conform to this structure:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Journal xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
         xsi:noNamespaceSchemaLocation="schema.xsd">
  <Entry>
    <Date>2024-01-01</Date>
    <Account>101</Account>
    <Amount>1200.00</Amount>
    <Description>Opening balance</Description>
  </Entry>
  <Entry>
    <Date>2024-01-02</Date>
    <Account>201</Account>
    <Amount>-500.50</Amount>
    <!-- Description is optional -->
  </Entry>
</Journal>
```

**Schema Rules:**
- Date: Must match pattern `\d{4}-\d{2}-\d{2}`
- Account: Must be 3-12 digits
- Amount: Must match pattern `-?\d+(\.\d{1,2})?`
- Description: Optional, max 255 characters

### Part 3: Error Handling & Logging

- Implement comprehensive error handling
- Log processing statistics (total records, valid records, skipped records)
- Use appropriate exception types
- Provide meaningful error messages

### Part 4: Testing

Write comprehensive tests covering:
- Data normalization functions
- Error handling scenarios  
- XML generation and schema validation (ensure the output XML is either valid or invalid according to the XSD)
- End-to-end pipeline execution
- Edge cases and invalid inputs


## 📦 Dependencies

```txt
lxml>=4.9.0
pytest>=7.0.0
```

## 🚀 Getting Started

1. Main implementation
   - Start with data normalization functions
   - Build the ETL pipeline class
   - Add error handling and logging
   - Write comprehensive tests

4. **Test your solution:**
   ```bash
   python -m pytest test_solution.py -v
   python solution.py
   ```

## ✅ Evaluation Criteria

Your solution will be evaluated on:

**Functionality (40%)**
- Correct data extraction from SQLite
- Proper data transformation and normalization
- Valid XML output conforming to schema
- Error handling for invalid data

**Code Quality (30%)**
- Clean, readable, and well-documented code
- Proper separation of concerns
- Appropriate use of classes and functions
- Meaningful variable and function names

**Testing (20%)**
- Comprehensive test coverage
- Testing edge cases and error conditions
- Proper use of pytest features
- Clear test organization

**Best Practices (10%)**
- Proper exception handling
- Logging and monitoring
- Performance considerations
- Documentation quality

## 🎯 Bonus Points

- Implement configuration management (config files)
- Add data quality metrics and reporting
- Create a simple CLI interface
- Add performance benchmarking
- Use type hints throughout
- Implement data lineage tracking

## 🚫 Common Pitfalls to Avoid

1. **Don't over-engineer:** Keep it simple and focused on the requirements
2. **Handle edge cases:** Empty databases, all invalid data, missing files
3. **Validate early:** Check data integrity before processing
4. **Test thoroughly:** Include both positive and negative test cases
5. **Document well:** Your code should be self-explanatory

## 📚 Helpful Resources

- [lxml documentation](https://lxml.de/tutorial.html)
- [SQLite Python documentation](https://docs.python.org/3/library/sqlite3.html)
- [pytest documentation](https://docs.pytest.org/)
- [XML Schema validation](https://www.w3.org/TR/xmlschema-0/)

## 🕐 Time Estimate

- Planning and setup: 10 minutes
- Core implementation: 2 hours
- Testing: 1-2 hours
- Documentation and polish: 20 minutes

**Total: 4-6 hours**

## 📝 Submission Guidelines

1. Ensure all tests pass
2. Verify XML output validates against schema
3. Include a brief README with:
   - How to run your solution
   - Design decisions you made
   - Any assumptions or limitations
   - Sample output

## 💡 Tips for Success

- **Start simple:** Get a basic version working first, then add features
- **Test as you go:** Don't wait until the end to test your code
- **Use meaningful examples:** Your test data should reflect real-world scenarios
- **Think about maintainability:** How would you extend this for more data sources?
- **Consider performance:** How would your solution scale with larger datasets?

## 🤝 Getting Help

If you have questions about the requirements or encounter technical issues:
1. Re-read the specification carefully
2. Check the provided XSD schema
3. Review the sample data structure
4. Consider the real-world context of accounting data

Remember: This task simulates a real-world scenario. Focus on creating a robust, maintainable solution that handles edge cases gracefully.

Good luck! 🚀