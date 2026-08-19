-- MySQL dump 10.13  Distrib 5.6.17, for Win32 (x86)
--
-- Host: localhost    Database: wsbodb
-- ------------------------------------------------------
-- Server version	5.6.17

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
-- Table structure for table `_usuarios_user`
--

DROP TABLE IF EXISTS `_usuarios_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `_usuarios_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `email` varchar(75) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_email_verified` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  `papel` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `_usuarios_user`
--

LOCK TABLES `_usuarios_user` WRITE;
/*!40000 ALTER TABLE `_usuarios_user` DISABLE KEYS */;
INSERT INTO `_usuarios_user` VALUES (1,'pbkdf2_sha256$12000$4pujh9ZTBMmi$xqqLqhy3JZ8CgHxH6Lnw9V02KXk6R2W1HEucOJ+gdWs=','2017-03-23 17:17:43',0,'teste@wasaboo.com','','',0,1,0,'2017-03-23 17:14:03','','',''),(2,'pbkdf2_sha256$12000$MiTwstcyadVW$YP7PN8xUIKvfwNnN20JiRo14jzUL/V6lxSvt7A6bvas=','2017-04-29 20:26:00',0,'igormcastro@gmail.com','','',0,1,0,'2017-03-23 17:14:55','','',''),(4,'pbkdf2_sha256$12000$qGVxg40wu2eT$m6L+Pu9HoL1QVBTlAjSbGEi35prlwLrXbh4hVWcU1gk=','2017-04-15 14:07:48',0,'igormachado@gmail.com','','',0,1,0,'2017-03-23 18:17:26','','',''),(5,'pbkdf2_sha256$12000$lRSbDL2BIYaq$a6Ef7w1bMQOmIvznlp31zlpI8BOdkNAOj9yMwdf++OI=','2017-04-15 14:10:54',0,'pedrobrito@gmail.com','','',0,1,0,'2017-04-15 14:05:36','','','');
/*!40000 ALTER TABLE `_usuarios_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `_usuarios_user_groups`
--

DROP TABLE IF EXISTS `_usuarios_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `_usuarios_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `group_id_refs_id_3b346ab7` (`group_id`),
  CONSTRAINT `group_id_refs_id_3b346ab7` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_825f908b` FOREIGN KEY (`user_id`) REFERENCES `_usuarios_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `_usuarios_user_groups`
--

LOCK TABLES `_usuarios_user_groups` WRITE;
/*!40000 ALTER TABLE `_usuarios_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `_usuarios_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `_usuarios_user_user_permissions`
--

DROP TABLE IF EXISTS `_usuarios_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `_usuarios_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `permission_id_refs_id_357e09af` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_357e09af` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_08d2522c` FOREIGN KEY (`user_id`) REFERENCES `_usuarios_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `_usuarios_user_user_permissions`
--

LOCK TABLES `_usuarios_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `_usuarios_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `_usuarios_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `permission_id_refs_id_6ba0f519` (`permission_id`),
  CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `content_type_id_refs_id_93d2d1f8` (`content_type_id`),
  KEY `user_id_refs_id_c3a1921b` (`user_id`),
  CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c3a1921b` FOREIGN KEY (`user_id`) REFERENCES `_usuarios_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('n2a0blue9i65pefmepsmqhs8nyauy6nn','YzU3YWRkZTkyZDM4ZTBlYjBhODJkMDhhMjI2ZWRlNmU1OTEyNmUxNjp7fQ==','2017-05-13 20:26:03'),('n46vhgesinc49uiq6m9nuctqtfjnia5s','ODU3NmM0NDRkNzhjMjYzYmYwMDg1Y2VhMzkyMzkwMmI0NGMwM2FkZjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6Mn0=','2017-04-09 13:13:56');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perfis_convite`
--

DROP TABLE IF EXISTS `perfis_convite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `perfis_convite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `solicitante_id` int(11) NOT NULL,
  `convidado_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `solicitante_id_refs_id_5d24cbc4` (`solicitante_id`),
  KEY `convidado_id_refs_id_5d24cbc4` (`convidado_id`),
  CONSTRAINT `convidado_id_refs_id_5d24cbc4` FOREIGN KEY (`convidado_id`) REFERENCES `perfis_perfil` (`id`),
  CONSTRAINT `solicitante_id_refs_id_5d24cbc4` FOREIGN KEY (`solicitante_id`) REFERENCES `perfis_perfil` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perfis_convite`
--

LOCK TABLES `perfis_convite` WRITE;
/*!40000 ALTER TABLE `perfis_convite` DISABLE KEYS */;
/*!40000 ALTER TABLE `perfis_convite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perfis_perfil`
--

DROP TABLE IF EXISTS `perfis_perfil`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `perfis_perfil` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `telefone` varchar(15) NOT NULL,
  `nome_empresa` varchar(255) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `usuario_id_refs_id_36186a4f` FOREIGN KEY (`usuario_id`) REFERENCES `_usuarios_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perfis_perfil`
--

LOCK TABLES `perfis_perfil` WRITE;
/*!40000 ALTER TABLE `perfis_perfil` DISABLE KEYS */;
INSERT INTO `perfis_perfil` VALUES (1,'Teste','33333333','teste LTDA',1),(2,'Igor','38652218','COC',2),(3,'Castro','89898989','CM',4),(4,'Pedro Brito','38652218','Solar Lafayete',5);
/*!40000 ALTER TABLE `perfis_perfil` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perfis_perfil_contatos`
--

DROP TABLE IF EXISTS `perfis_perfil_contatos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `perfis_perfil_contatos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from_perfil_id` int(11) NOT NULL,
  `to_perfil_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `from_perfil_id` (`from_perfil_id`,`to_perfil_id`),
  KEY `to_perfil_id_refs_id_4d7ab45a` (`to_perfil_id`),
  CONSTRAINT `from_perfil_id_refs_id_4d7ab45a` FOREIGN KEY (`from_perfil_id`) REFERENCES `perfis_perfil` (`id`),
  CONSTRAINT `to_perfil_id_refs_id_4d7ab45a` FOREIGN KEY (`to_perfil_id`) REFERENCES `perfis_perfil` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perfis_perfil_contatos`
--

LOCK TABLES `perfis_perfil_contatos` WRITE;
/*!40000 ALTER TABLE `perfis_perfil_contatos` DISABLE KEYS */;
INSERT INTO `perfis_perfil_contatos` VALUES (1,1,2),(2,2,1),(6,2,3),(7,2,4),(5,3,2),(4,3,4),(8,4,2),(3,4,3);
/*!40000 ALTER TABLE `perfis_perfil_contatos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-05-03 15:05:58
