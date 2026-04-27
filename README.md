# 🔐 Secure Web App with Microsoft Entra ID

This project implements a secure web application using **Microsoft Entra ID (Azure AD)** and **OpenID Connect** for authentication.

Users can:
- sign in with their Microsoft account
- view their profile
- update limited profile fields via Microsoft Graph API

The app is deployed on a public Ubuntu server with HTTPS.

---

## 🧠 Authentication

The system uses **OAuth 2.0 + OpenID Connect** with **Authorization Code Flow (PKCE)**:

1. User is redirected to Microsoft login  
2. After authentication, an authorization code is returned  
3. The code is exchanged for:
   - **ID Token** (identity)
   - **Access Token** (API access)

---

## 🪪 JWT Tokens

Authentication relies on **JSON Web Tokens (JWT)**:

- Header → algorithm  
- Payload → user data  
- Signature → verification  

---

## 🔑 Scopes

- `User.Read` → read user profile  
- `User.ReadBasic.All` → list users  
- `User.ReadWrite` → update allowed fields  

Some updates require admin privileges and are restricted.

---

## ⚙️ Tech Stack

- Python, Flask  
- MSAL (authentication)  
- Microsoft Graph API  
- Nginx (reverse proxy)  
- Ubuntu VM  

---

## 🔒 Security

- HTTPS via **Let’s Encrypt**  
- TLS encryption (1.2/1.3)  
- Protected routes require login  
- Session-based authentication  

The app handled real-world traffic such as scanning and malformed requests without exposing vulnerabilities.

---

## 📊 Features

- Secure login/logout  
- View user profile (`/profile`)  
- Update phone number  
- Retrieve tenant users (`/users`)  

---

## 🚀 Deployment

Live at: https://ami089.x310.net

---

## 🧩 Summary

- OpenID Connect authentication with Microsoft Entra ID  
- Secure token handling (JWT, OAuth2)  
- Integration with Microsoft Graph API  
- Production deployment with HTTPS and basic security protections  