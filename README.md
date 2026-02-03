# PostgreSQL Cheatsheet 📘

A comprehensive, interactive guide to PostgreSQL commands and best practices. Built with Streamlit for an optimal developer experience.

## 🌟 Features

- **29 PostgreSQL Topics** - From basics (Database, Schema, Table) to advanced features (Replication, Monitoring)
- **Interactive Navigation** - Easy-to-use sidebar with Table of Contents
- **Code Snippets** - Copy-paste ready SQL examples for every command
- **Best Practices** - Tips and tricks section in each topic
- **Professional UI** - Clean, gradient-based interface inspired by Snowflake Cheatsheet
- **Developer Friendly** - Perfect for quick reference while working

## 📚 Topics Covered

### Core Database Concepts
- 🔤 Data Types
- 🗄️ Database
- 📂 Schema
- 📊 Table
- 🔐 Constraints
- ⚡ Index

### Data Manipulation
- ➕ Insert
- 🔍 Select
- ✏️ Update
- 🗑️ Delete
- 🔗 Joins
- 📊 Aggregation

### Functions & Logic
- ⚙️ Functions
- 📋 JSON
- 🔧 Procedures
- ⚡ Triggers
- 🔄 Transactions

### Database Objects
- 👁️ View
- 📸 Materialized View
- 📂 Partitioning
- ⚡ Performance

### Administration & Security
- 👥 Roles & Users
- 🔑 Permissions
- 💾 Backup & Restore
- 🧩 Extensions

### Advanced Features
- 🔎 Full Text Search
- 🔄 Replication
- 📊 Monitoring

## 🚀 Quick Start

### Live Demo
[**Open PostgreSQL Cheatsheet on Streamlit Cloud**](https://your-streamlit-cloud-url-here) *(Add your Streamlit Cloud link here after deployment)*

### Run Locally

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/postgresql-cheatsheet.git
cd postgresql-cheatsheet
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the app**
```bash
streamlit run app.py
```

4. **Open in browser**
```
http://localhost:8501
```

## 📋 Requirements

- Python 3.8+
- Streamlit
- See `requirements.txt` for full list

## 📦 Installation

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 🎯 How to Use

1. **Browse Topics** - Select any topic from the sidebar Table of Contents
2. **View All Topics** - Click "📚 All Topics" to see everything at once
3. **Copy Code** - Click the copy button on any code snippet
4. **Learn Tips** - Each section includes best practices and gotchas
5. **Reference** - Keep this open in a browser tab while you work

## 🏗️ Project Structure

```
postgresql-cheatsheet/
├── app.py                # Main Streamlit application
├── layout.py             # Layout management utilities
├── utils.py              # Helper functions
├── segments/             # Individual topic modules
│   ├── database.py
│   ├── schema.py
│   ├── table.py
│   ├── insert.py
│   ├── select.py
│   ├── update.py
│   ├── delete.py
│   ├── joins.py
│   ├── functions.py
│   ├── procedures.py
│   ├── triggers.py
│   ├── views.py
│   ├── indexes.py
│   ├── roles_users.py
│   ├── permissions.py
│   ├── transactions.py
│   ├── backup_restore.py
│   ├── replication.py
│   ├── monitoring.py
│   ├── performance.py
│   ├── partitioning.py
│   ├── json_data.py
│   ├── full_text_search.py
│   ├── extensions.py
│   ├── aggregation.py
│   ├── constraints.py
│   ├── data_types.py
│   ├── materialized_view.py
│   └── __init__.py
├── logo/                 # Logo and images
└── README.md            # This file
```

## 🎨 Features Explained

### Interactive Navigation
- Select individual topics from the sidebar
- View all topics at once with "📚 All Topics" option
- Responsive design works on desktop and mobile

### Code Examples
Every topic includes:
- Clear SQL syntax examples
- Real-world use cases
- Step-by-step explanations
- Common gotchas and best practices

### Professional Layout
- Full-width PostgreSQL logo
- Expandable "How to Use" guide
- Legend explaining notation conventions
- Official documentation links

## 📖 Legend

- `[ BRACKETS ]` - Optional parameters that can be omitted
- `{ CURLY | BRACKETS }` - Available options (choose one)
- `< angle.brackets >` - Entity names (table, schema, database names)
- `--` - SQL comments
- `;` - Statement terminator

## 🤝 Contributing

Contributions are welcome! If you find errors, have suggestions, or want to add new topics:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add improvement'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Open a Pull Request

## 🐛 Bug Reports

If you find a bug or have a suggestion, please [open an issue](https://github.com/yourusername/postgresql-cheatsheet/issues) on GitHub.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by the [Snowflake Cheatsheet](https://github.com/syasini/snowflake_cheatsheet) project
- Built with [Streamlit](https://streamlit.io/)
- Uses the [PostgreSQL documentation](https://www.postgresql.org/docs/) as reference
- Made with ❤️ for the PostgreSQL community

## 📚 Resources

- [Official PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [PostgreSQL Wiki](https://wiki.postgresql.org/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)

## 🔗 Links

- **Live App**: [Streamlit Cloud](https://postgre-sql-cheat-sheet.streamlit.app/)
- **GitHub**: [Repository](https://github.com/sarotechhub/PostgreSQL-Cheatsheet-Streamlit)
- **PostgreSQL**: [Official Website](https://www.postgresql.org/)

---

**PostgreSQL Cheatsheet v2.0**

Made with ❤️ by Saravanakumar - AWS Developer

*Powered by Streamlit | Inspired by the Snowflake Community*
