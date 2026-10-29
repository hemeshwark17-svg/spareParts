CREATE DATABASE IF NOT EXISTS vehicle_spares;
USE vehicle_spares;

CREATE TABLE IF NOT EXISTS spare_parts (
  part_id INT AUTO_INCREMENT PRIMARY KEY,
  part_number VARCHAR(40) NOT NULL UNIQUE,
  part_name VARCHAR(120) NOT NULL,
  category VARCHAR(60) NOT NULL DEFAULT 'Other',
  vehicle_compatibility VARCHAR(160) NOT NULL DEFAULT 'Multiple models',
  price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  stock_quantity INT NOT NULL DEFAULT 0,
  supplier_name VARCHAR(120) NOT NULL DEFAULT 'Demo Supplier',
  description TEXT,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CHECK (price >= 0),
  CHECK (stock_quantity >= 0)
);

INSERT INTO spare_parts
(part_number,part_name,category,vehicle_compatibility,price,stock_quantity,supplier_name,description)
VALUES
('BRK-001','Brake Pad Set','Brakes','Demo sedan models',1250.00,12,'Demo Auto Supplies','Sample project inventory item.'),
('FLT-002','Engine Oil Filter','Filters','Multiple demo models',350.00,25,'Demo Auto Supplies','Sample project inventory item.'),
('LGT-003','Headlight Bulb','Electrical','Common 12V vehicles',220.00,18,'City Parts Demo','Sample project inventory item.'),
('MIR-004','Side Mirror','Body Parts','Demo hatchback models',780.00,6,'City Parts Demo','Sample project inventory item.')
ON DUPLICATE KEY UPDATE part_name=VALUES(part_name);
