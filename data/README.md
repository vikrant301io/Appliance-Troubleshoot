# Data Folder

This folder contains application data files.

## Files

- `knowledge_base.json` - Troubleshooting database with problems, steps, and parts
- `bookings.json` - Stored booking records (auto-generated, starts empty)

## Knowledge Base Structure

The knowledge base contains:
- Common appliance problems
- Troubleshooting steps for each problem
- Suggested parts with part numbers and prices
- Safety keywords for danger detection
- Technician fee configuration

## Bookings Structure

Bookings are stored as JSON array with the following structure:
- booking_id
- timestamp
- appliance details
- customer information
- time slot
- cost breakdown

