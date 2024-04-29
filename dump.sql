-- MySQL dump 10.13  Distrib 8.3.0, for Win64 (x86_64)
--
-- Host: localhost    Database: warehouse
-- ------------------------------------------------------
-- Server version	8.3.0

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
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `location_id` int NOT NULL,
  `quantity` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `location_id` (`location_id`),
  CONSTRAINT `inventory_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`),
  CONSTRAINT `inventory_ibfk_2` FOREIGN KEY (`location_id`) REFERENCES `location` (`id`),
  CONSTRAINT `inventory_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory`
--

LOCK TABLES `inventory` WRITE;
/*!40000 ALTER TABLE `inventory` DISABLE KEYS */;
INSERT INTO `inventory` VALUES (1,2,2,231),(2,2,3,78),(3,2,5,134),(4,12,5,567),(5,12,1,423),(6,12,2,456),(7,12,3,678),(8,12,4,264),(9,12,6,456),(10,12,7,244),(11,12,8,31),(12,12,9,2),(13,12,10,133),(14,10,2,15),(15,10,3,12),(16,10,1,0),(17,11,1,34),(18,11,5,24),(19,11,8,42),(20,11,9,0),(21,11,3,687),(22,3,2,412),(24,3,3,395),(25,3,7,65),(26,3,10,0),(27,4,6,0),(28,4,2,116),(29,4,3,178),(30,4,1,69),(31,4,4,16),(32,4,5,2),(33,4,7,0),(34,4,10,65),(35,13,1,674),(36,13,2,4234),(37,13,3,5553),(38,13,4,3455),(39,13,5,678),(40,13,6,678),(41,13,7,34),(42,13,8,0),(43,13,9,67),(44,13,10,0),(45,1,10,0),(46,1,1,0),(47,1,2,0),(48,1,3,0),(49,1,4,0),(50,1,5,0),(51,1,6,0),(52,1,7,0),(53,1,8,0),(54,1,9,0),(55,5,1,134),(56,5,3,87),(57,5,2,123),(58,5,7,34),(59,6,3,41),(60,6,2,54),(61,6,5,0),(62,6,9,24),(63,7,6,3),(64,8,10,0),(65,9,10,0),(66,9,3,0),(67,9,1,0),(68,9,2,1),(69,9,4,0),(70,9,5,0),(71,9,6,0),(72,9,7,0),(73,9,8,0),(74,9,9,0),(75,7,1,3);
/*!40000 ALTER TABLE `inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `location` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location`
--

LOCK TABLES `location` WRITE;
/*!40000 ALTER TABLE `location` DISABLE KEYS */;
INSERT INTO `location` VALUES (1,'Ижевск'),(2,'Москва'),(3,'Санкт-Петербург'),(4,'Новосибирск'),(5,'Краснодар'),(6,'Екатеринбург'),(7,'Казань'),(8,'Омск'),(9,'Воронеж'),(10,'Владивосток');
/*!40000 ALTER TABLE `location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `price` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'NVIDIA GeForce RTX 4090','Видеокарта',200000),(2,'NVIDIA GeForce RTX 4080','Видеокарта',150000),(3,'NVIDIA GeForce RTX 4070','Видеокарта',100000),(4,'AMD Radeon RX 6900 XT','Видеокарта',60000),(5,'AMD Radeon RX 7900 XT','Видеокарта',80000),(6,'AMD Radeon RX 7700 XT','Видеокарта',70000),(7,'AMD Radeon RX 7600 XT','Видеокарта',60000),(8,'AMD Ryzen 7 7800X3D','Процессор',43000),(9,'AMD Ryzen 9 7950X3D','Процессор',80000),(10,'Intel Core i9-14900K','Процессор',70000),(11,'Intel Core i7-14700K','Процессор',50000),(12,'NVIDIA GeForce RTX 3060','Видеокарта',30000),(13,'AMD Ryzen 5 5600X','Процессор',10000),(14,'NVIDIA GeForce RTX 5090','Видеокарта',500000);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-29  6:03:23
