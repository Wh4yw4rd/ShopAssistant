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
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    transaction_id TEXT NOT NULL,
    transaction_code TEXT NOT NULL,
    transaction_timestamp TIMESTAMP NOT NULL,
    entry_mode TEXT NOT NULL,
    card_type TEXT,
    amount DECIMAL(8,2),
    refunded_amount DECIMAL(8,2),
    payment_type TEXT NOT NULL,
    status TEXT NOT NULL
);

-- Create sessions table
CREATE TABLE sessions(
    session_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    email TEXT,
    admin BOOLEAN DEFAULT FALSE,
    created_date TIMESTAMP DEFAULT NOW()
);