-- mysql-init/01-init.sql
CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY 'vdkfan5106';
GRANT ALL PRIVILEGES ON elementary_school_webapp.* TO 'root'@'%';
FLUSH PRIVILEGES;
