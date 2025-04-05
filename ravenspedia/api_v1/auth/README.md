To create certificates for the JWT release, please follow these steps:

1. Create a new folder named `certs` in the `./ravenspedia/` directory.
2. Open the terminal and navigate to the `./ravenspedia/certs` folder.
3. Execute the following commands:

```shell
# Generate an RSA private key, of size 2048
openssl genrsa -out jwt-private.pem 2048
```

```shell
# Extract the public key from the key pair, which can be used in a certificate
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```
