-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: financials
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `financials`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `financials` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `financials`;

--
-- Table structure for table `expense_details`
--

DROP TABLE IF EXISTS `expense_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expense_details` (
  `expenseId` int NOT NULL AUTO_INCREMENT,
  `incomeId` int NOT NULL,
  `expenseName` varchar(25) NOT NULL,
  PRIMARY KEY (`expenseId`),
  KEY `expense_to_income_pointer_idx` (`incomeId`),
  CONSTRAINT `expense_to_income_pointer` FOREIGN KEY (`incomeId`) REFERENCES `income_details` (`incomeId`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expense_details`
--

LOCK TABLES `expense_details` WRITE;
/*!40000 ALTER TABLE `expense_details` DISABLE KEYS */;
INSERT INTO `expense_details` VALUES (1,1,'Haircut'),(2,1,'Shirt'),(3,1,'Jeans'),(4,1,'Shoes'),(5,1,'dad-custom');
/*!40000 ALTER TABLE `expense_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expenses`
--

DROP TABLE IF EXISTS `expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expenses` (
  `dateStr` varchar(10) NOT NULL,
  `expenseId` int NOT NULL,
  `price` int NOT NULL,
  `optionalDescription` varchar(150) DEFAULT NULL,
  KEY `exp_id` (`expenseId`),
  CONSTRAINT `exp_id` FOREIGN KEY (`expenseId`) REFERENCES `expense_details` (`expenseId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expenses`
--

LOCK TABLES `expenses` WRITE;
/*!40000 ALTER TABLE `expenses` DISABLE KEYS */;
INSERT INTO `expenses` VALUES ('2-8-2019',1,50,NULL),('19-9-2019',2,120,NULL),('22-9-2019',2,50,NULL),('27-9-2019',1,50,NULL),('29-7-2019',4,315,'White Nike Air Force'),('4-10-2019',2,50,'NULL'),('29-10-2019',3,290,'NULL'),('1-11-2019',1,50,'NULL'),('8-11-2019',3,225,'NULL'),('17-11-2019',2,25,'NULL'),('12-12-2019',1,50,'NULL'),('14-12-2019',1,50,'NULL'),('12-1-2020',5,75,'Passport renew'),('5-2-2020',3,400,'NULL'),('6-2-2020',1,50,'NULL');
/*!40000 ALTER TABLE `expenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `income_details`
--

DROP TABLE IF EXISTS `income_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `income_details` (
  `incomeId` int NOT NULL AUTO_INCREMENT,
  `incomeName` varchar(25) NOT NULL,
  PRIMARY KEY (`incomeId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `income_details`
--

LOCK TABLES `income_details` WRITE;
/*!40000 ALTER TABLE `income_details` DISABLE KEYS */;
INSERT INTO `income_details` VALUES (1,'from_dad');
/*!40000 ALTER TABLE `income_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `incomes`
--

DROP TABLE IF EXISTS `incomes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `incomes` (
  `dateStr` varchar(10) NOT NULL,
  `incomeId` int NOT NULL,
  `amount` int NOT NULL,
  `optionalDescription` varchar(150) DEFAULT NULL,
  KEY `income_to_income_type_pointer_idx` (`incomeId`) /*!80000 INVISIBLE */,
  CONSTRAINT `income_to_income_type_pointer` FOREIGN KEY (`incomeId`) REFERENCES `income_details` (`incomeId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incomes`
--

LOCK TABLES `incomes` WRITE;
/*!40000 ALTER TABLE `incomes` DISABLE KEYS */;
INSERT INTO `incomes` VALUES ('2-7-2019',1,500,NULL),('2-8-2019',1,500,NULL),('28-8-2019',1,500,NULL),('2-10-2019',1,500,NULL),('3-11-2019',1,500,NULL),('1-12-2019',1,500,NULL),('1-1-2020',1,500,NULL);
/*!40000 ALTER TABLE `incomes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-11  0:07:26
