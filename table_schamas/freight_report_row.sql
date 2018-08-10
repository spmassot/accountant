CREATE TABLE IF NOT EXISTS freight_report_row (
	month TEXT,
	year TEXT,
	pick_ticket TEXT,
	order_number TEXT,
	document_number TEXT,
	sales MONEY,
	cost MONEY,
	freight_sales MONEY,
	freight_cost MONEY,
	carrier_number TEXT,
	carrier TEXT,
	company TEXT,
	ship_date DATE,
	tracking_number TEXT,
	original_pick_ticket TEXT
)
