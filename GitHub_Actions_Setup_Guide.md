# GitHub Actions Setup Guide for FII Scheduler

This guide will help you set up your FII Consolidated Manager to run automatically in the cloud using GitHub Actions.

## 🚀 Quick Setup Steps

### 1. Create GitHub Repository
1. Create a new GitHub repository (or use existing one)
2. Upload these files to your repository:
   - `.github/workflows/fii-scheduler.yml`
   - `FII_Consolidated_Manager_Cloud.py`
   - `requirements.txt`

### 2. Configure GitHub Secrets
Go to your repository → Settings → Secrets and variables → Actions

Add these secrets:
- `OPENAI_API_KEY`: Your OpenAI API key
- `EMAIL_USER`: Your Gmail address (e.g., your.email@gmail.com)
- `EMAIL_PASSWORD`: Your Gmail App Password (see below)

### 3. Gmail App Password Setup
1. Enable 2-factor authentication on your Gmail account
2. Go to Google Account settings → Security → 2-Step Verification
3. Generate an "App Password" for "Mail"
4. Use this 16-character password as `EMAIL_PASSWORD` secret

### 4. Test the Setup
1. Go to Actions tab in your repository
2. Click "FII Consolidated Manager Scheduler"
3. Click "Run workflow" to test manually
4. Check the logs to ensure everything works

## ⏰ Schedule Configuration

The workflow is currently set to run daily at **7:00 AM Brazil time** (10:00 UTC).

To change the schedule, edit the cron expression in `.github/workflows/fii-scheduler.yml`:
```yaml
schedule:
  - cron: '0 10 * * *'  # Change this line
```

Common cron patterns:
- `0 10 * * *` - Daily at 10:00 UTC (7:00 AM Brazil)
- `0 10 * * 1-5` - Weekdays only at 10:00 UTC
- `0 10,14 * * *` - Twice daily at 10:00 and 14:00 UTC

## 📁 File Structure

Your repository should have this structure:
```
your-repo/
├── .github/
│   └── workflows/
│       └── fii-scheduler.yml
├── FII_Consolidated_Manager_Cloud.py
├── requirements.txt
├── config/                    # Optional: for configuration files
│   ├── DEPARA-FIIs.xlsx
│   ├── API.txt
│   └── mailing.xlsx
└── output/                    # Created automatically
    ├── Fatos_Relevantes/
    └── Ofertas_Publicas/
```

## 🔍 Monitoring and Logs

### View Execution Logs
1. Go to Actions tab → Click on a workflow run
2. Click on "run-fii-manager" job
3. Expand steps to see detailed logs

### Download Results
1. After each run, check "Artifacts" section
2. Download `fii-manager-results-XXX.zip`
3. Contains logs, Excel files, and generated reports

### Email Notifications
- Success: Receives daily report with Excel attachment
- Failure: Receives error notification with details

## 🛠️ Troubleshooting

### Common Issues

**Workflow not running:**
- Check if repository is public or if you have GitHub Actions minutes
- Verify cron syntax is correct

**Email not sending:**
- Verify Gmail App Password is correct
- Check if 2FA is enabled on Gmail account
- Ensure EMAIL_USER and EMAIL_PASSWORD secrets are set

**Missing files:**
- Upload any required configuration files to `config/` folder
- Update paths in `FII_Consolidated_Manager_Cloud.py` if needed

**Python errors:**
- Check the action logs for specific error messages
- Verify all dependencies are listed in `requirements.txt`

### Getting Help
1. Check the Actions logs for specific error messages
2. Ensure all secrets are properly configured
3. Test email sending manually first

## 💰 GitHub Actions Usage

- **Public repositories**: Free unlimited minutes
- **Private repositories**: 2000 free minutes/month
- Each run takes approximately 5-10 minutes

## 🔒 Security Notes

- Never commit API keys or passwords to the repository
- Always use GitHub Secrets for sensitive information
- Consider using a dedicated email account for automation

## ✅ Final Checklist

- [ ] Repository created with all required files
- [ ] GitHub Secrets configured (OPENAI_API_KEY, EMAIL_USER, EMAIL_PASSWORD)
- [ ] Gmail App Password generated and added as secret
- [ ] Workflow tested manually and works
- [ ] Schedule configured for desired time
- [ ] Email notifications working

Your FII Consolidated Manager will now run automatically in the cloud every day at 7:00 AM Brazil time!