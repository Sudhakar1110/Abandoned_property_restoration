# 🏢 Abandoned Property Restoration

A comprehensive **Frappe/ERPNext** application for identifying, restoring, preserving, and managing abandoned properties. Built for restoration companies, property developers, and private enterprises.

## 📋 Overview

This application provides an end-to-end solution for managing the lifecycle of abandoned properties — from client reporting and inspection through restoration, material salvage, and long-term maintenance. It includes robust reporting, a digital time capsule for historical preservation, and a reward system to encourage community participation.

> 🔄 **Context**: This application was originally designed for government use and has been **fully converted to a private/business-oriented context**. All government terminology has been replaced with private-sector equivalents.

---

## ✨ Features

### 📍 Property Management
- Register and track abandoned properties with detailed profiles
- Classify properties by type, category, risk level, and ownership type
- Maintain complete property timelines, images, and document records
- Track ownership history and legal status

### 👥 Client Engagement
- Allow clients to report abandoned properties via **Client Property Report**
- Reward system to incentivize community participation
- Track contributions and client recognition

### 🔍 Inspection System
- Conduct thorough **Property Inspections** with detailed assessment reports
- Assign field agents and track inspection schedules
- Document findings with structured inspection reports

### 🛠️ Restoration Projects
- Create and manage restoration projects with timelines and budgets
- Track **Restoration Progress** with milestone-based updates
- **Before/After Visualization** to document transformation
- Assign project teams (Engineers, Contractors, Field Agents)
- Monitor project costs and expense entries

### ♻️ Material Management
- **Material Salvage**: Recover and catalogue reusable materials
- **Material Exchange**: Trade materials between projects
- **Material Sale**: Sell salvaged materials to generate revenue

### 🏛️ Digital Time Capsule
- Preserve restoration history for future generations
- Store historical records, documents, and photographs
- Categorize and organize historical documentation

### 📊 Reports (14)
| Report | Description |
|--------|-------------|
| **Abandoned Property Summary** | Overview of all abandoned properties with status and risk levels |
| **Citizen Reward Report** | Track rewards issued to clients for reporting properties |
| **Digital Archive Report** | Browse the digital time capsule contents |
| **District Wise Restoration Report** | Restoration activity grouped by district |
| **Historical Records Report** | Historical documentation and records |
| **Maintenance Report** | Maintenance schedules and visit tracking |
| **Material Exchange Report** | Material exchange transactions |
| **Material Salvage Report** | Salvaged materials by category and status |
| **Project Progress Report** | Restoration project milestones and progress |
| **Property Inspection Report** | Inspection findings and compliance |
| **Property Timeline Report** | Chronological events for each property |
| **Restoration Cost Report** | Project cost breakdowns and analysis |
| **Restoration Status Report** | Current status of all restoration projects |
| **Top Contributors Report** | Most active contributors from all clients |

### 🔔 Notifications & Automation
- Automated inspection due reminders
- Maintenance schedule notifications
- Restoration completion alerts
- Reward claim status updates
- New property report notifications

### 🔒 Role-Based Access Control
| Role | Access Level |
|------|-------------|
| **System Manager** | Full administrative access |
| **Property Manager** | Manage properties, inspections, and restoration projects |
| **Restoration Manager** | Oversee restoration workflows and material management |
| **Approver** | View and approve reports and reward claims |
| **View Only User** | Read-only access to dashboards and reports |

---

## 🏗️ DocTypes (44 Total)

The application includes **44 DocTypes** organized into Master Data and Transaction records.

### Master Data (20)
| DocType | Purpose |
|---------|---------|
| Client | Individuals or entities who report properties |
| Contractor | Restoration contractors and vendors |
| Engineer | Project engineers and technical staff |
| Field Agent | On-site property inspection officers |
| Department | Organizational departments |
| Location | Geographic location references |
| District | Administrative districts |
| City | City/municipal boundaries |
| State | State/regional boundaries |
| Country | Country reference |
| Property Category | Classification (Residential, Commercial, Industrial, etc.) |
| Property Type | Specific type (House, Apartment, Factory, Warehouse, etc.) |
| Restoration Category | Type of restoration needed |
| Material Category | Classification of salvaged materials |
| Material Condition | Condition assessment (Excellent, Good, Fair, Poor, etc.) |
| Reward Type | Reward categories for property reports |
| Ownership Type | Private, Company, Corporate, Trust, Individual |
| Risk Level | Safety/structural risk assessment |
| Restoration Status | Workflow stages of restoration |
| Project Priority | Priority levels for projects |

### Transaction DocTypes (24)
| DocType | Purpose |
|---------|---------|
| Abandoned Property | Core property registration record |
| Client Property Report | Client-submitted property reports |
| Property Inspection | Inspection scheduling and execution |
| Inspection Report | Detailed inspection findings |
| Restoration Project | Project creation and management |
| Project Assignment | Team and resource assignments |
| Restoration Progress | Milestone and progress tracking |
| Before After Visualization | Photo/video documentation of transformation |
| Material Salvage | Material recovery and cataloguing |
| Material Exchange | Inter-project material transfers |
| Material Sale | Sale of salvaged materials |
| Digital Time Capsule | Historical preservation records |
| Historical Record | Archival documentation |
| Maintenance Schedule | Scheduled maintenance plans |
| Maintenance Visit | Maintenance execution records |
| Property Ownership Record | Ownership history and legal status |
| Property Timeline | Chronological property events |
| Property Images | Photographic documentation |
| Property Documents | Legal and technical documents |
| Reward Claim | Client reward requests and processing |
| Project Cost | Budget and cost tracking |
| Expense Entry | Project expense recording |

---

## 🚀 Installation

### Prerequisites
- **Frappe v15+** installed and configured
- **ERPNext** installed (required dependency)
- Python 3.10+

### Step-by-Step Installation

```bash
# 1. Navigate to your Frappe bench directory
cd ~/frappe-bench

# 2. Get the app (use --skip-assets for Frappe v15 to avoid esbuild ordering issues)
bench get-app --skip-assets https://github.com/Sudhakar1110/Abandoned_property_restoration.git

# 3. Install the app on your site
bench --site your-site.local install-app abandoned_property_restoration

# 4. Build assets after installation
bench build

# 5. Run migration to sync everything
bench --site your-site.local migrate

# 6. Clear cache
bench --site your-site.local clear-cache
```

> **Note for Frappe v15 users**: If you encounter an esbuild error during `bench get-app`, use the `--skip-assets` flag as shown above. This is a known Frappe v15 interaction where the asset build runs before the app is registered in `apps.txt`. Once installed, `bench build` will build the assets successfully.

### Quick Start (After Installation)

1. Log in to your Frappe site as **Administrator**
2. Navigate to the **Abandoned Property Restoration** workspace
3. Start by adding **Master Data** (Property Categories, Types, etc.)
4. Register an **Abandoned Property**
5. Create a **Restoration Project** and assign a team
6. Track progress and generate reports

---

## ⚙️ Configuration

### Site Configuration

Ensure your site's `site_config.json` includes:
```json
{
  "host_name": "http://your-domain:8000"
}
```

### Socket.IO (Required for Real-Time Features)

The app uses Socket.IO for real-time updates. Ensure:
- Port **9000** is open for Socket.IO connections
- Your domain resolves correctly (check `/etc/hosts` for local dev)

---

## 🛠️ Development

### Setting Up for Development

```bash
# Get the app in developer mode
bench get-app --skip-assets https://github.com/Sudhakar1110/Abandoned_property_restoration.git

# Set developer mode
bench --site your-site.local set-config developer_mode 1

# Install for development
bench --site your-site.local install-app abandoned_property_restoration

# Watch for changes (auto-builds assets)
bench watch
```

### Project Structure

```
abandoned_property_restoration/
├── config/              # App configuration
├── events/              # DocType event handlers
├── fixtures/            # Seed data (JSON)
├── hooks.py             # App hooks, fixtures, scheduler, permissions
├── install/             # After install/migrate/uninstall hooks
├── notifications/       # Notification templates
├── patches/             # Migration patches
├── permissions/         # Custom permission handlers
├── public/              # Static assets (CSS, JS)
├── restoration/         # Main module directory
│   ├── doctype/         # All 44 DocType definitions
│   └── report/          # 14 Report definitions
├── scheduler/           # Scheduled tasks
├── tasks.py             # Background task definitions
├── utils/               # Utility functions
├── workspaces/          # Workspace definitions
└── www/                 # Web pages
```

---

## 🍃 Conversion History

This application was originally designed with government terminology and has been **fully converted to a private/business context** with the following changes:

| Old (Government) | New (Private) |
|-----------------|---------------|
| Citizen → | **Client** |
| Citizen Property Report → | **Client Property Report** |
| Inspector → | **Field Agent** |
| Government Department → | **Department** |
| Property Administrator (role) → | **Property Manager** |
| Government Officer (role) → | **Approver** |

All doctype definitions, permissions, event handlers, workspace, notifications, and report configurations have been updated to reflect the new naming convention.

---

## 🔧 Troubleshooting

### Reports Show Blank White Page

**Cause**: Socket.IO connection failure or report type mismatch.

**Solution**:
```bash
# 1. Run migrate to update report records
bench --site your-site.local migrate

# 2. Clear cache
bench --site your-site.local clear-cache

# 3. Hard refresh browser (Ctrl+F5)
```

### Socket.IO Connection Error

```
Error connecting to socket.io: Unauthorized: Error: getaddrinfo EAI_AGAIN your-domain.local
```

**Solutions**:

1. **Add domain to `/etc/hosts`** (local dev):
   ```bash
   echo "127.0.0.1    your-domain.local" | sudo tee -a /etc/hosts
   ```

2. **Check DNS configuration** (production):
   ```bash
   # Verify domain resolves
   ping your-domain.local

   # Check site config
   bench --site your-site.local set-config host_name http://your-domain:8000
   ```

### Installation Fails with LinkValidationError

**Cause**: Roles referenced in workspace don't exist yet.

**Solution**: The `after_install` hook now creates roles before the workspace. If you encounter this:
```bash
# Re-run install
bench --site your-site.local install-app abandoned_property_restoration
```

### Workspace Shows "The block can not be displayed correctly"

**Solutions**:
```bash
# 1. Clear cache
bench --site your-site.local clear-cache
bench --site your-site.local clear-website-cache

# 2. Rebuild assets
bench build --app abandoned_property_restoration

# 3. Check browser console for Socket.IO errors
```

### Common Issues Quick Reference

| Issue | Likely Cause | Solution |
|-------|-------------|----------|
| `LinkValidationError` during install | Roles missing | Re-run `install-app` |
| Reports show blank page | Module Def missing | Run `bench migrate` |
| `JSON.parse("undefined")` | Server can't find report | Run `bench migrate` twice |
| Socket.IO `EAI_AGAIN` | DNS resolution issue | Update `/etc/hosts` |
| Workspace blocks broken | Socket.IO disconnected | Fix DNS, then clear cache |
| Doctypes not appearing | App not installed correctly | Re-run `install-app` |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 📬 Support

- **Email**: support@abandonedpropertyrestoration.com
- **Issues**: [GitHub Issues](https://github.com/Sudhakar1110/Abandoned_property_restoration/issues)

---

<p align="center">
  Built with ❤️ for restoring communities, one property at a time.
</p>