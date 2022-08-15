from twilio.rest import Client
import uuid

# Remember to add credidentials to enviroment(os) at PRODUCTION

"""
	AUTHENTICATION
	1. Send OTP
	2. Verify OTP
	3. Resend new OTP after 60 seconds if none is gotten
"""

def send_otp(recepient):
	account_sid = ""
	auth_token = ""
	client = Client(account_sid, auth_token)

	verification = client.verify \
						.v2 \
						.services("") \
						.verifications \
						.create(to="+" + recepient, channel='sms')

	status = { "message" : "" }
	if verification.status == "pending":
		status["message"] = "sent"
	else:
		status["message"] = verification.status
	return status

def verify_otp (recepient, v_code):
	account_sid = ""
	auth_token = ""
	client = Client(account_sid, auth_token)

	verification_check = client.verify \
							.v2 \
							.services("") \
							.verification_checks \
							.create(to="+" + recepient, code=v_code)

	status = {"message": ""}
	status["message"] = verification_check.status
	return status

def resend_otp(recepient):
	account_sid = ""
	auth_token = ""
	client = Client(account_sid, auth_token)

	verification = client.verify \
						.v2 \
						.services("") \
						.verifications("+" + recepient) \
						.update(status='canceled')

	# Resend
	send_otp(recepient)


def generate_username():
    code = str(uuid.uuid4()).replace("-", "")[:6]
    return code
