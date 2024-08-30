from twilio.rest import Client

whatsapp_number = "+14155238886"

def send_whatsapp_message(numbers: list, message: str, account_sid: str, auth_token: str):
    """
    Sends a WhatsApp message to multiple numbers simultaneously.
 
    Parameters:
    - numbers: list
        List of phone numbers to send the message to.
    - message: str
        The content of the message to be sent.
    - account_sid: str
        The Account SID for your Twilio account.
    - auth_token: str
        The Auth Token for your Twilio account.
 
    Returns:
    - int:
        The number of messages successfully sent.
 
    Raises:
    - ValueError:
        Raises an error if the length of the numbers list is not equal to 50.
    """
 
    # Checking if the length of the numbers list is equal to 50
    if len(numbers) > 50:
        raise ValueError("The numbers list should contain no more than 50 numbers.")
 
    # Creating a Twilio client using the account SID and auth token
    client = Client(account_sid, auth_token)
 
    # Counter for tracking the number of successfully sent messages
    sent_count = 0
 
    # Sending the message to each number in the list
    for number in numbers:
        try:
            # Sending the WhatsApp message using the Twilio client
            message = client.messages.create(
                body=message,
                from_=f'whatsapp:{whatsapp_number}',
                to=f'whatsapp:{number}'
            )
            sent_count += 1
        except Exception as e:
            print(f"Error sending message to {number}: {str(e)}")
 
    return sent_count
 
# Example usage of the send_whatsapp_message function:
 
# Define the list of numbers to send the message to
numbers = [
    "+14079634058",
    # Add more numbers here...
]
 
# Define the content of the message to be sent
message = "Hello! This is an automated message sent to multiple recipients."
 
# Set your Twilio account SID and auth token
account_sid = "ACc818fade4f5e7b299da59bd66ab30ff4"
auth_token = "7661ddbf69c39be33db049ad700eebb3"
 
try:
    # Send the WhatsApp message to the numbers
    sent_count = send_whatsapp_message(numbers, message, account_sid, auth_token)
    print(f"Successfully sent {sent_count} messages.")
except ValueError as e:
    print(f"Error: {str(e)}")