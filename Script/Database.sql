CREATE DATABASE  IF NOT EXISTS `ecommercedb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ecommercedb`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: ecommercedb
-- ------------------------------------------------------
-- Server version	8.4.3

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
-- Table structure for table `carrito`
--

DROP TABLE IF EXISTS `carrito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carrito` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `libro_id` int DEFAULT NULL,
  `cantidad` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `libro_id` (`libro_id`),
  CONSTRAINT `carrito_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `carrito_ibfk_2` FOREIGN KEY (`libro_id`) REFERENCES `libros` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carrito`
--

LOCK TABLES `carrito` WRITE;
/*!40000 ALTER TABLE `carrito` DISABLE KEYS */;
/*!40000 ALTER TABLE `carrito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorias`
--

DROP TABLE IF EXISTS `categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `categoria` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias`
--

LOCK TABLES `categorias` WRITE;
/*!40000 ALTER TABLE `categorias` DISABLE KEYS */;
INSERT INTO `categorias` VALUES (1,'Ciencia Ficcion'),(2,'Terror'),(3,'Drama'),(4,'Fantasia'),(5,'Romance');
/*!40000 ALTER TABLE `categorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `libro_categoria`
--

DROP TABLE IF EXISTS `libro_categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `libro_categoria` (
  `libro_id` int NOT NULL,
  `categoria_id` int NOT NULL,
  PRIMARY KEY (`libro_id`,`categoria_id`),
  KEY `categoria_id` (`categoria_id`),
  CONSTRAINT `libro_categoria_ibfk_1` FOREIGN KEY (`libro_id`) REFERENCES `libros` (`id`),
  CONSTRAINT `libro_categoria_ibfk_2` FOREIGN KEY (`categoria_id`) REFERENCES `categorias` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `libro_categoria`
--

LOCK TABLES `libro_categoria` WRITE;
/*!40000 ALTER TABLE `libro_categoria` DISABLE KEYS */;
INSERT INTO `libro_categoria` VALUES (1000,1),(1001,1),(1002,1),(1004,1),(1001,2),(1006,2),(1007,2),(1002,3),(1008,3),(1003,4),(1005,5);
/*!40000 ALTER TABLE `libro_categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `libros`
--

DROP TABLE IF EXISTS `libros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `libros` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(255) NOT NULL,
  `descripcion` text,
  `precio` decimal(10,2) NOT NULL,
  `iva` decimal(10,2) DEFAULT NULL,
  `ventas` int DEFAULT '0',
  `imagen` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1023 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `libros`
--

LOCK TABLES `libros` WRITE;
/*!40000 ALTER TABLE `libros` DISABLE KEYS */;
INSERT INTO `libros` VALUES (1000,'La máquina del tiempo','La trama principal gira en torno a un caballero victoriano y sus teorías sobre los viajes en el tiempo . Para demostrarlas, construye una máquina y viaja 800.000 años hacia el futuro, donde entabla amistad con un grupo de personas, los Eloi, descendientes de los humanos modernos.',30000.00,5700.00,556,'assets/images/tiempo.jpg'),(1001,'En las montañas de la locura','narra una expedición al Ártico que descubre los restos de una civilización extraterrestre inteligente, aún desconocida, anterior a la vida humana en la Tierra ',70000.00,13300.00,740,'assets/images/locura.jpg'),(1002,'Las estrellas, mi destino','Narra la historia de Gulliver Foyle, un hombre sin ambiciones ni rumbo, que es abandonado en una nave espacial averiada y, a causa de su propia rabia y una serie de contratiempos, se reinventa como aristócrata en una sociedad destrozada por la invención de la teletransportación para acechar a quienes le hicieron daño.',300000.00,57000.00,96,'assets/images/estrella.jpg'),(1003,'El señor de los anillos','novela épica de fantasía escrita por J.R.R. Tolkien que narra la aventura de Frodo Bolsón y sus amigos para destruir el Anillo Único',315000.00,59850.00,557,'assets/images/anillos.jpg'),(1004,'La rueda del tiempo','narra la búsqueda de un grupo de jóvenes que podrían ser la reencarnación del Dragón Renacido',400000.00,76000.00,100,'assets/images/rueda.jpg'),(1005,'Orgullo Y Prejuicio','La aparición en Longbourn, un pueblo de la campiña inglesa, de Charles Bingley, joven, soltero y rico, despierta las ambiciones de las familias del vecindario, que lo consideran un excelente partido para sus hijas.',123000.00,23370.00,60,'assets/images/orgullo.jpg'),(1006,'Dispersión','Reid nos cuenta la historia de Penny, una anciana que vive sola, sufre un accidente doméstico y cuando despierta se encuentra en la residencia Seis Cedros. Un lugar muy grande, pero que solo acoge a otros tres ancianos: Peter, Hilbert y Ruth. Penny se siente enseguida bien tratada y acogida pero hay varias cosas que la inquietan.',85000.00,16150.00,79,'assets/images/dispersion.jpg'),(1007,'Los 13 exorcismos de Salomon Joch','El padre Salomon Joch, exorcista al servicio del Vaticano ha sido bendecido (o maldecido quizás) con el don de la inmortalidad. Por su faceta de exorcista inmortal, ha vivido cosas que la mayoría ni siquiera alcanza a imaginar. Una lectura fresca, en la que acompañamos a este peculiar sacerdote en trece exorcismos escalofriantes a través de los tiempos.',189000.00,35910.00,130,'assets/images/exorcismo.jpg'),(1008,'Romeo y Julieta','cuenta la historia de dos jóvenes enamorados, Romeo Montesco y Julieta Capuleto, cuyas familias están en guerra, lo que conduce a una tragedia fatal',40000.00,7600.00,893,'assets/images/romeo.jpg');
/*!40000 ALTER TABLE `libros` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido_detalle`
--

DROP TABLE IF EXISTS `pedido_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido_detalle` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `libro_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `iva` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  KEY `libro_id` (`libro_id`),
  CONSTRAINT `pedido_detalle_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`),
  CONSTRAINT `pedido_detalle_ibfk_2` FOREIGN KEY (`libro_id`) REFERENCES `libros` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido_detalle`
--

LOCK TABLES `pedido_detalle` WRITE;
/*!40000 ALTER TABLE `pedido_detalle` DISABLE KEYS */;
INSERT INTO `pedido_detalle` VALUES (1,1,1000,5,30000.00,5700.00),(2,1,1001,2,70000.00,13300.00),(3,2,1000,5,30000.00,5700.00),(4,3,1000,5,30000.00,5700.00),(5,4,1000,5,30000.00,5700.00),(6,5,1000,201,30000.00,5700.00),(7,6,1001,500,70000.00,13300.00),(8,7,1003,10,315000.00,59850.00),(9,8,1000,10,30000.00,5700.00),(10,9,1003,10,315000.00,59850.00),(11,10,1000,10,30000.00,5700.00),(12,11,1003,10,315000.00,59850.00),(13,12,1000,10,30000.00,5700.00),(14,13,1002,2,300000.00,57000.00),(15,14,1008,3,40000.00,7600.00),(16,15,1003,2,315000.00,59850.00);
/*!40000 ALTER TABLE `pedido_detalle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `total` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (1,100001,'2025-04-07 20:30:37',345100.00),(2,100001,'2025-04-08 22:21:48',178500.00),(3,100001,'2025-04-08 22:23:41',178500.00),(4,100001,'2025-04-08 22:25:25',178500.00),(5,100001,'2025-04-08 22:26:28',7175700.00),(6,100001,'2025-04-08 22:28:32',41650000.00),(7,100001,'2025-04-08 22:34:52',3748500.00),(8,100001,'2025-04-08 22:38:10',357000.00),(9,100001,'2025-04-08 22:39:57',3748500.00),(10,100000,'2025-04-08 23:19:13',357000.00),(11,100001,'2025-04-08 23:36:04',3748500.00),(12,100001,'2025-04-09 11:06:59',357000.00),(13,100001,'2025-04-09 12:46:39',714000.00),(14,100001,'2025-04-09 13:00:25',142800.00),(15,100001,'2025-04-09 13:02:38',749700.00);
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol` varchar(50) DEFAULT 'user',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=100002 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (100000,'admin','admin123','admin'),(100001,'rodrigo','yo','user');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-09 18:12:52
