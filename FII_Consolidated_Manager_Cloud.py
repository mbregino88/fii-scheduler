import datetime
import os
import time
from io import BytesIO
from urllib.parse import urljoin, urlparse, parse_qs
from pathlib import Path
import pandas as pd
import requests
import openai
from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook
from openpyxl.styles import numbers
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pdfplumber
import PyPDF2
import json
from json.decoder import JSONDecodeError
from openai import OpenAI, BadRequestError
import warnings
from PyPDF2.errors import PdfReadWarning
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
import traceback

warnings.filterwarnings("ignore", category=PdfReadWarning)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fii_consolidated_manager.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- CLOUD CONFIGURATION ---
# Detect if running in GitHub Actions
IS_GITHUB_ACTIONS = os.getenv('GITHUB_ACTIONS') == 'true'

if IS_GITHUB_ACTIONS:
    # GitHub Actions paths (relative to workspace)
    BASE_DIR = Path(".")
    FATOS_DIR = BASE_DIR / "output" / "Fatos_Relevantes"
    OFERTAS_DIR = BASE_DIR / "output" / "Ofertas_Publicas"
    TEMP_DIR = BASE_DIR / "temp"
    DEPARA_PATH = BASE_DIR / "config" / "DEPARA-FIIs.xlsx"
    API_PATH = BASE_DIR / "config" / "API.txt"
    MAILING_PATH = BASE_DIR / "config" / "mailing.xlsx"
else:
    # Local paths (original)
    BASE_DIR = Path(r"C:\Users\Marco Regino\Documents\BDG-Bom Dia Gestor")
    FATOS_DIR = BASE_DIR / "Fatos Relevantes"
    OFERTAS_DIR = BASE_DIR / "Ofertas Públicas"
    TEMP_DIR = BASE_DIR / "Transitory"
    DEPARA_PATH = BASE_DIR / "Suporte" / "DEPARA-FIIs.xlsx"
    API_PATH = BASE_DIR / "Suporte" / "API.txt"
    MAILING_PATH = BASE_DIR / "Suporte" / "mailing.xlsx"

# Create directories
FATOS_DIR.mkdir(parents=True, exist_ok=True)
OFERTAS_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# --- CHROME DRIVER SETUP FOR CLOUD ---
def setup_chrome_driver():
    """Setup Chrome driver with cloud-compatible options"""
    chrome_options = Options()
    
    if IS_GITHUB_ACTIONS:
        # GitHub Actions specific options
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
    
    try:
        if IS_GITHUB_ACTIONS:
            # Use system Chrome in GitHub Actions
            service = ChromeService()
        else:
            # Use ChromeDriverManager locally
            service = ChromeService(ChromeDriverManager().install())
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        logger.error(f"Failed to setup Chrome driver: {e}")
        return None

# --- EMAIL CONFIGURATION ---
def get_email_config():
    """Get email configuration from environment or file"""
    if IS_GITHUB_ACTIONS:
        # Use GitHub Secrets
        return {
            'user': os.getenv('EMAIL_USER'),
            'password': os.getenv('EMAIL_PASSWORD'),
            'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            'smtp_port': int(os.getenv('SMTP_PORT', '587'))
        }
    else:
        # Local configuration (implement as needed)
        return {
            'user': 'contato@bookcapital.com.br',
            'password': 'Hurst@1212',
            'smtp_server': 'smtp.office365.com',
            'smtp_port': 587
        }

# --- OPENAI CONFIGURATION ---
def get_openai_client():
    """Get OpenAI client with API key from environment"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        logger.error("OpenAI API key not found in environment variables")
        return None
    return OpenAI(api_key=api_key)

# --- EMAIL SENDING FUNCTION ---
def send_email_with_attachment(subject, body, attachment_path=None, recipients=None):
    """Send email with optional attachment"""
    try:
        config = get_email_config()
        if not config['user'] or not config['password']:
            logger.error("Email credentials not configured")
            return False
        
        msg = MIMEMultipart()
        msg['From'] = config['user']
        msg['Subject'] = subject
        
        # Default recipients for testing
        if not recipients:
            recipients = [config['user']]  # Send to self by default
        
        msg['To'] = ', '.join(recipients)
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Add attachment if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(attachment_path)}'
            )
            msg.attach(part)
        
        # Send email
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.starttls()
        server.login(config['user'], config['password'])
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Email sent successfully to {recipients}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False

# --- MAIN EXECUTION WRAPPER ---
def main():
    """Main execution function for cloud deployment"""
    logger.info("Starting FII Consolidated Manager (Cloud Version)")
    logger.info(f"Running in GitHub Actions: {IS_GITHUB_ACTIONS}")
    
    try:
        # Your existing FII processing logic would go here
        # This is a placeholder - you'll need to adapt your existing code
        
        # Example: Create a simple report
        today = datetime.date.today()
        report_content = f"FII Consolidated Manager executed successfully on {today}"
        
        # Save report
        report_path = FATOS_DIR / f"FII_Report_{today:%Y%m%d}.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # Send email notification
        send_email_with_attachment(
            subject=f"FII Report - {today}",
            body=report_content,
            attachment_path=str(report_path)
        )
        
        logger.info("FII Consolidated Manager completed successfully")
        
    except Exception as e:
        logger.error(f"FII Consolidated Manager failed: {e}")
        logger.error(traceback.format_exc())
        
        # Send error notification
        send_email_with_attachment(
            subject=f"FII Report ERROR - {datetime.date.today()}",
            body=f"FII Consolidated Manager failed with error:\n\n{str(e)}\n\n{traceback.format_exc()}"
        )
        
        raise

if __name__ == "__main__":
    main()