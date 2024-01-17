crypto:
1.
	- Import bnr certificate: keytool -import -alias bnr -keystore "C:\Program Files\Java\jdk-17.0.4.1\lib\security\cacerts" -file _.bnr.ro.crt
2.
	- FakeCA Private Key: openssl genrsa -out fakeCA.key 2048
	- FakeCA : openssl req -new -x509 -days 365 -key fake.key -out fakeCA.crt
	- Fake certificate key: openssl genrsa -out fake.key 2048
	- Fake certificate CSR: openssl req -new -key fake.key -out fake.csr
	- Sign fake certificate: openssl x509 -req -days 365 -in fake.csr -CA fakeCA.crt -CAkey fakeCA.key -set_serial <number> -out fake.crt
	- Import fake CA: keytool -import -alias fakeCA -file fakeCA.crt -keystore fake_keystore.jks -storepass changeit
	- Import fake certificate: 
	- Convert crt to pem: openssl x509 -in fake.crt -out pem/fake.pem -outform PEM
3.	
	- RootCA Private Key: openssl ecparam -name prime256v1 -genkey -out rootCA.key
	- RootCA certificate: openssl req -new -x509 -days 365 -key rootCA.key -out rootCA.crt
	- ServerCA Private Key: openssl ecparam -name prime256v1 -genkey -out serverCA.key
	- ClientCA Private Key: openssl ecparam -name prime256v1 -genkey -out clientCA.key
	- ServerCA CSR: openssl req -new -key serverCA.key -out serverCA.csr
	- ClientCA CSR: openssl req -new -key clientCA.key -out clientCA.csr
	- Sign ServerCA: openssl x509 -req -days 365 -in serverCA.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out serverCA.crt
	- Sign ClientCA: openssl x509 -req -days 365 -in clientCA.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out clientCA.crt
	- Convert crt to pem: 
						- openssl x509 -in serverCA.crt -out pem/serverCA.pem -outform PEM
						- openssl x509 -in clientCA.crt -out pem/clientCA.pem -outform PEM
						- openssl x509 -in rootCA.crt -out pem/rootCA.pem -outform PEM
4.
	- Client certificate key: openssl ecparam -name prime256v1 -genkey -out client.key
	- Client certificate CSR: openssl req -new -key client.key -out client.csr
	- Sign Client certificate: openssl x509 -req -days 365 -in client.csr -CA clientCA.crt -CAkey clientCA.key -set_serial <number> -out client.crt
	- Convert crt to pem: openssl x509 -in client.crt -out pem/client.pem -outform PEM
5.
	- Server certificate key: openssl genrsa -out server.key 2048
	- Server certificate CSR: openssl req -new -key server.key -out server.csr
	- Sign Server certificate: openssl x509 -req -days 365 -in server.csr -CA serverCA.crt -CAkey serverCA.key -set_serial <number> -out server.crt
	- Convert crt to pem: openssl x509 -in server.crt -out pem/server.pem -outform PEM
6. 
