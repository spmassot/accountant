CREATE TABLE IF NOT EXISTS givens_invoice_row (
	load_number TEXT,
	location TEXT,
	order_numbers TEXT,
	ship_date DATE,
	carrier TEXT,
	total MONEY,
	accrual MONEY,
	adjustment MONEY,
	company TEXT,
	line_of_business TEXT
)
