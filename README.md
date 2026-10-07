# Provider Productivity & Compensation Analytics

## Overview

This project demonstrates a healthcare analytics and decision-support workflow using synthetic provider, encounter, productivity, quality, and compensation data.

The project was independently developed as a portfolio exercise to explore how healthcare organizations can use provider productivity and operational data to support:

- Provider performance reporting
- Productivity target monitoring
- wRVU analysis
- Quality measurement
- Incentive calculation
- Compensation analysis
- Data-quality validation and reconciliation
- Executive and operational decision support

**Note** All data and compensation values in this project are synthetic and were created for educational and portfolio purposes. They do not represent any actual provider, actual compensation methodology, or actual organizational benchmarks.

## Tools & Technologies

- Python
- Pandas
- NumPy
- Faker
- Power Query
- Power BI
- DAX

## Business Questions

The project addresses questions such as:

- How does provider productivity compare with monthly targets?
- Which providers and specialties are above or below productivity targets?
- How do wRVUs, encounters, revenue, and FTE relate to provider productivity?
- How does provider quality performance relate to productivity?
- How can incentive eligibility and incentive payments be calculated?
- How can compensation calculations be independently reconciled?
- Are provider, encounter, and monthly productivity datasets complete and internally consistent?
- How can these metrics be presented through decision-support dashboards?

## Power BI Dashboard

### 1. Executive Decision Support
Provides a high-level view of:

- Total providers and encounters
- wRVUs and revenue
- Overall productivity
- Quality performance
- Monthly wRVU trends
- Revenue by clinic
- Productivity by specialty
- Top providers by productivity

### 2. Provider Productivity
Provides provider-level analysis of:

- Actual vs. target wRVUs
- Productivity %
- wRVUs per FTE
- Revenue per wRVU
- Quality scores
- Provider productivity status

### 3. Compensation & Incentives
Analyzes:

- Productivity thresholds
- Excess wRVUs
- Incentive calculations
- Estimated compensation
- Incentive by specialty
- Monthly incentive trends
- Provider-level incentive reporting

### 4. Data Quality & Reconciliation
Includes validation checks for:

- Duplicate encounters
- Missing identifiers
- Invalid quality records
- Provider-month duplicates
- wRVU reconciliation
- Incentive reconciliation

## Data & Methodology

Synthetic healthcare data was generated in Python and loaded into Power BI through Power Query.

The Power BI model uses separate dimension and fact tables for providers, patients, CPT/services, encounters, monthly provider productivity, dates, and compensation-plan parameters.

DAX measures were developed for productivity, quality, incentive calculations, and reconciliation.

## Key Takeaways

This project provided hands-on experience with a healthcare provider analytics workflow, particularly:

- Designing a healthcare-focused analytical data model
- Working with provider productivity and wRVU concepts
- Creating Power BI measures using DAX
- Building interactive decision-support dashboards
- Translating operational metrics into actionable reporting
- Applying data-quality validation within BI reporting
- Reconciling aggregated metrics against transactional data
- Independently validating compensation/incentive calculations
- Designing reporting for both executive and operational users

The project also helped me understand the types of metrics and analytical workflows used in provider productivity, performance measurement, and compensation decision support.

