# LinkedIn App Setup Guide
## For Africa-USA Agriculture Trade Intelligence Platform

## Step-by-Step Instructions

### 1. Create a LinkedIn Developer Account
1. Go to [LinkedIn Developer Portal](https://www.linkedin.com/developers/)
2. Click "Create app" in the top right corner
3. If you don't have a LinkedIn account, you'll need to create one first

### 2. Create Your App
1. Click "Create app" 
2. Fill in the required information:
   - **App name**: Free World Trade Africa-USA Trade Intelligence
   - **Company**: If you have a company page, select it. Otherwise, you can create one or select "No Company"
   - **Privacy policy URL**: You can use your GitHub repo URL or create a simple privacy policy
   - **Business email**: Your business email address
   - **App logo**: You can upload a logo later

### 3. Complete App Verification
1. LinkedIn will send a verification code to your email
2. Enter the code to verify your app

### 4. Configure Your App
After creating your app, you'll be taken to the app dashboard:

#### Authentication Settings
1. Under the "Auth" tab, add the following:
   - **Redirect URLs**: Add `http://localhost:8501` (for Streamlit)
   - **OAuth 2.0 scopes**: Add these scopes:
     - `r_liteprofile` (to read basic profile information)
     - `r_emailaddress` (to read email address)
     - `w_member_social` (to post content on behalf of the user)
     - `r_organization_admin` (to access company page data if needed)

#### Products
1. In the "Products" tab, request access to:
   - **Marketing Developer Platform** (for sharing content)
   - **Share on LinkedIn** (essential for posting)

### 5. Get Your Credentials
On the "Auth" tab, you'll find:
- **Client ID** (also called App ID or Consumer Key): `77o6mi0iq7k3j4`
- **Client Secret** (also called App Secret or Consumer Secret): You need to copy this from your app dashboard

These are the credentials you need to add to your `.env` file.

### 6. Update Your .env File
Update your [.env](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/.env) file with your actual client secret:

1. Go to your LinkedIn app dashboard
2. Navigate to the "Auth" tab
3. Copy your Client Secret (it will be hidden, click the eye icon to reveal it)
4. Replace `your_actual_client_secret_here` with your actual client secret in the [.env](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/.env) file:

```env
LINKEDIN_CLIENT_ID=77o6mi0iq7k3j4
LINKEDIN_CLIENT_SECRET=your_actual_client_secret_goes_here
LINKEDIN_REDIRECT_URI=http://localhost:8501
```

**Important Security Note**: Never share your Client Secret with anyone or commit it to version control. The [.env](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/.env) file is included in [.gitignore](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/.gitignore) to prevent accidental commits.

### 7. Configure OAuth Scopes
I can see you've successfully requested access to the "Share on LinkedIn" product, and the endpoints are now visible! This is great progress.

If the OAuth scopes are still not appearing in the interface, this is normal and can happen due to:

1. **Processing delay**: LinkedIn may still be processing your product access request
2. **Interface delay**: The UI sometimes takes time to update completely
3. **Cache issues**: Try refreshing the page or logging out and back in

To access the OAuth scopes:

1. Go back to the "Auth" tab in your LinkedIn app dashboard
2. Look for the "OAuth 2.0 scopes" section
3. If you don't see it immediately, try:
   - Refreshing the page
   - Waiting 10-15 minutes and checking again
   - Logging out of the LinkedIn Developer Portal and logging back in

The required OAuth scopes you need to add are:
- `r_liteprofile` (to read basic profile information)
- `r_emailaddress` (to read email address)
- `w_member_social` (to post content on behalf of the user)

### 8. Add Required OAuth Scopes
Once the scopes section appears:

1. In the OAuth 2.0 scopes section, you should see available scopes
2. Add the three scopes listed above
3. Save your changes

### 9. Test Your Integration
Run the test script to verify your LinkedIn API integration:

```bash
python scripts/test_linkedin_api.py
```

## Workaround: Client Credentials Flow (2-legged OAuth)

If you're experiencing delays with the standard OAuth scopes appearing, you can use LinkedIn's Client Credentials flow as a workaround. This flow is designed for accessing APIs that are not member-specific.

### How to Use Client Credentials Flow

1. **Ensure your app is verified** (which you've already done)
2. **Use the client credentials token** for non-member specific APIs

The Client Credentials flow allows you to generate an access token using only your Client ID and Client Secret, without requiring user authorization. This token can be used to access certain LinkedIn APIs that don't require member-specific information.

### Testing Client Credentials Flow

Run the dedicated test script for Client Credentials flow:

```bash
python scripts/test_linkedin_client_credentials.py
```

### When to Use Client Credentials Flow

Use the Client Credentials flow when:
- You need to access LinkedIn APIs that are not member-specific
- You're experiencing delays with OAuth scope approvals
- You want to access public data or perform app-specific operations

### Limitations of Client Credentials Flow

Note that the Client Credentials flow has limitations:
- Cannot access member-specific data (profile, connections, etc.)
- Cannot post on behalf of users
- Limited to specific API endpoints that don't require user context

## Important Notes

1. **Approval Process**: LinkedIn may require approval for some APIs, especially for posting content. This can take 1-2 business days.

2. **Rate Limits**: LinkedIn has strict rate limits. Be respectful of API usage.

3. **Privacy Compliance**: Make sure your app complies with LinkedIn's privacy policies and terms of service.

4. **Free Tier**: LinkedIn's API is free to use but has limitations compared to paid enterprise solutions.

## Troubleshooting

### Common Issues
1. **Authorization Error**: Make sure your redirect URL exactly matches what you registered
2. **Scope Not Approved**: Some scopes require LinkedIn's approval before use. You must first request access to the "Share on LinkedIn" product.
3. **Invalid Client ID/Secret**: Double-check that you copied the credentials correctly
4. **Missing Scopes Option**: If you don't see the OAuth scopes option, it's because:
   - LinkedIn is still processing your product access request (can take 10-15 minutes)
   - Try refreshing the page or logging out and back in
   - The scopes section will appear under the "Auth" tab once processing is complete
5. **Scopes Not Appearing After Product Approval**: 
   - This is normal and happens due to interface delays
   - Wait 10-15 minutes and refresh the page
   - Try logging out and back into the LinkedIn Developer Portal

### Getting Help
- Check the [LinkedIn Developer Documentation](https://docs.microsoft.com/en-us/linkedin/)
- Visit the [LinkedIn Developer Support](https://linkedin.zendesk.com/hc/en-us)
- Review your app settings in the developer portal

## Next Steps

After setting up your LinkedIn app:
1. Wait for the OAuth scopes section to appear in the "Auth" tab (10-15 minutes)
2. Add the required OAuth scopes (`r_liteprofile`, `r_emailaddress`, `w_member_social`)
3. Update your [.env](file:///C:/Users/tjd20.LAPTOP-PCMC2SUO/ASCEND%20GLOBAL%20VENTURES/FREE%20WORLD%20TRADE/.env) file with your actual client secret
4. Test the integration with the provided test script
5. Run your dashboard to see LinkedIn features in action
6. Begin posting content about Africa-USA agricultural trade opportunities
7. Monitor engagement and adjust your content strategy

This integration will help establish your presence as the #1 Africa-USA agriculture broker by sharing market intelligence and building professional connections.