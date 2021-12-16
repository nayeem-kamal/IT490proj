CREATE TABLE `Accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `account_number` varchar(12) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `balance` float DEFAULT '0',
  `account_type` varchar(255) DEFAULT 'Bitcoin',
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified` datetime DEFAULT NULL,
  `closed` tinyint DEFAULT '0',
  `freeze` tinyint DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_number` (`account_number`),
  KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `source` int NOT NULL,
  `destination` int NOT NULL,
  `totalCost` float NOT NULL,
  `transactionType` varchar(255) DEFAULT NULL,
  `recentTrades` varchar(255) DEFAULT NULL,
  `intitialCost` float NOT NULL,
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `source` (`source`),
  KEY `destination` (`destination`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `firstName` varchar(45) DEFAULT NULL,
  `lastName` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `Accounts` (
  `id` int auto_increment,
  `username` varchar(255) DEFAULT NULL,
  `balance` float DEFAULT '0',
  `account_type` varchar(255) DEFAULT 'Bitcoin',
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified` datetime DEFAULT NULL,
  `closed` tinyint DEFAULT '0',
  `freeze` tinyint DEFAULT '0',
  PRIMARY KEY (`id`)
);

