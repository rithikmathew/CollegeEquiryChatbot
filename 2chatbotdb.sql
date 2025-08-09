-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 22, 2021 at 07:37 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `1chatbotdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `name` varchar(50) NOT NULL,
  `psw` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`name`, `psw`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `querytb`
--

CREATE TABLE `querytb` (
  `id` bigint(250) NOT NULL auto_increment,
  `UserName` varchar(250) NOT NULL,
  `QType` varchar(250) NOT NULL,
  `Query` varchar(250) NOT NULL,
  `QDate` varchar(250) NOT NULL,
  `Answer` varchar(250) NOT NULL,
  `Status` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `querytb`
--

INSERT INTO `querytb` (`id`, `UserName`, `QType`, `Query`, `QDate`, `Answer`, `Status`) VALUES
(1, 'san', 'Department', 'asfsaf', '2021-10-21', 'asfsdafgsd', 'Answer'),
(2, 'sangeeth', 'Subject', 'what is java', '2021-10-22', 'java is high level language', 'Answer');

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `id` int(50) NOT NULL auto_increment,
  `name` varchar(50) NOT NULL,
  `age` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `location` varchar(50) NOT NULL,
  `address` varchar(200) NOT NULL,
  `uname` varchar(50) NOT NULL,
  `psw` varchar(50) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`id`, `name`, `age`, `email`, `phone`, `location`, `address`, `uname`, `psw`) VALUES
(1, 'admin', '21', 'test@gmail.com', '9486365535', 'trichy', 'trichy', 'san', 'san'),
(2, 'mani', '20', 'ishu@gmail.com', '09600357839', '12423643', 'dgh', 'mani', 'mani'),
(3, 'sangeeth', '20', 'sangeeth5535@gmail.com', '9486365535', '620001', 'no 6 trichy', 'sangeeth', 'sangeeth');
