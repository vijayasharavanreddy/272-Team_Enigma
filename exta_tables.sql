-- MySQL dump 10.13  Distrib 8.1.0, for macos14.0 (arm64)
--
-- Host: localhost    Database: employees
-- ------------------------------------------------------
-- Server version	8.1.0

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
-- Table structure for table `hr_user`
--

DROP TABLE IF EXISTS `hr_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `first_name` varchar(80) NOT NULL,
  `last_name` varchar(80) NOT NULL,
  `address` varchar(200) DEFAULT NULL,
  `email` varchar(120) NOT NULL,
  `mobile_number` varchar(20) NOT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `role` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `mobile_number` (`mobile_number`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_user`
--

LOCK TABLES `hr_user` WRITE;
/*!40000 ALTER TABLE `hr_user` DISABLE KEYS */;
INSERT INTO `hr_user` VALUES (1,'shiva','Shiva','Vardhineedi','101 e san fernando st, Unit 145, 101 san fernando apt','sivaswaroop.vardhineedi@sjsu.edu','4084837703','$2b$12$8ZuNnexNjECHN7DegYgQBe6woy8msq.sFBUY8aXkAx1JBTzHbgixm','hr'),(2,'charan','Sree Charan','Mallu','101 e san fernando st, Unit 145, 101 san fernando apt','sreecharanmallu04@gmail.com','14084837704','$2b$12$8Ez19TXfz7AN1zApgO3KSu1akjBreiWS2RvmFUaaF8Po9YjCoG47K','hr'),(3,'chandu','Chandu','Gorle','101 e san fernando st','chandu.gorle@sjsu.edu','4084837704','$2b$12$JOQs7iqx5lu5Cmrw369V4.IsZuPZvPk2XiRCtXdtv.23AJIr80vyW','manager'),(4,'kakashi','kakashi','hatake','101 e san fernando st','kaakshi.hataki@gmail.com','9490192369','$2b$12$vP2I2gQf/ZroqEQudLePr.RlaM1.aukaghWdnBgwHqp0riKud6bKC','employee'),(6,'siddu','siddu','roy','145, 101 san fernando apartment','siddu.roy@gmail.com','1767666653','$2b$12$KD1BPD5jqUAt9MC2N2RBC.CpqeaW9pBCTOJe5bo2IiEvXril1EUt6','employee');
/*!40000 ALTER TABLE `hr_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hr_request`
--

DROP TABLE IF EXISTS `hr_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hr_request` (
  `req_type` varchar(10) NOT NULL,
  `first_name` varchar(14) NOT NULL,
  `last_name` varchar(16) NOT NULL,
  `hire_date` date DEFAULT NULL,
  `dept_no` char(4) NOT NULL,
  `manager_no` int DEFAULT NULL,
  `title` varchar(50) DEFAULT NULL,
  `salary` int DEFAULT NULL,
  `hire_status` int NOT NULL,
  PRIMARY KEY (`req_type`,`first_name`,`last_name`,`hire_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hr_request`
--

LOCK TABLES `hr_request` WRITE;
/*!40000 ALTER TABLE `hr_request` DISABLE KEYS */;
INSERT INTO `hr_request` VALUES ('newhire','bharat','venna','2023-12-06','dYQA',301874,'junior developer',50000,1),('newhire','kakashi','hatake','2023-12-04','dYQA',301874,'hokage',50000,1),('newhire','naruto','uzumaki','2023-12-05','dYQA',301874,'jonin',50000,1),('newhire','naruto','uzumaki','2023-12-04','dYQA',301874,'hokage',50000,2),('newhire','nezi','hyuga','2023-12-15','dYQA',301874,'devops engineer',50000,1),('promote','kakashi','kakashi','2023-12-04','dYQA',301874,'senior developer',180000,1),('promote','kakashi','kakashi','2023-12-04','dYQA',301874,'staff',30000,2),('promote','nezi','nezi','2023-12-06','dYQA',301874,'devops senior',100000,2),('terminate','bharat','venna','2023-12-06','dYQA',301874,'Unknown',50000,1),('terminate','kakashi','hatake','2023-12-04','dYQA',301874,'Staff',50000,1);
/*!40000 ALTER TABLE `hr_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manager_requests`
--

DROP TABLE IF EXISTS `manager_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manager_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `assignee` varchar(255) NOT NULL,
  `deadline` date NOT NULL,
  `manager_no` int NOT NULL,
  `dept_name` varchar(255) DEFAULT NULL,
  `task_status` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager_requests`
--

LOCK TABLES `manager_requests` WRITE;
/*!40000 ALTER TABLE `manager_requests` DISABLE KEYS */;
INSERT INTO `manager_requests` VALUES (1,'setup code','python code setup','10000','2023-12-23',301874,NULL,1),(2,'kt session','knowledge transfer','10000','2023-12-30',301874,NULL,0),(3,'grooming','points to be assigned to stories','10000','2023-12-23',301874,NULL,0),(4,'sprint demo','get ready with birndown charts','10000','2023-12-30',301874,NULL,0);
/*!40000 ALTER TABLE `manager_requests` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-06  2:48:00
