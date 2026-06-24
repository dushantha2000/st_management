# Student Management System

[![Version](https://img.shields.io/badge/version-0.1-blue.svg)](https://www.odoo.com/)
[![Category](https://img.shields.io/badge/category-School-orange.svg)](https://www.odoo.com/)
[![License](https://img.shields.io/badge/license-LGPL--3-green.svg)](https://www.gnu.org/licenses/lgpl-3.0.en.html)

A comprehensive Odoo module designed to streamline educational institution operations by managing students, courses, and financial records efficiently.

---

## 🌟 Key Features

- **🎓 Student Information System**: Comprehensive records for students including personal details, academic history, and contact information.
- **📚 Course Management**: Easily define and manage curriculum, course details, and enrollment requirements.
- **💰 Fee Management**: Automated fee calculation and tracking system to handle student payments seamlessly.
- **⚡ Invoicing Integration**: Directly integrated with Odoo's Accounting module for automated invoice generation and financial tracking.
- **💬 Real-time Collaboration**: Built on Odoo's Chatter functionality for internal notes and student-related communications.
- **🔢 Custom Sequences**: Automated numbering for student records and fee entries for organized record-keeping.

---

## 🛠️ Installation

### Prerequisites
- Odoo 17.0 or 18.0 (Community or Enterprise)
- Python 3.10+

### Steps
1. **Clone the module** into your Odoo `custom_addons` directory:
   ```bash
   git clone https://github.com/your-repo/st_management.git
   ```
2. **Update Addon Paths**: Ensure your `odoo.conf` includes the directory where the module is located.
3. **Restart Odoo Server**: 
   ```bash
   ./odoo-bin -c odoo.conf
   ```
4. **Install Module**:
   - Log in to your Odoo instance as an Administrator.
   - Activate **Developer Mode**.
   - Navigate to **Apps** -> **Update Apps List**.
   - Search for `Student Management` and click **Activate**.

---

## 🏗️ Technical Specifications

### Dependencies
- `base`: Core Odoo framework
- `mail`: For chatter and messaging features
- `account`: For invoicing and financial integration

### Folder Structure
```text
st_management/
├── data/           # XML data for sequences and defaults
├── models/         # Business logic and database schemas
├── security/       # Access Control Lists (ACLs)
├── static/         # Icons and UI assets
└── views/          # XML definitions for the user interface
```

---

## 👤 Author

**Dushantha**
- *Odoo Customization Specialist*

---

## 📜 License

This project is licensed under the **LGPL-3 License**. See the [LICENSE](LICENSE) file for details.

---

> [!TIP]
> Need help with customization or installation? Feel free to open an issue or contact the development team.
