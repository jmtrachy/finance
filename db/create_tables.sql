CREATE TABLE IF NOT EXISTS `equity_snapshot` (
  `snapshot_id` INT AUTO_INCREMENT NOT NULL,
  `ticker` VARCHAR(10) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `exchange` VARCHAR(10) NOT NULL,
  `date` DATE NOT NULL,
  `price` FLOAT(10,4) NOT NULL,
  `price_change` FLOAT(10,4) NOT NULL,
  `price_change_percent` FLOAT(10,4) NOT NULL,
  PRIMARY KEY (`snapshot_id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_bin

CREATE VIEW fifty_day_moving_average AS
SELECT `ticker`, AVG(`price`) AS average_price
  FROM `equity_snapshot`
 WHERE `date` BETWEEN DATE_SUB(NOW(), INTERVAL 50 DAY) AND NOW()
 GROUP BY `ticker`;

CREATE VIEW fifty_day_volatility_average AS
SELECT `ticker`, AVG(ABS(`price_change_percent`)) AS volatility_average
  FROM `equity_snapshot`
 WHERE `date` BETWEEN DATE_SUB(NOW(), INTERVAL 50 DAY) AND NOW()
   AND `price_change_percent` IS NOT NULL
 GROUP BY `ticker`;

CREATE VIEW fifty_day_averages AS
SELECT DISTINCT(es.`ticker`), moving_avg.average_price, volatility.volatility_average
  FROM fifty_day_moving_average moving_avg
  JOIN fifty_day_volatility_average volatility ON moving_avg.`ticker` = volatility.`ticker`
  JOIN `equity_snapshot` es ON es.`ticker` = moving_avg.`ticker`;
