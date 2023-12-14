# Step-by-Step Guide 

### Prerequisites

Before starting, ensure you have the following:

1. **Meta Developer Account:** Create a Meta developer account [here](https://developers.facebook.com/).

2. **Business App:** Have a business app. Learn to create one [here](https://developers.facebook.com/docs/development/create-an-app/). If the option is not visible, choose Other > Next > Business.

3. **Python Knowledge:** Basic familiarity with Python is required for this tutorial.

### Step 1: Select Phone Numbers

1. Ensure WhatsApp is added to your App.
2. Start with a test number for sending messages to up to 5 numbers.
3. Go to API Setup and locate the test number for sending messages.
4. Add numbers to send messages to, including your own WhatsApp number.
5. Receive a code on your phone via WhatsApp to verify your number.

### Step 2: Send Messages with the API

1. Obtain a 24-hour access token from the API access section.
2. Use the provided example curl command to send messages (can be done via terminal or tools like Postman).
3. Convert the curl command into a Python function using the request library.
4. Create a .env file based on sample.env and update the required variables.
5. Receive a "Hello World" message (Expect a 10-20 second delay for the message).

### Required Information for Environment variables 

Before continuing, gather the following information from the App Dashboard:

- APP_ID: "<YOUR-WHATSAPP-BUSINESS-APP_ID>" (Found at App Dashboard)
- APP_SECRET: "<YOUR-WHATSAPP-BUSINESS-APP_SECRET>" (Found at App Dashboard)
- VERSION: "v18.0" (The latest version of the Meta Graph API)
- ACCESS_TOKEN: "" (Created in the previous step)
- PHONE_NUMBER_ID: "" (ID for your phone number)
- VERIFY_TOKEN: "" (Token for verifying your phone number)

Note: The first message to a user must be a template type message; hence, send a reply first before proceeding.

### Step 3: Configure Webhooks to Receive Messages

**Note: This is a crucial step in the tutorial.**

1. Start your app.
2. Ensure you have Python installed and install the requirements: `pip install -r requirements.txt`.
3. Run your FastaPI app locally by executing `main.py`.
4. Launch ngrok.
    - If you're not using ngrok yet, sign up for ngrok [here](https://ngrok.com/docs/integrations/whatsapp/webhooks/).
    - Download the ngrok agent.
    - Go to the ngrok dashboard, click "Your Authtoken," and copy your Authtoken.
    - Authenticate your ngrok agent using the instructions provided.
    - On the left menu, expand "Cloud Edge," then click "Domains."
    - Click "+ Create Domain" or "+ New Domain" to create a static ngrok domain.
    - Start ngrok by running the following command in a terminal on your local desktop:
      ```bash
      ngrok http 8000 --domain your-domain.ngrok-free.app
      ```
      Copy the URL displayed by ngrok for later use.

5. Integrate WhatsApp.
    - In the Meta App Dashboard, go to WhatsApp > Configuration and click "Edit."
    - In the Edit webhook's callback URL popup, enter the ngrok URL with /webhook at the end (e.g., https://example.ngrok-free.app/webhook).
    - Set a verification token (update in your VERIFY_TOKEN environment variable).
    - After adding the webhook, Meta will send a validation post request to your ngrok-exposed application. Confirm receipt in your terminal with "Successfully verify the token."
    - Back to the Configuration page, click "Manage."
    - On the Webhook fields popup, click "Subscribe to the messages" field.

6. Testing the Integration
    - Use the phone number associated with your WhatsApp product or the test number copied earlier.
    - Add this number to your WhatsApp app contacts and send a message.
    - Confirm your localhost app receives the message and logs both headers and body in the terminal.
    - Test if the bot replies back in uppercase.

Congratulations! You have successfully integrated the bot. 🎉 Now, it's time to build exciting things with it.