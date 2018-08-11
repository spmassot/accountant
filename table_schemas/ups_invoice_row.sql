CREATE TABLE IF NOT EXISTS ups_invoice_row (
	recipient_number TEXT,
	account_number TEXT,
	invoice_date DATE,
	invoice_number TEXT,
	invoice_amount TEXT,
	transaction_date DATE,
	lead_shipment_number TEXT,
	shipment_reference_number_1 TEXT,
	shipment_reference_number_2 TEXT,
	tracking_number TEXT,
	package_reference_number_1 TEXT,
	package_reference_number_2 TEXT,
	package_reference_number_3 TEXT,
	package_reference_number_4 TEXT,
	package_reference_number_5 TEXT,
	net_amount DECIMAL(12, 2)
)
