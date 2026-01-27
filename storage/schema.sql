-- Create users table
CREATE TABLE users (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT,
    admin BOOLEAN DEFAULT FALSE,
    created_date DATE DEFAULT NOW(),
    CONSTRAINT unique_name UNIQUE (name)
);

-- Create transactions table
CREATE TABLE transactions (
    transaction_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    transaction_code TEXT NOT NULL,
    entry_mode TEXT NOT NULL,
    transaction_date TIMESTAMP NOT NULL,
    amount DECIMAL(8,2) NOT NULL,
    payment_type TEXT NOT NULL,
    status TEXT NOT NULL,
    CONSTRAINT unique_transaction_code UNIQUE (transaction_code)
);