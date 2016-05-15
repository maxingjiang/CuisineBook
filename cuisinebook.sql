-- MySQL dump 10.13  Distrib 5.6.28, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: cuisinebook
-- ------------------------------------------------------
-- Server version	5.6.28-0ubuntu0.15.10.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `CuisineBook`
--
SET NAMES utf8;

DROP TABLE IF EXISTS `CuisineBook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kBCookBook` (
  `kBCookBookId` varchar(128) NOT NULL,
  `kBCookerId` varchar(128) DEFAULT '',
  `kBDishName` varchar(128) NOT NULL,
  `kBFavorNums` varchar(64) DEFAULT '0',
  `kBDescription`text DEFAULT '', 
  `kBTips` text DEFAULT '',
  `kBFoodMaterials` text DEFAULT '',
  `kBIsPublish` varchar(4) DEFAULT '0',
  `kBKind` varchar(64) DEFAULT '',
  `kBFollowMadeNums` varchar(64) DEFAULT '0',
  `kBVisitNums` varchar(64) DEFAULT '0',
  `kBTopic` text DEFAULT '',
  `kBSubKind` varchar(64) DEFAULT '',
  `kBFrontCoverUrl` varchar(256) DEFAULT '',
  `kBStepNums` varchar(64) DEFAULT '0',
  `kBVideoUrl` varchar(256) DEFAULT '',
  `kBTags` text DEFAULT '',
  `kBTimeNeeded` varchar(64) DEFAULT '',
  `kBCookSteps` text DEFAULT '',
  `kBNickName` varchar(64) DEFAULT '',
  `kBIconUrl` varchar(64) DEFAULT '',
  `kBCreateTime` bigint DEFAULT 0,
  PRIMARY KEY (`kBCookBookId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `Prouct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Prouct` (
  `kPProuctId` varchar(128) NOT NULL,
  `kPCookerId` varchar(128) DEFAULT '',
  `kPDishName` varchar(128) NOT NULL,
  `kPFollowBookId` varchar(64) DEFAULT '',
  `kPPhotoNums` varchar(64) DEFAULT '0',
  `kPFrontCoverUrl` varchar(128) DEFAULT '',
  `kPTopic` text DEFAULT '',
  `kPDescription` text DEFAULT '',
  `kPKind` varchar(64) DEFAULT '',
  `kPSubKind` varchar(64) DEFAULT '',
  `kPIsPublished` varchar(4) DEFAULT '0',
  `kPTags` varchar(64) DEFAULT '',
  `kPTips` text DEFAULT '',
  `kPScore` varchar(64) DEFAULT '',
  `kPPhotos` text DEFAULT '',
  `kPNickName` varchar(64) DEFAULT '',
  `kPIconUrl` varchar(64) DEFAULT '',
  `kPCreateTime` bigint DEFAULT 0,
  PRIMARY KEY (`kPProuctId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `icon`
--

DROP TABLE IF EXISTS `icon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `icon` (
  `iconid` varchar(128) NOT NULL,
  `imagemd5` varchar(128) DEFAULT NULL,
  `image64` longtext,
  `created_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`iconid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `userid` varchar(128) NOT NULL,
  `password` varchar(60) NOT NULL,
  `nickname` varchar(64) DEFAULT NULL,
  `type` int(11) NOT NULL DEFAULT '0',
  `icon` varchar(128) DEFAULT NULL,
  `tel` varchar(64) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`userid`),
  UNIQUE KEY `tel` (`tel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-04-14  4:52:50
