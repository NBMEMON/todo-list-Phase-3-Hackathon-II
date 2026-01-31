---
id: 1-fix-user-registration-error
title: Fix User Registration Error
stage: red
date: 2026-01-12
surface: agent
model: Claude Sonnet 4
feature: auth
branch: main
user: User
command: sp.analyze
labels:
  - bugfix
  - auth
  - registration
files:
  - backend/models/user.py
tests: []
links:
  - spec: null
  - ticket: null
  - adr: null
  - pr: null
---

# Fix User Registration Error

## Summary
Fixed the user registration error "UserCreate object has no field password_hash" that was occurring when creating new accounts.

## Root Cause
The issue was in the UserCreate model in `backend/models/user.py`. The model was missing the `password_hash` field definition, but the `hash_password()` method was dynamically adding it. When the registration endpoint tried to access `user_create_data.password_hash` to create the User object, it was failing because the field wasn't properly defined in the model.

## Solution
Added the `password_hash` field to the UserCreate model definition:

```python
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)
    password_hash: Optional[str] = Field(default=None, min_length=1)  # Added this field

    def hash_password(self):
        """Hash the password before storing"""
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        self.password_hash = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # Clear plain text passwords after hashing
        delattr(self, 'password')
        delattr(self, 'confirm_password')
```

## Verification
- Tested the registration endpoint with a new user and confirmed it now works correctly
- The endpoint returns 200 status with access and refresh tokens
- Proper error handling still works for duplicate emails and mismatched passwords

## Files Changed
- `backend/models/user.py` - Added password_hash field to UserCreate model

## Outcome
The registration form now works correctly without throwing the "UserCreate object has no field password_hash" error. Users can successfully create new accounts and receive JWT tokens for authentication.