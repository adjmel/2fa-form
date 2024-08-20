# Project Overview

## Overview

This project is a Django web application that provides a secure login and registration form. The application includes a Two-Factor Authentication (2FA) option to enhance connection security.

## Main Features

1. **Login Form**:
   - The application provides a simple form allowing users to log in with their username and password, but an account must be created first.

2. **Two-Factor Authentication (2FA)**:
   - **Optional**: Users have the option to enable Two-Factor Authentication (2FA) to add an extra layer of security to their account.
   - **Google Authenticator**: If 2FA is enabled, users can use the Google Authenticator app to generate OTP (One-Time Password) codes. A QR code is provided to set up Google Authenticator with their account.

3. **Containerization with Docker**:
   - The project is encapsulated in a Docker container, which simplifies deployment and management by ensuring a consistent and isolated environment.

4. **Reverse Proxy**:
   - A reverse proxy is configured to route traffic to the Docker container where the application is running. This allows for centralized traffic management and improved security.

5. **Access Port**:
   - The application is accessible locally on port 8003. In production, access is typically via a domain or IP address configured in the reverse proxy.

## Usage

To use the application:
1. **Access the Application**: Open your browser and go to [http://localhost:8003](http://localhost:8003) or the URL configured in the reverse proxy.
2. **Login**: Use the login form to enter your credentials.
3. **Enable 2FA**: Once logged in, you have the option to enable 2FA by following the instructions to set up Google Authenticator.

## Deployment

The project uses Docker to facilitate deployment. Here’s how to start the application:

```bash
docker compose up --build
```

![Capture d’écran 2024-08-20 à 19 34 24](https://github.com/user-attachments/assets/843694f4-913d-4931-a16f-d6c9e7638f98)
![Capture d’écran 2024-08-20 à 19 34 33](https://github.com/user-attachments/assets/75c162e6-038a-4544-8ac5-80661eb57163)
![Capture d’écran 2024-08-20 à 19 35 16](https://github.com/user-attachments/assets/0529a4fa-bf3d-4f4e-9eb9-5e60d272a4cd)
![Capture d’écran 2024-08-20 à 19 36 12](https://github.com/user-attachments/assets/ba0b6ee1-dc55-4cb1-89d1-64aa1e8bee28)
![Capture d’écran 2024-08-20 à 19 35 33](https://github.com/user-attachments/assets/a13c6640-fed6-4bdb-aaed-bd9525daa400)

