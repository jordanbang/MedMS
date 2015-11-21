import twilio.twiml
from twilio.rest import TwilioRestClient


class SmsService(object):

    ACCOUNT_SID = 'ACf3e25484f8b36cd1af3542308c5b735c'
    AUTH_TOKEN = '52b566ccba89ebfb61a549f32db43410'
    NUMBER = '+16476938595'

    def __init__(self):
        self.client = TwilioRestClient(self.ACCOUNT_SID, self.AUTH_TOKEN)

    @staticmethod
    def reply_to_message():
        resp = twilio.twiml.Response()
        resp.message('Thank you for reaching out to MedMS we will try to connect you to a doctor as soon as possible.')
        return resp

    def send_new_message(self, body, recepients):
        failed_messages = {}
        for recepient in recepients:
            try:
                message = self.client.messages.create(to=recepient, from_=self.NUMBER, body=body)
            except Exception as e:
                failed_messages[recepient] = str(e)

        return failed_messages


if __name__ == '__main__':
    sms_sender = SmsService()
    sms_sender.send_new_message('This is a test', ['4169488810', '+14162768158', '16472359220'])
