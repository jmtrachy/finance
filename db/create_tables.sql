CREATE TABLE IF NOT EXISTS `equity_snapshot` (
  `snapshot_id` INT AUTO_INCREMENT NOT NULL,
  `ticker` VARCHAR(10) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `exchange` VARCHAR(10) NOT NULL,
  `date` DATE NOT NULL,
  `price` FLOAT(10,4) NOT NULL,
  PRIMARY KEY (`snapshot_id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_bin
