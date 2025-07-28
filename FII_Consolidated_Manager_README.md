# FII Consolidated Manager

A unified Python application that consolidates the functionality of four separate scripts for managing Brazilian Real Estate Investment Fund (FII) data processing and email notifications.

## Overview

This consolidated manager combines the following functionalities:
- **Fatos Relevantes Processing** (Material Facts)
- **Ofertas Públicas Processing** (Public Offerings)
- **Email Notifications** for both types of documents

## Features

### 🚀 Core Features
- **Web Scraping**: Automated data collection from CVM (Brazilian Securities Commission) website
- **PDF Processing**: Downloads and extracts text from PDF documents
- **AI-Powered Analysis**: Uses OpenAI GPT to parse and summarize documents
- **Excel Generation**: Creates formatted Excel reports with hyperlinks
- **Email Automation**: Sends HTML-formatted emails via Outlook or SMTP
- **Logging**: Comprehensive logging for debugging and monitoring
- **Error Handling**: Robust error handling with fallback mechanisms

### 📊 Data Processing

#### Fatos Relevantes (Material Facts)
- Scrapes material facts from the last 7 days (configurable)
- Extracts: CNPJ, Summary, and Tenor (Positive/Neutral/Negative)
- Updates the DEPARA-FIIs.xlsx file with new funds
- Merges ticker information

#### Ofertas Públicas (Public Offerings)
- Scrapes public offering announcements from the last 30 days (configurable)
- Extracts detailed offering information including:
  - Fund details (Name, CNPJ, Ticker)
  - Offering details (Volume, Price, Target Audience)
  - Important dates (Subscription, Preference Rights, Settlement)
- Formats dates in Brazilian format (DD/MM/YY)

## Installation

### Prerequisites
```bash
# Required Python packages
pip install pandas requests openai beautifulsoup4 openpyxl selenium webdriver-manager
pip install pdfplumber PyPDF2 pywin32
```

### Directory Structure
```
C:\Users\Marco Regino\Documents\BDG-Bom Dia Gestor\
├── Códigos\
│   └── FII_Consolidated_Manager.py
├── Fatos Relevantes\          # Output directory for Material Facts
├── Ofertas Públicas\          # Output directory for Public Offerings
├── Transitory\                # Temporary files
└── Suporte\
    ├── API.txt                # OpenAI API key
    ├── DEPARA-FIIs.xlsx       # Fund ticker mapping
    └── mailing.xlsx           # Email distribution lists
```

## Usage

### Command Line Interface

```bash
# Process both Fatos Relevantes and Ofertas Públicas with emails
python FII_Consolidated_Manager.py

# Process only Fatos Relevantes
python FII_Consolidated_Manager.py --fatos

# Process only Ofertas Públicas
python FII_Consolidated_Manager.py --ofertas

# Process without sending emails
python FII_Consolidated_Manager.py --no-email
```

### Programmatic Usage

```python
from FII_Consolidated_Manager import FIIConsolidatedManager

# Initialize the manager
manager = FIIConsolidatedManager()

# Process everything
fatos_path, ofertas_path = manager.process_all(send_emails=True)

# Process individually
fatos_path = manager.process_fatos_relevantes(send_email=True)
ofertas_path = manager.process_ofertas_publicas(send_email=True)
```

## Configuration

### Email Settings
Update the SMTP configuration in the code:
```python
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SMTP_USER = "your_email@domain.com"
SMTP_PASS = "your_password"
```

### Processing Parameters
- `N_DAYS`: Number of days to look back (default: 7 for Fatos, 30 for Ofertas)
- `MAX_ROWS`: Maximum rows to display in CVM table (default: 100)
- `MAX_CHARS`: Maximum characters for GPT processing (default: 30000)

### Mailing Lists
The `mailing.xlsx` file should have:
- Column D (index 3): Email addresses
- Column E (index 4): Mark with 'x' for Fatos Relevantes recipients
- Column F (index 5): Mark with 'x' for Ofertas Públicas recipients

## Output Files

### Excel Files
- **Fatos Relevantes**: `FatosRelevantesFII_YYYYMMDD.xlsx`
- **Ofertas Públicas**: `OfertasPub_YYYYMMDD.xlsx`

### Log File
- `fii_consolidated_manager.log`: Contains detailed execution logs

## Architecture

### Class Structure

```
FIIConsolidatedManager
├── FatosRelevantesProcessor (extends FIIDataScraper)
│   ├── parse_with_gpt()
│   ├── update_depara_and_merge()
│   └── write_excel()
├── OfertasPublicasProcessor (extends FIIDataScraper)
│   ├── parse_with_gpt()
│   ├── process_dates()
│   └── write_excel()
└── EmailSender
    ├── send_fatos_relevantes_email()
    ├── send_ofertas_publicas_email()
    ├── _send_via_outlook()
    └── _send_via_smtp()
```

### Base Class: FIIDataScraper
- Handles Selenium WebDriver setup
- Performs web scraping from CVM website
- Downloads and extracts PDF content
- Provides common functionality for both processors

## Error Handling

The application includes comprehensive error handling:
- **WebDriver failures**: Logged with full stack trace
- **PDF extraction failures**: Falls back from pdfplumber to PyPDF2
- **GPT API failures**: Truncates text if token limit exceeded
- **Email failures**: Falls back from Outlook to SMTP
- **Partial failures**: Continues processing other documents if one fails

## Logging

All operations are logged with timestamps and severity levels:
- **INFO**: Normal operations
- **WARNING**: Recoverable issues (e.g., PDF extraction fallback)
- **ERROR**: Failures that stop processing

## Maintenance

### Updating the DEPARA File
The system automatically updates `DEPARA-FIIs.xlsx` when it encounters new funds. Review and add tickers manually as needed.

### Monitoring
Check the log file regularly for warnings and errors:
```bash
tail -f fii_consolidated_manager.log
```

## Troubleshooting

### Common Issues

1. **Selenium WebDriver Issues**
   - Ensure Chrome is installed
   - WebDriver Manager will auto-download the correct driver

2. **PDF Extraction Failures**
   - Some PDFs may have security restrictions
   - Check logs for specific error messages

3. **Email Sending Failures**
   - Verify SMTP credentials
   - Check if Outlook is running (for COM interface)
   - Ensure firewall allows SMTP connections

4. **GPT API Errors**
   - Verify API key in `API.txt`
   - Check OpenAI API status and quotas

## Security Notes

- Store API keys securely (not in source control)
- Use environment variables for sensitive data in production
- Regular review email distribution lists
- Monitor log files for sensitive information

## Future Enhancements

- Add support for additional document types
- Implement retry logic for transient failures
- Add configuration file support
- Create web interface for monitoring
- Add support for multiple email providers
- Implement document caching to avoid re-processing