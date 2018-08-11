CREATE TABLE IF NOT EXISTS pick_ticket (
	pick_ticket TEXT UNIQUE,
	accrual DECIMAL(12, 2),
	adjustment DECIMAL(12, 2),
	paid DECIMAL(12, 2),
	released DECIMAL(12, 2),
	company TEXT,
	line_of_business TEXT
)
