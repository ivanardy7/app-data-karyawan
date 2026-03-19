CREATE DATABASE database_karyawan;
USE database_karyawan;

CREATE TABLE employees (
  employee_id INT AUTO_INCREMENT PRIMARY KEY,
  full_name   VARCHAR(100) NOT NULL,
  department  VARCHAR(50)  NOT NULL,
  age         INT          NOT NULL,
  salary      INT          NOT NULL,
  join_date   DATE         NOT NULL,
  status      ENUM('active','resigned') NOT NULL DEFAULT 'active'
);

INSERT INTO employees (full_name, department, age, salary, join_date, status) VALUES
('Andi Saputra', 'Production', 29, 8500000, '2022-03-14', 'active'),
('Bunga Lestari', 'HR', 31, 9500000, '2021-07-01', 'active'),
('Citra Wulandari', 'Finance', 27, 8000000, '2023-01-10', 'active'),
('Dimas Pratama', 'IT', 25, 10000000, '2022-11-21', 'active'),
('Eka Putri', 'Production', 35, 12000000, '2020-05-30', 'active'),
('Fajar Hidayat', 'Sales', 28, 7800000, '2023-09-18', 'active'),
('Gita Ananda', 'HR', 26, 7200000, '2024-02-12', 'active'),
('Hendra Wijaya', 'IT', 33, 15000000, '2019-08-05', 'active'),
('Intan Maharani', 'Finance', 30, 11000000, '2020-10-20', 'resigned'),
('Joko Santoso', 'Sales', 24, 6500000, '2024-06-01', 'active'),
('Kiki Amelia', 'Production', 22, 6700000, '2024-05-10', 'active'),
('Luthfi Hakim', 'IT', 29, 13500000, '2021-11-01', 'active'),
('Maya Safira', 'Sales', 31, 7200000, '2023-02-15', 'active'),
('Naufal Rizky', 'HR', 26, 8800000, '2024-01-20', 'active'),
('Olivia Putri', 'Finance', 34, 11500000, '2020-08-12', 'active');