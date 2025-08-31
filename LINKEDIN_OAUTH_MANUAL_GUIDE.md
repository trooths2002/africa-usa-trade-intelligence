# LinkedIn OAuth Manual Guide

## Overview
Since you're experiencing issues with the OAuth scope selection in the LinkedIn Developer Portal and the automatic callback server, this guide will walk you through manually completing the OAuth flow to get proper permissions for your LinkedIn API integration.

## Prerequisites
1. Your LinkedIn app is created and verified
2. Your Client ID and Client Secret are in the [.env](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/.env) file
3. The redirect URI in your LinkedIn app is set to: `http://localhost:8501`

## Step-by-Step Manual OAuth Process

### Step 1: Generate the Authorization URL
Run this script to generate the authorization URL:

```bash
python scripts/generate_auth_url.py
```

This will output an authorization URL that you need to open in your browser.

### Step 2: Authorize the Application
1. Copy the authorization URL from the script output
2. Open it in your browser
3. Log in to your LinkedIn account if prompted
4. Review the permissions requested:
   - `r_liteprofile` (Read basic profile information)
   - `r_emailaddress` (Read email address)
   - `w_member_social` (Post content on behalf of user)
5. Click "Allow" to grant these permissions

### Step 3: Capture the Authorization Code
After clicking "Allow", you'll be redirected to a URL that looks like this:
```
http://localhost:8501/?code=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX&state=random_state_string
```

Since there's no server running on localhost:8501, you'll see an error page. This is expected.

1. Copy the entire URL from your browser's address bar
2. Extract the `code` parameter (everything between `code=` and `&state=`)

### Step 4: Exchange Code for Access Token
Run this script to exchange the authorization code for an access token:

```bash
python scripts/exchange_code_for_token.py
```

When prompted, paste the authorization code you extracted in Step 3.

### Step 5: Update Your .env File
The script will automatically update your [.env](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/.env) file with the new access token.

### Step 6: Test the Integration
Test your LinkedIn API integration:

```bash
python scripts/test_linkedin_api.py
```

## Troubleshooting

### If you see "Unable to connect" error
This is expected since there's no server running on localhost:8501. Just copy the URL from the address bar.

### If you can't select scopes in the LinkedIn Developer Portal
This is a known issue that occurs after app verification. The interface may take 24-48 hours to update with the newly granted permissions. The manual OAuth flow bypasses this issue.

### If the authorization URL doesn't work
Make sure your LinkedIn app's redirect URI is set to `http://localhost:8501` in the app settings.

## Security Notes
- Access tokens expire after 2 months
- Keep your Client Secret secure and never share it
- The [.env](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/.env) file is excluded from version control via [.gitignore](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/.gitignore)