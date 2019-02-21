CREATE TABLE IF NOT EXISTS freight_report (
  name TEXT,
  inserted_date DATE
);

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
);

CREATE TABLE IF NOT EXISTS givens_adjustment_row (
  load_number TEXT,
  location TEXT,
  order_numbers TEXT,
  ship_date DATE,
  carrier TEXT,
  total DECIMAL(12, 2),
  company TEXT,
  line_of_business TEXT
);

CREATE TABLE IF NOT EXISTS givens_invoice (
  name TEXT,
  inserted_date DATE
);

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
);

CREATE TABLE IF NOT EXISTS pick_ticket (
  pick_ticket TEXT,
  accrual DECIMAL(12, 2),
  adjustment DECIMAL(12, 2),
  paid DECIMAL(12, 2),
  released DECIMAL(12, 2),
  company TEXT,
  line_of_business TEXT
);

CREATE TABLE IF NOT EXISTS ups_invoice (
  name TEXT,
  inserted_date DATE
);

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
);
