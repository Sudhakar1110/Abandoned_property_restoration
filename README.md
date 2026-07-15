# Abandoned Property Restoration

A Frappe application for managing abandoned property restoration processes.

## Features

- **Property Management**: Track abandoned properties, their status, location, and restoration details
- **Citizen Reporting**: Allow citizens to report abandoned properties for rewards
- **Inspection System**: Conduct property inspections with detailed assessments
- **Restoration Projects**: Manage restoration projects with timelines, budgets, and progress tracking
- **Material Management**: Salvage, exchange, and sell materials from restoration projects
- **Digital Time Capsule**: Preserve restoration progress and historical records
- **Reward System**: Track and manage rewards for citizen reports
- **Maintenance Scheduling**: Schedule and track property maintenance

## DocTypes

The application includes **44 DocTypes**:

### Master Data (17)
- Citizen, Contractor, Engineer, Inspector
- Government Department, Location, District, City, State, Country
- Property Category, Property Type, Restoration Category
- Material Category, Material Condition, Reward Type
- Ownership Type, Risk Level, Restoration Status, Project Priority

### Transaction DocTypes (27)
- Abandoned Property, Citizen Property Report
- Property Inspection, Inspection Report
- Restoration Project, Project Assignment
- Restoration Progress, Before After Visualization
- Material Salvage, Material Exchange, Material Sale
- Digital Time Capsule, Historical Record
- Maintenance Schedule, Maintenance Visit
- Property Ownership Record, Property Timeline
- Property Images, Property Documents
- Reward Claim, Project Cost, Expense Entry

## Installation

1. Install the app in your Frappe bench:
```bash
bench get-app abandoned_property_restoration <repository_url>
bench --site <site_name> install-app abandoned_property_restoration
```

2. After installation, the fixtures will be loaded automatically providing initial reference data.

## License

MIT License