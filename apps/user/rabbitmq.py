from config.rabbit import Rabbit


class RabbitSmsOtp(Rabbit):
    _exchange = 'sms_otp'
    _route = 'sms_otp'
    _queue_name = 'sms_otp'


class RabbitEmailOtp(Rabbit):
    _exchange = 'email_otp'
    _route = 'email_otp'
    _queue_name = 'email_otp'
