CREATE TABLE IF NOT EXISTS givens_invoice_row (
	load_number TEXT,
	location TEXT,
	order_numbers TEXT,
	ship_date DATE,
	carrier TEXT,
	total DECIMAL(12, 2),
	accrual DECIMAL(12, 2),
	adjustment DECIMAL(12, 2),
	company TEXT,
	line_of_business TEXT
)
