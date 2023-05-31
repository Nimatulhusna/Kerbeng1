-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 31, 2023 at 08:05 AM
-- Server version: 10.4.18-MariaDB
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `kb_a`
--

-- --------------------------------------------------------

--
-- Stand-in structure for view `hn_mach`
-- (See below for the actual view)
--
CREATE TABLE `hn_mach` (
`hn_id` int(9)
,`hn_name` varchar(90)
,`type` varchar(90)
,`service` enum('running','stopped')
,`updated` timestamp
,`mc_id` int(9)
,`mc_name` varchar(90)
,`location` varchar(90)
,`platform` enum('Ubuntu 18.04 or below','Ubuntu 20.04 and above')
,`ip` varchar(15)
,`status` enum('active','inactive')
);

-- --------------------------------------------------------

--
-- Table structure for table `honeypot`
--

CREATE TABLE `honeypot` (
  `id` int(9) NOT NULL,
  `name` varchar(90) NOT NULL,
  `type` varchar(90) NOT NULL,
  `m_id` int(9) NOT NULL,
  `created` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `status` tinyint(2) NOT NULL,
  `service` enum('running','stopped') NOT NULL DEFAULT 'stopped'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `honeypot`
--

INSERT INTO `honeypot` (`id`, `name`, `type`, `m_id`, `created`, `updated`, `status`, `service`) VALUES
(1, 'hn', 'dionaea', 1, '2023-05-10 06:36:32', '2023-05-24 14:43:17', 1, 'stopped'),
(4, 'hp', 'dionaea', 2, '2023-05-12 13:06:48', '2023-05-24 14:44:23', 1, 'stopped'),
(5, 'hd', 'dionaea', 3, '2023-05-12 13:06:48', '2023-05-24 14:45:12', 1, 'stopped'),
(6, 'hp2', 'dionaea', 2, '2023-05-12 13:10:01', '2023-05-15 05:03:14', 1, 'stopped'),
(7, 'hd2', 'dionaea', 3, '2023-05-12 13:10:01', '2023-05-15 05:03:14', 1, 'stopped'),
(8, 'hd3', 'dionaea', 3, '2023-05-12 13:10:19', '2023-05-24 14:46:18', 1, 'stopped');

-- --------------------------------------------------------

--
-- Table structure for table `machine`
--

CREATE TABLE `machine` (
  `id` int(9) NOT NULL,
  `name` varchar(90) NOT NULL,
  `location` varchar(90) NOT NULL,
  `platform` enum('Ubuntu 18.04 or below','Ubuntu 20.04 and above') NOT NULL DEFAULT 'Ubuntu 18.04 or below',
  `ip` varchar(15) NOT NULL,
  `user` varchar(90) NOT NULL,
  `passw` varbinary(999) NOT NULL,
  `r_user` varchar(90) NOT NULL,
  `r_pass` varbinary(999) NOT NULL,
  `status` enum('active','inactive') NOT NULL DEFAULT 'inactive'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `machine`
--

INSERT INTO `machine` (`id`, `name`, `location`, `platform`, `ip`, `user`, `passw`, `r_user`, `r_pass`, `status`) VALUES
(1, 'mc', 'ugm', 'Ubuntu 18.04 or below', '1.1.1.1', 'user', 0xb6b97a560e026124d75716d8d39d8a9fb46bba2abc5d758c09, 'user', 0xb6b97a560e026124d75716d8d39d8a9fb46bba2abc5d758c09, 'inactive'),
(2, 'mc2', 'sv', 'Ubuntu 20.04 and above', '2.2.2.2', 'admin', 0xb65c083af272cd4bc9aa704fcfabb11c0e19fcb687da685231, 'admin', 0xb65c083af272cd4bc9aa704fcfabb11c0e19fcb687da685231, 'inactive'),
(3, 'mc3', 'tri', 'Ubuntu 20.04 and above', '3.3.3.3', 'mhs', 0xb6328a1bb8ba15ac439879e595f06ad796d980bf786c9ac65d, 'mhs', 0xb6328a1bb8ba15ac439879e595f06ad796d980bf786c9ac65d, 'inactive'),
(12, 'a', 'a', 'Ubuntu 18.04 or below', '1.2.3.4', 'a', 0xb6ca4c25a2c3aa7ebb574247918f2f05594701637181e13c83, 'a', 0xb6ca4c25a2c3aa7ebb574247918f2f05594701637181e13c83, 'inactive'),
(13, 'z', 'z', 'Ubuntu 18.04 or below', '4.3.2.1', 'z', 0xb622b13c42de680fb7a9a1d104915925228b20d87115cf61ac, 'z', 0xb622b13c42de680fb7a9a1d104915925228b20d87115cf61ac, 'inactive'),
(14, 'x', 'x', 'Ubuntu 18.04 or below', '5.6.7.8', 'x', 0xb67561bf5552b3f8ce673693ec3526c26bb756073183b3139c, 'x', 0xb67561bf5552b3f8ce673693ec3526c26bb756073183b3139c, 'inactive');

-- --------------------------------------------------------

--
-- Table structure for table `repository`
--

CREATE TABLE `repository` (
  `id` int(9) NOT NULL,
  `name` varchar(90) NOT NULL,
  `type` enum('setup','packages','install','additional','services','start','others') NOT NULL DEFAULT 'others',
  `label` varchar(90) NOT NULL,
  `os` enum('any','ubuntu-18','ubuntu+20') NOT NULL DEFAULT 'any',
  `script` varchar(360) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `repository`
--

INSERT INTO `repository` (`id`, `name`, `type`, `label`, `os`, `script`) VALUES
(1, 'dionaea1', 'setup', 'dionaea', 'any', 'git clone https://github.com/DinoTools/dionaea.git'),
(3, 'libemu2', 'packages', 'dionaea', 'ubuntu+20', 'wget http://archive.ubuntu.com/ubuntu/pool/universe/libe/libemu/libemu2_0.2.0+git20120122-1.2build1_amd64.deb'),
(4, 'libemu-dev', 'packages', 'dionaea', 'ubuntu+20', 'wget http://archive.ubuntu.com/ubuntu/pool/universe/libe/libemu/libemu-dev_0.2.0+git20120122-1.2build1_amd64.deb'),
(5, 'git', 'packages', 'dionaea', 'any', 'apt-get install git -y'),
(6, 'build-essential', 'packages', 'dionaea', 'any', 'apt-get install build-essential -y'),
(7, 'cmake', 'packages', 'dionaea', 'any', 'apt-get install cmake -y'),
(8, 'check', 'packages', 'dionaea', 'any', 'apt-get install check -y'),
(9, 'cython3', 'packages', 'dionaea', 'any', 'apt-get install cython3 -y'),
(10, 'libcurl4-openssl-dev', 'packages', 'dionaea', 'any', 'apt-get install libcurl4-openssl-dev -y'),
(11, 'libemu-dev', 'packages', 'dionaea', 'any', 'apt-get install libemu-dev -y'),
(12, 'libev-dev', 'packages', 'dionaea', 'any', 'apt-get install libev-dev -y'),
(13, 'libglib2.0-dev', 'packages', 'dionaea', 'any', 'apt-get install libglib2.0-dev -y'),
(14, 'libloudmouth1-dev', 'packages', 'dionaea', 'any', 'apt-get install libloudmouth1-dev -y'),
(15, 'libnetfilter-queue-dev', 'packages', 'dionaea', 'any', 'apt-get install libnetfilter-queue-dev -y'),
(16, 'libnl-3-dev', 'packages', 'dionaea', 'any', 'apt-get install libnl-3-dev -y'),
(17, 'libpcap-dev', 'packages', 'dionaea', 'any', 'apt-get install libpcap-dev -y'),
(18, 'libssl-dev', 'packages', 'dionaea', 'any', 'apt-get install libssl-dev -y'),
(19, 'libtool', 'packages', 'dionaea', 'any', 'apt-get install libtool -y'),
(20, 'libudns-dev', 'packages', 'dionaea', 'any', 'apt-get install libudns-dev -y'),
(21, 'python3', 'packages', 'dionaea', 'any', 'apt-get install python3 -y'),
(22, 'python3-dev', 'packages', 'dionaea', 'any', 'apt-get install python3-dev -y'),
(23, 'python3-bson', 'packages', 'dionaea', 'any', 'apt-get install python3-bson -y'),
(24, 'python3-yaml', 'packages', 'dionaea', 'any', 'apt-get install python3-yaml -y'),
(25, 'python3-boto3', 'packages', 'dionaea', 'any', 'apt-get install python3-boto3 -y'),
(26, 'fonts-liberation', 'packages', 'dionaea', 'any', 'apt-get install fonts-liberation -y'),
(27, 'libemu2-in', 'packages', 'dionaea', 'ubuntu+20', 'apt install ./libemu2_0.2.0+git20120122-1.2build1_amd64.deb -y'),
(28, 'libemu-dev-in', 'packages', 'dionaea', 'ubuntu+20', 'apt install ./libemu-dev_0.2.0+git20120122-1.2build1_amd64.deb -y'),
(29, 'libnl3', 'packages', 'dionaea', 'ubuntu+20', 'apt-get install libnl-route-3-dev -y'),
(31, 'create_dio_serv', 'services', 'dionaea', 'any', 'touch dionaea.service'),
(32, 'dio_serv_in1', 'services', 'dionaea', 'any', 'echo \'[Unit]\' >> dionaea.service'),
(33, 'dio_serv_in2', 'services', 'dionaea', 'any', 'echo \'Description=honeypot dionaea service\' >> dionaea.service'),
(34, 'dio_serv_in3', 'services', 'dionaea', 'any', 'echo \'After=network.target\' >> dionaea.service'),
(35, 'dio_serv_in4', 'services', 'dionaea', 'any', 'echo \'StartLimitIntervalSec=0\' >> dionaea.service'),
(36, 'dio_serv_in5', 'services', 'dionaea', 'any', 'echo \'\' >> dionaea.service'),
(37, 'dio_serv_in6', 'services', 'dionaea', 'any', 'echo \'[Service]\' >> dionaea.service'),
(38, 'dio_serv_in7', 'services', 'dionaea', 'any', 'echo \'Type=simple\' >> dionaea.service'),
(39, 'dio_serv_in8', 'services', 'dionaea', 'any', 'echo \'Restart=on-failure\' >> dionaea.service'),
(40, 'dio_serv_in9', 'services', 'dionaea', 'any', 'echo \'RestartSec=3\' >> dionaea.service'),
(41, 'dio_serv_in10', 'services', 'dionaea', 'any', 'echo \'User=root\' >> dionaea.service'),
(42, 'dio_serv_in11', 'services', 'dionaea', 'any', 'echo \"ExecStart=/opt/dionaea/bin/dionaea -l all,-debug -L \'*\'\" >> dionaea.service'),
(43, 'dio_serv_in12', 'services', 'dionaea', 'any', 'echo \'\' >> dionaea.service'),
(44, 'dio_serv_in13', 'services', 'dionaea', 'any', 'echo \'[Install]\' >> dionaea.service'),
(45, 'dio_serv_in14', 'services', 'dionaea', 'any', 'echo \'WantedBy=multi-user.target\' >> dionaea.service'),
(46, 'dio_serv_in15', 'services', 'dionaea', 'any', 'cp dionaea.service /etc/systemd/system'),
(47, 'dio_serv_in16', 'services', 'dionaea', 'any', 'cp dionaea.service /lib/systemd/system'),
(48, 'dio_serv_in17', 'services', 'dionaea', 'any', 'cp dionaea.service /usr/lib/systemd/system'),
(49, 'dio_serv_in18', 'services', 'dionaea', 'any', 'systemctl daemon-reload'),
(50, 'strt_dio_serv', 'services', 'dionaea', 'any', 'systemctl start dionaea'),
(51, 'en_dio_serv', 'services', 'dionaea', 'any', 'systemctl enable dionaea'),
(52, 'check', 'others', 'dionaea', 'any', 'systemctl status dionaea'),
(60, 's_editor', 'additional', 'dionaea', 'any', 'select-editor\\n1'),
(62, 'change_dir', 'additional', 'dionaea', 'any', 'cd /opt/dionaea/etc/dionaea/ihandlers-available/'),
(63, 'copy_json_yaml', 'additional', 'dionaea', 'any', 'cp log_json.yaml /opt/dionaea/etc/dionaea/ihandlers-enabled'),
(64, 'get_json_add', 'additional', 'dionaea', 'any', 'wget https://raw.githubusercontent.com/Nimatulhusna/Kerbeng1/main/dionaeaSqliteToJson.py'),
(65, 'move_json_add', 'additional', 'dionaea', 'any', 'mv dionaeaSqliteToJson.py /opt/'),
(66, 'make_cron', 'additional', 'dionaea', 'any', '(crontab -l 2>/dev/null || true; echo \"*/1 * * * * /usr/bin/python3 /opt/dionaeaSqliteToJson.py\") | crontab -'),
(67, 'hom_dir', 'additional', 'dionaea', 'any', 'cd /home'),
(68, 'setcap', 'additional', 'dionaea', 'any', 'setcap CAP_NET_BIND_SERVICE=+eip /opt/dionaea/bin/dionaea'),
(69, 'c_dir', 'install', 'dionaea', 'any', 'cd dionaea'),
(70, 'mk_build', 'install', 'dionaea', 'any', 'mkdir build'),
(71, 'c_dir_build', 'install', 'dionaea', 'any', 'cd build'),
(72, 'cmake_dio', 'install', 'dionaea', 'any', 'cmake -DCMAKE_INSTALL_PREFIX:PATH=/opt/dionaea ..'),
(73, 'make_dio', 'install', 'dionaea', 'any', 'make'),
(74, 'ins_dio', 'install', 'dionaea', 'any', 'make install'),
(75, 'start_dio', 'start', 'dionaea', 'any', 'systemctl start dionaea'),
(76, 'enable_dio', 'start', 'dionaea', 'any', 'systemctl enable dionaea');

-- --------------------------------------------------------

--
-- Structure for view `hn_mach`
--
DROP TABLE IF EXISTS `hn_mach`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `hn_mach`  AS SELECT `hn`.`id` AS `hn_id`, `hn`.`name` AS `hn_name`, `hn`.`type` AS `type`, `hn`.`service` AS `service`, `hn`.`updated` AS `updated`, `mc`.`id` AS `mc_id`, `mc`.`name` AS `mc_name`, `mc`.`location` AS `location`, `mc`.`platform` AS `platform`, `mc`.`ip` AS `ip`, `mc`.`status` AS `status` FROM (`honeypot` `hn` join `machine` `mc` on(`hn`.`m_id` = `mc`.`id`)) ORDER BY `mc`.`id` ASC, `hn`.`id` ASC ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `honeypot`
--
ALTER TABLE `honeypot`
  ADD PRIMARY KEY (`id`),
  ADD KEY `m_id` (`m_id`);

--
-- Indexes for table `machine`
--
ALTER TABLE `machine`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `repository`
--
ALTER TABLE `repository`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `honeypot`
--
ALTER TABLE `honeypot`
  MODIFY `id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `machine`
--
ALTER TABLE `machine`
  MODIFY `id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `repository`
--
ALTER TABLE `repository`
  MODIFY `id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=79;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `honeypot`
--
ALTER TABLE `honeypot`
  ADD CONSTRAINT `honeypot_ibfk_1` FOREIGN KEY (`m_id`) REFERENCES `machine` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
