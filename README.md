# Config > Policy
## Scope: Authentication
- `challenge_response`: totp
- `otppin`: userstore
- `passthru`: userstore

## Scope: Enrollment
- `tokenissuer`: {user}
- `tokenlabel`: {serial}

## Scope: WebUI
- `default_tokentype`: totp
- `login_mode`: userstore
- `tokenwizard`
- `user_details`

## Scope: User
- `Turn on all of group token`
- `totp_hashlib`: sha1 (more complex hashing function not working if using another app to scan QR code OTP instead of PrivacyIDEA)
- `totp_otplen`: 6
- `totp_timestep`: 30
- `updateuser`
- `enrollTOTP`

## Scope: Authorization
- `add_resolver_in_response` (for API endpoint `/validate/check`)
- `add_user_in_response` (for API endpoint `/validate/check`)
- `api_key_required`

## Creating a Token

To create a token using `pi-manage`, use the following commands:

```sh
pi-manage api createtoken -r admin -d 3650 -u admin
pi-manage api createtoken -r validate -d 3650 -u admin
```
`After create token, add it into /backend/.env. Then reboot server`

# Config > Users
## Add New Resolver
- `In this situation, MySQL was chosen to store user data.`
- `Below this page, configure mapping to your table and database. Then set the default realm or merge (It's up to you).`

# Note
> This is a simple test of FastAPI combined with OAuth2 and integrated with PrivacyIDEA (for 2FA).  
> PrivacyIDEA (PI) has a large number of functions; my project uses only a small part of PI, and its objective is just for testing. (PrivacyIDEA + KeyCloak/ is a popular approach.)
> In database accounts and users were created but can't login immediately cuz PI has a special encryption mechanism to secure user passwords, an extra customized endpoint is needed to insert user information into both the Account and Person tables.
> PrivacyIDEA web login __[https://10.128.0.23/](https://10.128.0.23/)__ **(user: admin; password: 123)**

# Tools, Libraries, and Open Source Used
- `PrivacyIDEA for 2FA`
- `FastAPI OAuth2`
- `Vagrant for creating the initial environment and automating the app`
- `Ubuntu Server`
- `MySQL`
- `Redis (just used a library for rate limiting)`
- `Docker to containerize the application`

# References
> [PrivacyIDEA](https://privacyidea.readthedocs.io/en/latest/index.html)