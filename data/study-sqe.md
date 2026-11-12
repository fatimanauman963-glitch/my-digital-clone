# My Software Quality Engineering (SQE) study notes

## Quality basics
Software Quality Engineering is about making sure software is built and tested to meet requirements and user expectations. Quality assurance is process-focused: it prevents defects by improving how we work. Quality control is product-focused: it finds defects by checking the software, mainly through testing. Verification asks whether we are building the product right, and validation asks whether we are building the right product.

## Testing levels and strategies
Unit testing checks individual functions or modules. Integration testing checks that modules work together. System testing checks the full system against the requirements. Acceptance testing checks that the customer or user accepts it. A testing strategy decides the order and scope of these levels, for example testing from small parts upwards (bottom-up) or from the main structure downwards (top-down).

## Black box and white box testing
Black box testing looks only at inputs and outputs, with no knowledge of the code. Common techniques are equivalence partitioning, where inputs are grouped into classes that should behave the same, and boundary value analysis, where I test at and around the edges of valid ranges, because bugs often hide at boundaries.
White box testing uses knowledge of the internal code. Typical goals are statement coverage, branch coverage and path coverage. Cyclomatic complexity gives the number of independent paths and helps decide how many tests are needed.

## Test plans, test cases and bug reports
A test plan describes the scope, approach, resources, schedule and risks of testing. A test case has an ID, a description, preconditions, steps, input data, expected result and actual result. A bug report records a title, steps to reproduce, expected and actual behaviour, severity, priority, environment and status, so developers can fix the issue quickly.

## My SQE course project
For my SQE course project I used WhatsApp as the application under test. I wrote project documentation with a test plan, black box and white box test cases and bug reports, and I also made a presentation about the testing. Messaging, calls, groups and settings were good areas for designing test cases because they have many inputs and edge cases.

## Cleanroom Software Engineering
Cleanroom is a quality-focused process whose aim is to prevent defects instead of fixing them later. The software is specified and designed formally, and correctness is checked through reviews and verification before the code is ever executed. It is built in small increments, and testing is statistical: the tests are based on the expected usage of the software, so I can estimate its reliability. Developers do not run their own unit tests, and a separate team does the statistical testing.
