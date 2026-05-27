from ponika import PonikaClient


connection = PonikaClient(
    host='192.168.178.1',
    username='admin',
    password='admin01',
    # Optional, default is True, but often there no valid certificate
    verify_tls=False,
)
