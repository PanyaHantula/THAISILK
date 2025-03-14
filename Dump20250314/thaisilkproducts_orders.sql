-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: thaisilkproducts
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `orderID` varchar(15) NOT NULL,
  `weight` float NOT NULL,
  `basketNumber` varchar(3) DEFAULT NULL,
  `grade` varchar(1) NOT NULL DEFAULT 'A',
  `weightReject` varchar(10) DEFAULT NULL,
  `materialType` varchar(15) NOT NULL,
  `price` float NOT NULL,
  `staffID` varchar(5) NOT NULL,
  `customerID` varchar(10) NOT NULL,
  `building` varchar(1) DEFAULT NULL,
  `container` varchar(10) DEFAULT 'basket',
  `containerWeight` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=172 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (131,'2025-03-10 20:10:56','202503100008',10.24,'1','A','0.0','sakonnakhon',15,'0010','3102','B','basket',4.7),(132,'2025-03-10 20:11:00','202503100008',17.35,'2','B','0.5','sakonnakhon',15,'0010','3102','B','basket',4.7),(133,'2025-03-10 20:11:04','202503100008',19.61,'3','C','1.0','sakonnakhon',15,'0010','3102','B','basket',4.7),(134,'2025-03-10 20:11:08','202503100008',16.4,'4','D','2.0','sakonnakhon',15,'0010','3102','B','basket',4.7),(135,'2025-03-10 20:11:12','202503100008',12.81,'5','E','3.0','sakonnakhon',15,'0010','3102','B','basket',4.7),(136,'2025-03-10 20:11:18','202503100008',19.12,'6','F','4.0','sakonnakhon',15,'0010','3102','B','basket',4.7),(137,'2025-03-10 20:11:32','202503100008',16.63,'7','A','0.0','sakonnakhon',15,'0010','3101','B','basket',4.7),(138,'2025-03-10 20:11:36','202503100008',16.05,'8','B','0.5','sakonnakhon',15,'0010','3101','B','basket',4.7),(139,'2025-03-10 20:11:42','202503100008',18.55,'9','C','1.0','sakonnakhon',15,'0010','3101','B','basket',4.7),(140,'2025-03-10 20:11:46','202503100008',18.78,'10','D','2.0','sakonnakhon',15,'0010','3101','B','basket',4.7),(141,'2025-03-10 20:11:50','202503100008',15.09,'11','E','3.0','sakonnakhon',15,'0010','3101','B','basket',4.7),(142,'2025-03-10 20:11:56','202503100008',19.97,'12','F','4.0','sakonnakhon',15,'0010','3101','B','basket',4.7),(143,'2025-03-10 20:12:07','202503100008',18.05,'13','A','0.0','sakonnakhon',15,'0010','3103','B','basket',4.7),(144,'2025-03-10 20:12:12','202503100008',12.07,'14','B','0.5','sakonnakhon',15,'0010','3103','B','basket',4.7),(145,'2025-03-10 20:12:16','202503100008',19.75,'15','C','1.0','sakonnakhon',15,'0010','3103','B','basket',4.7),(146,'2025-03-10 20:12:21','202503100008',14.53,'16','D','2.0','sakonnakhon',15,'0010','3103','B','basket',4.7),(147,'2025-03-10 20:12:28','202503100008',12.58,'17','E','3.0','sakonnakhon',15,'0010','3103','B','basket',4.7),(148,'2025-03-10 20:12:34','202503100008',17.25,'18','F','4.0','sakonnakhon',15,'0010','3103','B','basket',4.7),(149,'2025-03-12 21:36:09','202503120009',10.16,'1','A','0.0','buriram',15,'0010','3103','A','basket',4.7),(150,'2025-03-12 21:36:13','202503120009',17.77,'2','B','0.5','buriram',15,'0010','3103','A','basket',4.7),(151,'2025-03-12 21:36:16','202503120009',12.53,'3','C','1.0','buriram',15,'0010','3103','A','basket',4.7),(152,'2025-03-12 21:36:19','202503120009',16.43,'4','D','2.0','buriram',15,'0010','3103','A','basket',4.7),(153,'2025-03-12 21:36:24','202503120009',17.58,'5','E','3.0','buriram',15,'0010','3103','A','basket',4.7),(154,'2025-03-12 21:36:29','202503120009',17.49,'6','F','4.0','buriram',15,'0010','3103','A','basket',4.7),(155,'2025-03-13 13:02:59','202503130010',8.14,'86','B','0.3','buriram',16,'4001','2102','B','basket',4.7),(156,'2025-03-13 13:03:23','202503130010',8.14,'78','A','0.0','buriram',16,'4001','2102','B','basket',4.7),(157,'2025-03-13 13:28:16','202503130011',8.14,'87','F','4.0','buriram',16,'0010','2103','B','basket',4.7),(158,'2025-03-13 13:28:30','202503130011',8.14,'88','B','0.3','buriram',16,'0010','2103','B','basket',4.7),(159,'2025-03-13 13:28:59','202503130011',12.56,'99','C','1.0','buriram',16,'0010','2103','B','basket',4.7),(160,'2025-03-13 13:29:39','202503130011',8.14,'56','E','3.0','buriram',16,'0010','2103','B','basket',4.7),(161,'2025-03-13 13:39:28','202503130011',8.14,'33','C','1.0','buriram',16,'0010','2105','B','basket',4.7),(162,'2025-03-14 17:38:14','202503140012',14.15,'12','A','0.0','sakonnakhon',14,'0010','2103','A','basket',4.7),(163,'2025-03-14 17:38:19','202503140012',19.69,'10','B','0.3','sakonnakhon',14,'0010','2103','A','basket',4.7),(164,'2025-03-14 17:38:24','202503140012',17.34,'11','F','4.0','sakonnakhon',14,'0010','2103','A','basket',4.7),(165,'2025-03-14 17:38:32','202503140012',19.55,'8','E','3.0','sakonnakhon',14,'0010','2103','A','basket',4.7),(166,'2025-03-14 17:38:41','202503140012',10.85,'7','B','0.3','sakonnakhon',14,'0010','2103','A','basket',4.7),(167,'2025-03-14 17:41:05','202503140013',15.46,'1','A','0.0','sakonnakhon',17,'0010','3105','A','basket',4.7),(168,'2025-03-14 17:41:08','202503140013',16.58,'2','B','0.3','sakonnakhon',17,'0010','3105','A','basket',4.7),(169,'2025-03-14 17:41:12','202503140013',14.51,'4','D','2.0','sakonnakhon',17,'0010','3105','A','basket',4.7),(170,'2025-03-14 17:41:16','202503140013',11.61,'5','A','0.0','sakonnakhon',17,'0010','3105','A','basket',4.7),(171,'2025-03-14 17:41:28','202503140013',12.25,'6','E','3.0','sakonnakhon',17,'0010','3105','A','basket',4.7);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-14 22:58:58
