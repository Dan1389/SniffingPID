from ftplib import FTP_TLS

source = '/home/pi/Desktop/RaspiFy/Enviroment/serviceAux.txt'
destiny = './serviceAux.txt'

with FTP_TLS() as ftps:
  ftps.connect(192.168.10.104, port)
  ftps.sendcmd("pi")
  ftps.sendcmd("raspberry")

  with ftps as conn:
    with open(destiny, 'wb') as file:
      conn.retrbinary(f'RETR { source }', file.write)