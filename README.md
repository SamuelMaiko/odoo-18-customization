# Multi Vendor RFQ & Purchase Request Modules

## Overview  
This repository contains two Odoo modules that extend the procurement workflow:  

1. **Multi Vendor RFQ** - Enhances the existing **Purchases** module to support multi-vendor RFQs, bidding, and purchase order selection.  
2. **Purchase Request** - A standalone installable module that allows employees to submit purchase requests, which the procurement team can convert into RFQs.  

---

## 📌 Multi Vendor RFQ

### Features  
- Allows **RFQs to be sent to multiple vendors** instead of just one.  
- Vendors can **submit bids** for the RFQs they receive.  
- One-to-many relationship between an **RFQ and supplier bids**.  
- Procurement team can **select the winning bid**, triggering automatic **Purchase Order (PO) creation**.  

### Installation & Testing  
1. Ensure the **Purchases** module is installed.  
2. Install the **Multi Vendor RFQ** module via **Apps**.  
3. **Upgrade** the module after installation.  
4. Create an RFQ and **assign multiple vendors**.  
5. Submit bids as different vendors.  
6. Select a **winning bid** and verify that a **PO is generated**.  

---

## 📌 Purchase Request

### Features  
- Employees can submit **purchase requests** to the Procurement department.  
- Approved requests are used to generate **RFQs** in the **Multi Vendor RFQ** module.  

### Installation & Testing  
1. Install the **Purchase Request** module via **Apps**.  
2. Log in as an **employee** and submit a **purchase request**.  
3. Log in as **procurement staff**, review, and approve the request.  
4. Verify that an **RFQ is created** based on the request.  

---