CREATE TABLE IF NOT EXISTS pick_ticket (
	pick_ticket TEXT PRIMARY KEY,
	accrual MONEY,
	adjustment MONEY,
	paid MONEY,
	released MONEY,
	company TEXT,
	line_of_business TEXT
)
