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
# Get the app (use --skip-assets to avoid Frappe v15 esbuild ordering issue)
bench get-app --skip-assets https://github.com/Sudhakar1110/Abandoned_property_restoration.git

# Install on your site
bench --site <site_name> install-app abandoned_property_restoration

# Build assets after the app is installed
bench build
```

2. After installation, the fixtures will be loaded automatically providing initial reference data.

> **Note for Frappe v15 users**: If you encounter an esbuild error during `bench get-app`, use the `--skip-assets` flag as shown above. This is a known Frappe v15 interaction where the asset build runs before the app is registered in `apps.txt`. Once installed, `bench build` will build the assets successfully.

## Troubleshooting

### Socket.IO Connection Error

If you see an error like:
```
Error connecting to socket.io: Unauthorized: Error: getaddrinfo EAI_AGAIN your-domain.local
```

This indicates a DNS resolution issue with your site's configured domain. Here's how to fix it:

#### Option 1: Add Domain to Hosts File (Recommended for Local Development)

Edit the `/etc/hosts` file and add:
```
127.0.0.1    your-domain.local
```

#### Option 2: Configure Correct Site URL

Update your site's `site_config.json` file:
```bash
# Edit the site config
bench --site <site_name> set-config host_name http://correct-domain:8000

# Or manually edit:
# /path/to/frappe-bench/sites/<site_name>/site_config.json
```

Add or update:
```json
{
  "host_name": "http://your-correct-domain:8000"
}
```

#### Option 3: Check DNS Configuration

If using a custom domain, ensure:
1. DNS A records point to your server IP
2. Your firewall allows traffic on port 8000 (Frappe) and 9000 (Socket.IO)
3. The domain resolves correctly: `ping your-domain.local`

### Workspace Blocks Not Displaying

If workspace shows "doc" or "The block can not be displayed correctly":

1. **Check Socket.IO Connection**: The error above often causes this
2. **Verify Permissions**: Ensure your user role has access to the doctypes
3. **Clear Cache**:
   ```bash
   bench --site <site_name> clear-cache
   bench --site <site_name> clear-website-cache
   ```
4. **Rebuild Assets**:
   ```bash
   bench build --app abandoned_property_restoration
   ```

### Common Issues

| Issue | Solution |
|-------|----------|
| Socket.IO connection refused | Ensure `bench start` is running and socket.io port (9000) is accessible |
| DNS EAI_AGAIN error | Add domain to `/etc/hosts` or fix DNS configuration |
| Workspace blocks missing | Check browser console for socket.io errors, fix connectivity first |
| Permission denied | Verify user role is in workspace allowed roles |

## License

MIT License