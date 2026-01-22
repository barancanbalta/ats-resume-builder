# ATS-Friendly Resume Builder

A Streamlit-based application for creating ATS-optimized resumes with multi-language support, job posting analysis, and professional templates.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Note:** This project is under active development. Core features are functional, but additional improvements are ongoing.

## Features

### Core Functionality
- **Multi-language Support**: Turkish and English interface with automatic translation
- **ATS Optimization**: Format compliance with Applicant Tracking Systems
- **Professional Templates**: Three distinct styles (Classic, Modern, Academic)
- **Job Posting Analysis**: Calculate resume-job description matching scores
- **Export Formats**: PDF and DOCX output with live preview

### Analysis Tools
- Keyword extraction from job postings
- Percentage-based matching score calculation
- Missing skills identification
- Interactive preview before export

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/barancanbalta/ats-resume-builder.git
cd ats-resume-builder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure user data:
```bash
cp user_data.example.py user_data.py
# Edit user_data.py with your personal information
```

4. Run the application:
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

## Usage

The application guides you through the following steps:

1. **Language Selection**: Choose Turkish or English
2. **Personal Information**: Name, contact details, professional summary
3. **Work Experience**: Job titles, companies, dates, achievements
4. **Education**: Degrees, institutions, GPA, rankings
5. **Projects & Certifications**: Professional projects and credentials
6. **Skills**: Programming languages, frameworks, tools, languages
7. **Job Analysis** (Optional): Paste job description for compatibility analysis
8. **Template Selection**: Choose template and export as PDF/DOCX

## Project Structure

```
ats-resume-builder/
├── app.py                   # Main application
├── user_data.example.py     # User data template
├── requirements.txt         # Python dependencies
├── .gitignore              # Excluded files
│
├── cv_generator.py         # PDF generation module
├── cv_generator_docx.py    # DOCX generation module
├── translator_utils.py     # Translation utilities
├── matcher_utils.py        # Job matching logic
├── localization.py         # Language files
├── ui_components.py        # UI components
├── pdf_utils.py           # PDF preview utilities
│
└── fonts/                 # Font files
```

## Privacy

This application follows a privacy-first design. All personal data remains local on your machine. The `.gitignore` configuration ensures that your `user_data.py` file and generated resumes are never committed to version control.

## Technology Stack

- **Python 3.8+**
- **Streamlit** - Web framework
- **FPDF2** - PDF generation
- **python-docx** - DOCX generation
- **deep-translator** - Automatic translation
- **Pandas** - Data processing

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## Roadmap

- Additional resume templates
- Cover letter generation
- LinkedIn integration
- Enhanced ATS analysis algorithms
- Additional language support

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, please open an issue on GitHub.
