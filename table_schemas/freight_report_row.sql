CREATE TABLE IF NOT EXISTS freight_report_row (
	month TEXT,
	year TEXT,
	pick_ticket TEXT,
	order_number TEXT,
	document_number TEXT,
	sales DECIMAL(12, 2),
	cost DECIMAL(12, 2),
	freight_sales DECIMAL(12, 2),
	freight_cost DECIMAL(12, 2),
	carrier_number TEXT,
	carrier TEXT,
	company TEXT,
	ship_date DATE,
	tracking_number TEXT,
	original_pick_ticket TEXT
)
