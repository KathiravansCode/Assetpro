-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 11, 2023 at 09:58 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `cloud_brain_py`
--

-- --------------------------------------------------------

--
-- Table structure for table `vb_account`
--

CREATE TABLE `vb_account` (
  `id` int(11) NOT NULL,
  `rid` int(11) NOT NULL,
  `uname` varchar(30) NOT NULL,
  `bank` varchar(100) NOT NULL,
  `branch` varchar(100) NOT NULL,
  `account` varchar(100) NOT NULL,
  `pinno` varchar(100) NOT NULL,
  `cardno` varchar(100) NOT NULL,
  `acpass` varchar(100) NOT NULL,
  `rdate` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vb_account`
--

INSERT INTO `vb_account` (`id`, `rid`, `uname`, `bank`, `branch`, `account`, `pinno`, `cardno`, `acpass`, `rdate`) VALUES
(1, 1, 'ramesh', 'tQI2bSp6AKl3pZ+0hdKm8ndUIuw0QWWoR882GjC41kY=', 'ABNuJ1rEaXvQDp719F7ht4voMUhlPDLENSNYNkBAQas=', 'cy5hnZMcBJ0P92htTe1u0EJGDbxAqKgH56uXitoQAFg=', 'E6h8LlZ6ay5Zw+5juT29yhm5R7VDMDKbT21oh5qo99Y=', '7TUO6nPQXSVV9fcYvW3iHmZr96hhhp/3CLlyRjPgwyE=', '+3qm5JkOzmDoAwlZZBf3SQ8g+Ihgs4u/ivzvm2VdJ9E=', 'EKnpB2+nMHeCRZeA1HqJofzzjVJVPkfYOuB59Phzeqc=');

-- --------------------------------------------------------

--
-- Table structure for table `vb_audio`
--

CREATE TABLE `vb_audio` (
  `id` int(11) NOT NULL,
  `rid` int(11) NOT NULL,
  `uname` varchar(30) NOT NULL,
  `ftype` varchar(100) NOT NULL,
  `title` varchar(200) NOT NULL,
  `details` text NOT NULL,
  `filename` varchar(200) NOT NULL,
  `rdate` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vb_audio`
--

INSERT INTO `vb_audio` (`id`, `rid`, `uname`, `ftype`, `title`, `details`, `filename`, `rdate`) VALUES
(1, 0, 'ramesh', 'lM2qbGNplHrHQ35tMYalDPNGkhV3JWnQfWjRa8NaIZ4=', '', 'izF+UAj2pWevx2Ygp0sx52V35Z2j2rgFUcSI64B/n8w=', 'Ad0ekfRU+HUsydka+X+k8cZhIyoALme0ZUWdlTQ4qio=', '11-02-2023');

-- --------------------------------------------------------

--
-- Table structure for table `vb_document`
--

CREATE TABLE `vb_document` (
  `id` int(11) NOT NULL,
  `rid` int(11) NOT NULL,
  `uname` varchar(30) NOT NULL,
  `title` varchar(200) NOT NULL,
  `details` text NOT NULL,
  `filename` varchar(200) NOT NULL,
  `rdate` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vb_document`
--

INSERT INTO `vb_document` (`id`, `rid`, `uname`, `title`, `details`, `filename`, `rdate`) VALUES
(1, 1, 'ramesh', '8zrY+eYMNjxRLgWXZ5Nl75BBOxHa12d7a2MXWLft+vY=', 'fL1NK0pG2OhIZTXosGc+s7vBIb8I3e68A2gii+W7Ir4=', 'HPhs6lhVvCxqvjcC22vizpdYijNfwwEWC5m+6i1erLE=', '28-12-2022'),
(2, 1, 'ramesh', 'hrIy6zCplBZ6xe7mOFughPussVykOui1ffEatXxs6Gc=', '5zgTZeos4JOLHjsZ/jCaiGo10iBH+zYvTdS6wPjFjRs=', 'r6R5+JBKc9kAHdT4fx/Utx5cbqQ0DDWzNmfebp8M2pk=', '11-02-2023');

-- --------------------------------------------------------

--
-- Table structure for table `vb_email`
--

CREATE TABLE `vb_email` (
  `id` int(11) NOT NULL,
  `rid` int(11) NOT NULL,
  `uname` varchar(30) NOT NULL,
  `email` varchar(100) NOT NULL,
  `pass` varchar(100) NOT NULL,
  `rdate` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vb_email`
--

INSERT INTO `vb_email` (`id`, `rid`, `uname`, `email`, `pass`, `rdate`) VALUES
(1, 1, 'ramesh', 'DbwosGw09y2LVm/CRUJBgU+0fZL2s/10oggd5rN4a9EksllC4l/P0rSywWFvjPM+', 'mjQaYbGW27BVye4CgDAQYA7AKceHeYh5iHPCHUw+ZVo=', '64wNPi8gAdXdyYB79fXDz6RGjA6ffnIHqlFCyIV//78=');

-- --------------------------------------------------------

--
-- Table structure for table `vb_occupation`
--

CREATE TABLE `vb_occupation` (
  `id` int(11) NOT NULL,
  `rid` int(11) NOT NULL,
  `uname` varchar(30) NOT NULL,
  `company` varchar(200) NOT NULL,
  `position` varchar(200) NOT NULL,
  `experience` text NOT NULL,
  `salary` varchar(100) NOT NULL,
  `duration` varchar(100) NOT NULL,
  `rdate` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vb_occupation`
--

INSERT INTO `vb_occupation` (`id`, `rid`, `uname`, `company`, `position`, `experience`, `salary`, `duration`, `rdate`) VALUES
(1, 1, 'ramesh', '8O8HdnPCNOsLRMYX+On4fN6psSkTMCzfc6Oh7TIs+Sk=', 'QmJpfXCDDFrRF/PDWEN0kSrpNOKRSsZ0T0J/iD2lrr9ISh6DNFeh1Ozasf3iRPNU', '3wkAv3bILOZ2r6lhHGezrplQhd38StksUb8yY/hYertLAtrasNC9iNatOAEyAD2H', 'svBDdbr8bYzn98RSRduW32MbbbrxiGBbtSVcJCaXFyM=', 'k14MEaWT7dE+/Rm5NMhUpHb8BTmveMBZ+zKTos2CFoc=', 'j5/gBZTvvEbqEkTtzyFCLgOoRYM0tGEJNxnvFPfcvqg=');

-- --------------------------------------------------------

--
-- Table structure for table `vb_register`
--

CREATE TABLE `vb_register` (
  `id` int(11) NOT NULL,
  `fname` varchar(200) NOT NULL,
  `lname` varchar(200) NOT NULL,
  `gender` varchar(200) NOT NULL,
  `dob` varchar(200) NOT NULL,
  `address` varchar(200) NOT NULL,
  `address2` varchar(200) NOT NULL,
  `pincode` varchar(200) NOT NULL,
  `city` varchar(200) NOT NULL,
  `state` varchar(200) NOT NULL,
  `country` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `mobile` varchar(200) NOT NULL,
  `mobile2` varchar(200) NOT NULL,
  `landline` varchar(200) NOT NULL,
  `adhar` varchar(200) NOT NULL,
  `voter` varchar(200) NOT NULL,
  `pancard` varchar(200) NOT NULL,
  `driving` varchar(200) NOT NULL,
  `sslc_school` varchar(200) NOT NULL,
  `sslc_mark` varchar(200) NOT NULL,
  `sslc_year` varchar(200) NOT NULL,
  `sslc_per` varchar(200) NOT NULL,
  `hsc_school` varchar(200) NOT NULL,
  `hsc_mark` varchar(200) NOT NULL,
  `hsc_year` varchar(200) NOT NULL,
  `hsc_per` varchar(200) NOT NULL,
  `ug_college` varchar(200) NOT NULL,
  `ug_per` varchar(200) NOT NULL,
  `ug_year` varchar(200) NOT NULL,
  `pg_college` varchar(200) NOT NULL,
  `pg_per` varchar(200) NOT NULL,
  `pg_year` varchar(200) NOT NULL,
  `photo` varchar(200) NOT NULL,
  `uname` varchar(30) NOT NULL,
  `pass` varchar(200) NOT NULL,
  `last_date` varchar(200) NOT NULL,
  `secret` varchar(200) NOT NULL,
  `sms_st` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `rid` int(11) NOT NULL,
  `rdate` varchar(200) NOT NULL,
  `alert_st` int(11) NOT NULL,
  `active_st` int(11) NOT NULL,
  PRIMARY KEY  (`uname`),
  UNIQUE KEY `adhar` (`adhar`),
  UNIQUE KEY `voter` (`voter`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vb_register`
--

INSERT INTO `vb_register` (`id`, `fname`, `lname`, `gender`, `dob`, `address`, `address2`, `pincode`, `city`, `state`, `country`, `email`, `mobile`, `mobile2`, `landline`, `adhar`, `voter`, `pancard`, `driving`, `sslc_school`, `sslc_mark`, `sslc_year`, `sslc_per`, `hsc_school`, `hsc_mark`, `hsc_year`, `hsc_per`, `ug_college`, `ug_per`, `ug_year`, `pg_college`, `pg_per`, `pg_year`, `photo`, `uname`, `pass`, `last_date`, `secret`, `sms_st`, `status`, `rid`, `rdate`, `alert_st`, `active_st`) VALUES
(1, 'QBdcwr0zgPJ7Um1QDwqlBpoZ3AkzIk28qPCL9JwoMuY=', '/hi7X86Rhr2iBHuBRkzNubEA7ypNC7rWemXFSpsJr3U=', 'DkN8643/Tle7aX4oi+fy9buqYr0FNT3xu32xCJbazOA=', 'kGubRrTKTZmMN1T+l8fT0oLyEdklXVjyL27Tx2uKHG0=', 'SDiRxrWTrYo85GU1ydBnCR8ZJZXGCxBf7Gva7M98qCk=', '/hco6+zDARictApk6kOutgnjNmSt2dHvomL7c/hkW3I=', 'bpF3NrcdSzMcM5kxB8axXkNzMVoQo76g69EcIjwa19Q=', 'pn8ZcTRvVcYRAikmk4Qp5bzSZIljOEwzRvDdkfRo00k=', 'sWWbnCCLRr1GBxvQcCztoiQkQbr3RFygkj3XQzaRaFg=', 'c5RQC0/ZCFed+tSxwMNHMm+WOP5wuY/DWvyl/9x2zb4=', '9N0I/aXM6zKx897MukhS08TjnFilC0AG/zXUJ6taoppsm/1fvctTpCDBGh7ecINA', 'Al4Y8GH3p9fHD5T8WYw/wMwGlodDYmKjlbLhzEug9wI=', '/qI6ATrQXaNIUKRlA2+uHZeGK3lRVH6EODGeELX5m84=', 'kowP2w15W8OV+ON8g31muGH38OBgZ3KloWB6X1LM3S4=', 'YwlojYiYuAurYwj8HfXtrGcJ2tLqHlAuQAZ1ZR0+A5w=', 'EISWlgN1ugM2OS2aSej7JEpmSJfx53s2HRrhl5gtpXo=', 'ixgL+PpZxBYggnVYHInkgOPGHPgOOjwk3Oe7rWPc6DQ=', '+T4lxHFfY6Poy5kmE9NVZupLgW+4Sbgq5vRVNPcyBcYduYZngCwFvWHDCKiljjva', '2QYrOaVqWSMl+flfJJHVrol1IFr6n9aXpOe5eeNaR2k=', 'aaQpU27LJrYvfbzvP1n5CSoa3+LldbU/eRPDU7zPF/g=', 'sxq5sq+85OUa6UvfqE7Z3Qwp/85Fy1FF3qA0PgVPhxM=', 'zMMed7ZmQqolxtm15pB1OBo1MBoCO8Zk+E4NDftrl2Y=', 'MLKEK2imZbBZUpiJ7ZlHPsvcH8CugpE3noeoyKz2ZhM=', '4daDmBO1GCanwNEYp56sWlohaPr9Ja9ygnNw1yHVCWw=', 'ajYBUUjYNSqNMLK3cqsGMcjNz7wtCQ+h55MP0V5UUpg=', 'SYgfXfXaAzDyEydh7npMTGftP6TUEpgJkV75NfBjX4Q=', '10L2blOshle/aK1HS/IITU97Bo9xdSY1WUpHsGAYeVk=', 'zpbv81IH6/AXb/8NRBUR1ddoxdaIPsMWLVRu/ijBmKU=', 'MjKl0RTIHOtjsjcaJIvXji5DOkSUM7kC+HmemnB2fxM=', 'Bg7LOjQdQqbRcYhNLqdg3dQiBbxySmjVtv3HtGLa2G4=', 'E5LcEd/SrTdluoFK36IVsagZ5xKo356iKPtqyEsNQYg=', 'h/4l82ug/bvWCO2c5dAC4MIWTfKbG83QHPE+O+zytJE=', '3ZKgUZDAl4AtD4thybiqnRKq8lPUrzVLXmkBKdXDId8=', 'ramesh', 'toCMwqhQg5gpEHYTw/toyw0XWKP4jzPtxCc6GsPJ72U=', 'D2tVl3coSrm9EyKvrXU2B/bQAzlW0UQxBdmRxY+tYE8=', '', 0, 3, 1, 'RLlMRQUVBnnrsJpBe6GtN630ZmiKUCQ6qM6aJaL+HXM=', 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `vb_relative`
--

CREATE TABLE `vb_relative` (
  `id` int(11) NOT NULL,
  `uname` varchar(30) NOT NULL,
  `name` varchar(100) NOT NULL,
  `relation` varchar(100) NOT NULL,
  `mobile` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `pass` varchar(100) NOT NULL,
  `rdate` varchar(100) NOT NULL,
  `secret_key` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vb_relative`
--

INSERT INTO `vb_relative` (`id`, `uname`, `name`, `relation`, `mobile`, `email`, `pass`, `rdate`, `secret_key`) VALUES
(1, 'ramesh', 'jnZEzxWWVOMEnQAOBVLOBWRq5WPIlVBqLZ6q0b1ZmvM=', 'aJJHNwK+pIk51Zd9yAszYtq5DQj/VDOWA0CRy9M9wA8=', '9635102423', 'g9Te5jhA0KSy7NBrFl0wAUjMrxEaMi5qGIet+P39Nd/pga/zpw3Bl9M9Z6UyNXS+', '4F1L3ksEQOS64ks9d4uHQ3xSgifPO1pKVTLorDzEG7o=', 'I9fAWlJj+l+SiaYMfNzefgXOXJY/rVXY4zi0A6ebD1I=', '115851');

-- --------------------------------------------------------

--
-- Table structure for table `vb_user`
--

CREATE TABLE `vb_user` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `mobile` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `userid` varchar(100) NOT NULL,
  `pass` varchar(100) NOT NULL,
  `rdate` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vb_user`
--

INSERT INTO `vb_user` (`id`, `uname`, `name`, `mobile`, `email`, `userid`, `pass`, `rdate`) VALUES
(1, 'ramesh', 'wvN6mRvZT1xZiDsZWD6TxRJ6GMmN+sWAMQNH/hAPEWs=', 'heDU56bHO1+kk3ZKlQEe/50otviX/UqBfDYM8l4Nksg=', 'oxboCgs6HDeKxkvAnZ0vul0HtjFk3JV7MOpOqk5een0z2J+AEmpw3xrl2UcoQUAu', 'raji', '0pxApqe9vkpmzz8rriAmnICmL66QuTq9FwXRg0Tu02I=', 'gpZOz0Ob73hEpo8Y8MDGuMvp2J7/rKczV8FbXhYFLvI=');
