-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 05, 2019 at 08:59 PM
-- Server version: 10.1.35-MariaDB
-- PHP Version: 7.2.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pgsdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `authtoken_token`
--

CREATE TABLE `authtoken_token` (
  `key` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `authtoken_token`
--

INSERT INTO `authtoken_token` (`key`, `created`, `user_id`) VALUES
('cbb051828676bc237ff2cbe7fe0942ba94a1fb44', '2018-12-02 21:20:26.782571', 1);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(80) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add user info', 7, 'add_userinfo'),
(26, 'Can change user info', 7, 'change_userinfo'),
(27, 'Can delete user info', 7, 'delete_userinfo'),
(28, 'Can view user info', 7, 'view_userinfo'),
(29, 'Can add pocket margin data', 8, 'add_pocketmargindata'),
(30, 'Can change pocket margin data', 8, 'change_pocketmargindata'),
(31, 'Can delete pocket margin data', 8, 'delete_pocketmargindata'),
(32, 'Can view pocket margin data', 8, 'view_pocketmargindata'),
(33, 'Can add year info', 9, 'add_yearinfo'),
(34, 'Can change year info', 9, 'change_yearinfo'),
(35, 'Can delete year info', 9, 'delete_yearinfo'),
(36, 'Can view year info', 9, 'view_yearinfo'),
(37, 'Can add Token', 10, 'add_token'),
(38, 'Can change Token', 10, 'change_token'),
(39, 'Can delete Token', 10, 'delete_token'),
(40, 'Can view Token', 10, 'view_token');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `first_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$120000$crGlQvsrOyDR$uFUE+VIzP8QCVp56PxBF9cxV6JDD2ZUc+hIQNXyIf5w=', NULL, 1, 'admin', '', '', 'admin@gmail.com', 1, 1, '2018-10-25 11:17:11.233000');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `data_pocketmargindata`
--

CREATE TABLE `data_pocketmargindata` (
  `id` int(11) NOT NULL,
  `profit_center_code` int(10) UNSIGNED NOT NULL,
  `profit_center_name` longtext COLLATE utf8_unicode_ci NOT NULL,
  `product_segmentation` longtext COLLATE utf8_unicode_ci NOT NULL,
  `channel_partnar_ind` longtext COLLATE utf8_unicode_ci NOT NULL,
  `business_segment_group` longtext COLLATE utf8_unicode_ci NOT NULL,
  `customer_group_code` int(10) UNSIGNED NOT NULL,
  `customer_group_name` longtext COLLATE utf8_unicode_ci NOT NULL,
  `material_number_code` int(10) UNSIGNED NOT NULL,
  `material_name` longtext COLLATE utf8_unicode_ci NOT NULL,
  `freight_type_code` longtext COLLATE utf8_unicode_ci NOT NULL,
  `freight_types` longtext COLLATE utf8_unicode_ci NOT NULL,
  `best_fit_acc_man` longtext COLLATE utf8_unicode_ci NOT NULL,
  `manf_plant` longtext COLLATE utf8_unicode_ci NOT NULL,
  `sold_to_region` longtext COLLATE utf8_unicode_ci NOT NULL,
  `business_segment` longtext COLLATE utf8_unicode_ci NOT NULL,
  `product_family` longtext COLLATE utf8_unicode_ci NOT NULL,
  `sales_volume_mt` double NOT NULL,
  `gross_sale_usd` double NOT NULL,
  `invoice_price` double NOT NULL,
  `freight_costs` double NOT NULL,
  `freight_revenue` longtext COLLATE utf8_unicode_ci NOT NULL,
  `other_discounts_and_rebates` double NOT NULL,
  `pocket_price` double NOT NULL,
  `cogs` double NOT NULL,
  `pocket_margin` double NOT NULL,
  `pocket_margin_percentage` double NOT NULL,
  `volume_bands` longtext COLLATE utf8_unicode_ci NOT NULL,
  `floor_pocket_margin_corresponding_band` double NOT NULL,
  `target_pocket_margin_corresponding_band` double NOT NULL,
  `lower_than_floor_flag` longtext COLLATE utf8_unicode_ci NOT NULL,
  `lower_than_target_flag` longtext COLLATE utf8_unicode_ci NOT NULL,
  `change_in_invoice_price_per_mt_if_using_floor` longtext COLLATE utf8_unicode_ci NOT NULL,
  `change_in_invoice_price_per_mt_if_using_target` longtext COLLATE utf8_unicode_ci NOT NULL,
  `opportunity_to_floor` double NOT NULL,
  `opportunity_to_target` double NOT NULL,
  `percentage_change_in_invoice_price_or_mt_if_using_floor_margin` longtext COLLATE utf8_unicode_ci NOT NULL,
  `percentage_change_in_invoice_price_or_mt_if_using_target_margin` longtext COLLATE utf8_unicode_ci NOT NULL,
  `year_info_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `data_pocketmargindata`
--

INSERT INTO `data_pocketmargindata` (`id`, `profit_center_code`, `profit_center_name`, `product_segmentation`, `channel_partnar_ind`, `business_segment_group`, `customer_group_code`, `customer_group_name`, `material_number_code`, `material_name`, `freight_type_code`, `freight_types`, `best_fit_acc_man`, `manf_plant`, `sold_to_region`, `business_segment`, `product_family`, `sales_volume_mt`, `gross_sale_usd`, `invoice_price`, `freight_costs`, `freight_revenue`, `other_discounts_and_rebates`, `pocket_price`, `cogs`, `pocket_margin`, `pocket_margin_percentage`, `volume_bands`, `floor_pocket_margin_corresponding_band`, `target_pocket_margin_corresponding_band`, `lower_than_floor_flag`, `lower_than_target_flag`, `change_in_invoice_price_per_mt_if_using_floor`, `change_in_invoice_price_per_mt_if_using_target`, `opportunity_to_floor`, `opportunity_to_target`, `percentage_change_in_invoice_price_or_mt_if_using_floor_margin`, `percentage_change_in_invoice_price_or_mt_if_using_target_margin`, `year_info_id`) VALUES
(50777, 1, 'Profit Center 1', 'Differentiated', '', 'Petrochemical', 138, 'Customer SoldTo 138', 385, 'Material 385', '51', 'Prepaid', 'Sales Person 32', 'EU', 'EU', 'Petrochemical', 'Product Family 121', 100, 1977.97372824188, 2260.541403705, -332.248248041694, '0', -0.882694942265224, 1927.41046072104, -735.813679240276, 1191.59678148077, 69, '1. Low', 0.572375862265906, 0.619903629276617, 'FLAG', 'FLAG', '239.18797988028336', '551.757540875466', 209.289482395248, 482.787848266033, '0.1058100415627235', '0', 11),
(50778, 1, 'Profit Center 1', 'Differentiated', '', 'Petrochemical', 1279, 'Customer SoldTo 1279', 385, 'Material 385', '51', 'Prepaid', 'Sales Person 34', 'EU', 'EU', 'Petrochemical', 'Product Family 121', 200, 17235.7587642492, 3191.80717856467, -325.691849933805, '0', 0, 2866.11532863086, -735.803006761528, 2130.31232186933, 55, '1. Low', 0.572375862265906, 0.619903629276617, '', '', '0', '0', 0, 0, '0', '0', 11),
(50779, 1, 'Profit Center 1', 'Differentiated', '', 'Pharma/Personal Care', 1419, 'Customer SoldTo 1419', 561, 'Material 561', '3', 'Indent', 'Sales Person 55', 'EU', 'AP', 'Pharma/Personal Care', 'Product Family 121', 200, 13026.92245831, 2171.15374305166, -214.944220562114, '0', 0, 1956.20952248955, -713.493526698503, 1242.71599579104, 43, '1. Low', 0.572375862265906, 0.619903629276617, '', 'FLAG', '0', '271.4840161399229', 0, 1628.90409683954, '0', '0', 11),
(50780, 1, 'Profit Center 1', 'Differentiated', '', 'Pharma/Personal Care', 1, 'Customer SoldTo 1', 561, 'Material 561', '51', 'Prepaid', 'Sales Person 1', 'EU', 'EU', 'Pharma/Personal Care', 'Product Family 121', 400, 58136.7777082855, 1845.61199073922, -118.18077337084, '0.5818307190064639', -0.0663289886054719, 1727.94671909878, -738.706288997397, 989.240430101386, 68, '2. Mid', 0.519648572757596, 0.519648572757596, '', '', '0', '0', 0, 0, '0', '0', 11),
(50781, 2, 'Profit Center 2', 'Differentiated', 'Y', 'Petrochemical', 469, 'Customer SoldTo 469', 385, 'Material 385', '51', 'Prepaid', 'Sales Person 64', 'EU', 'EU', 'Petrochemical', 'Product Family 121', 800, 96925.059878859, 1794.90851627517, -138.863099197065, '0', -0.0969468918626858, 1655.94847018624, -735.801933380045, 920.146536806194, 70, '2. Mid', 0.519648572757596, 0.519648572757596, 'FLAG', 'FLAG', '26.17898312250577', '26.17898312250577', 1413.66508861531, 1413.66508861531, '0.014585135055703545', '0', 11),
(50782, 1, 'Profit Center 1', 'Differentiated', '', 'Petrochemical', 139, 'Customer SoldTo 139', 385, 'Material 385', '51', 'Prepaid', 'Sales Person 22', 'EU', 'EU', 'Petrochemical', 'Product Family 121', 900, 128579.59504274, 1785.82770892695, -151.954108380162, '0', 0, 1633.87360054679, -735.80123568208, 898.072364864707, 65, '3. High', 0.502888582350608, 0.502888582350608, '', '', '0', '0', 0, 0, '0', '0', 11),
(50783, 4, 'Profit Center 4', 'Differentiated', '', 'Pharma/Personal Care', 1, 'Customer SoldTo 1', 1, 'Material 1', '51', 'Prepaid', 'Sales Person 1', 'EU', 'EU', 'Pharma/Personal Care', 'Product Family 121', 1000, 5547748.31768529, 1780.61218146933, -370.728871394376, '0.5818307190064639', -0.0639929766863613, 1410.40114781728, -697.463967817511, 712.937179999765, 80, '3. High', 0.502888582350608, 0.502888582350608, 'FLAG', 'FLAG', '367.1457729106005', '367.1457729106005', 1143894.42305696, 1143894.42305696, '0.20619075660127048', '0', 11),
(50784, 1, 'Profit Center 1', 'Differentiated', 'Y', 'Coatings', 263, 'Customer SoldTo 263', 12, 'Material 12', '3', 'Indent', 'Sales Person 61', 'EU', 'AP', 'Coatings', 'Product Family 121', 1100, 168.418723645598, 8420.9361822799, -1822.8130133876, '0', 0, 6598.1231688923, -2711.6001811169, 3886.5229877754, 45, '1. Low', 0.6019261726501, 0.676663724472687, 'FLAG', 'FLAG', '2969.9488319183056', '5602.8945404237365', 59.3989766383661, 112.057890808475, '0.3526863008614104', '0', 11),
(50785, 4, 'Profit Center 4', 'Differentiated', '', 'Coatings', 1155, 'Customer SoldTo 1155', 314, 'Material 314', '#', 'Not assigned', 'Sales Person 30', 'EU', 'LA', 'Coatings', 'Product Family 121', 1200, 838.080919763308, 20952.0229940827, -586.656643834316, '0', 0, 20365.3663502484, -4923.24532176587, 15442.1210284825, 69, '1. Low', 0.6019261726501, 0.676663724472687, '', '', '0', '0', 0, 0, '0', '0', 11),
(50786, 1, 'Profit Center 1', 'Differentiated', '', 'Coatings', 1246, 'Customer SoldTo 1246', 314, 'Material 314', '#', 'Not assigned', 'Sales Person 30', 'EU', 'LA', 'Coatings', 'Product Family 121', 1500, 545.541424053262, 13638.5356013316, -381.878996837283, '0', 0, 13256.6566044943, -4923.3054823979, 8333.35112209637, 55, '1. Low', 0.6019261726501, 0.676663724472687, '', 'FLAG', '0', '2769.1021454174843', 0, 110.764085816699, '0', '0', 11),
(50787, 1, 'Profit Center 1', 'Differentiated', 'Y', 'Coatings', 106, 'Customer SoldTo 106', 12, 'Material 12', '#', 'Not assigned', 'Sales Person 33', 'EU', 'AP', 'Coatings', 'Product Family 121', 1600, 1352.46397721167, 22541.0662868612, -9084.81780299218, '0', 0, 13456.248483869, -2777.4803700152, 10678.7681138538, 43, '1. Low', 0.6019261726501, 0.676663724472687, 'FLAG', 'FLAG', '7258.175356274096', '14146.119998258713', 435.490521376446, 848.767199895523, '0.3219978710814032', '0', 11),
(50788, 1, 'Profit Center 1', 'Differentiated', '', 'Coatings', 557, 'Customer SoldTo 557', 12, 'Material 12', '51', 'Prepaid', 'Sales Person 12', 'EU', 'EU', 'Coatings', 'Product Family 121', 2000, 532.0966688721, 8868.277814535, -785.779648621217, '0', 0, 8082.49816591379, -2848.86179466925, 5233.63637124454, 68, '1. Low', 0.6019261726501, 0.676663724472687, 'FLAG', 'FLAG', '262.29343524395335', '2372.7789996529937', 15.7376061146372, 142.36673997918, '0.02957659206549185', '0', 11),
(50789, 3, 'Profit Center 3', 'Differentiated', '', 'Coatings', 20, 'Customer SoldTo 20', 314, 'Material 314', '53', 'Collect', 'Sales Person 14', 'EU', 'NA', 'Coatings', 'Product Family 121', 2100, 6659.98, 18499.9444444444, 0, '0', 0, 18499.9444444444, -3114.36111111111, 15385.5833333333, 70, '1. Low', 0.6019261726501, 0.676663724472687, '', '', '0', '0', 0, 0, '0', '0', 11),
(50790, 1, 'Profit Center 1', 'Differentiated', '', 'Coatings', 2, 'Customer SoldTo 2', 902, 'Material 902', '51', 'Prepaid', 'Sales Person 2', 'EU', 'EU', 'Coatings', 'Product Family 121', 2200, 3524.126085776, 8810.31521444, -221.446113662947, '0', 0, 8588.86910077705, -2875.06088991219, 5713.80821086486, 65, '1. Low', 0.6019261726501, 0.676663724472687, '', 'FLAG', '0', '766.4234256188684', 0, 306.569370247547, '0', '0', 11),
(50791, 2, 'Profit Center 2', 'Differentiated', '', 'Coatings', 950, 'Customer SoldTo 950', 12, 'Material 12', '#', 'Not assigned', 'Sales Person 29', 'EU', 'EU', 'Coatings', 'Product Family 121', 2500, 2303.66557817568, 5759.1639454392, -153.555887182207, '492.6821008075', 0, 6098.29015906449, -2848.8328133692, 3249.45734569529, 80, '1. Low', 0.6019261726501, 0.676663724472687, 'FLAG', 'FLAG', '545.4620493211205', '2002.7445990040624', 218.184819728448, 801.097839601625, '0.09471201974604022', '0', 11),
(50792, 1, 'Profit Center 1', 'Differentiated', 'Y', 'Coatings', 1525, 'Customer SoldTo 1525', 12, 'Material 12', '3', 'Indent', 'Sales Person 47', 'EU', 'LA', 'Coatings', 'Product Family 121', 2800, 8601.41800369762, 11946.4138940245, -334.499589032685, '0', 0, 11611.9143049918, -2848.76519033576, 8763.14911465603, 45, '1. Low', 0.6019261726501, 0.676663724472687, '', '', '0', '0', 0, 0, '0', '0', 11),
(50793, 3, 'Profit Center 3', 'Differentiated', '', 'Coatings', 898, 'Customer SoldTo 898', 12, 'Material 12', '51', 'Prepaid', 'Sales Person 22', 'EU', 'EU', 'Coatings', 'Product Family 121', 3500, 7027.84933631856, 9760.901855998, -438.277760329443, '0', 0, 9322.62409566856, -2848.79739178026, 6473.8267038883, 69, '1. Low', 0.6019261726501, 0.676663724472687, '', 'FLAG', '0', '405.21744734640197', 0, 291.756562089409, '0', '0', 11),
(50794, 4, 'Profit Center 4', 'Differentiated', '', 'Coatings', 129, 'Customer SoldTo 129', 12, 'Material 12', '3', 'Indent', 'Sales Person 57', 'EU', 'LA', 'Coatings', 'Product Family 121', 3600, 6259.96081026, 8694.39001425, -243.442920399, '0', 0, 8450.947093851, -2848.79739178026, 5602.14970207074, 55, '1. Low', 0.6019261726501, 0.676663724472687, '', 'FLAG', '0', '869.1527931144901', 0, 625.790011042433, '0', '0', 11),
(50795, 2, 'Profit Center 2', 'Differentiated', '', 'Coatings', 1521, 'Customer SoldTo 1521', 12, 'Material 12', '51', 'Prepaid', 'Sales Person 32', 'EU', 'EU', 'Coatings', 'Product Family 121', 3700, 10942.4114963345, 10131.862496606, -425.538224857452, '0', 0, 9706.32427174855, -2848.79739178026, 6857.52687996829, 43, '1. Low', 0.6019261726501, 0.676663724472687, '', '', '0', '0', 0, 0, '0', '0', 11),
(50796, 1, 'Profit Center 1', 'Differentiated', '', 'Coatings', 1527, 'Customer SoldTo 1527', 12, 'Material 12', '51', 'Prepaid', 'Sales Person 31', 'EU', 'EU', 'Coatings', 'Product Family 121', 3800, 10822.544839338, 10020.8748512389, -396.249508353152, '0', 0, 9624.62534288576, -2848.79739178026, 6775.8279511055, 68, '1. Low', 0.6019261726501, 0.676663724472687, '', 'FLAG', '0', '15.261350432938343', 0, 16.4822584675734, '0', '0', 11),
(50797, 2, 'Profit Center 2', 'Differentiated', 'Y', 'Coatings', 111, 'Customer SoldTo 111', 12, 'Material 12', '3', 'Indent', 'Sales Person 5', 'EU', 'AP', 'Coatings', 'Product Family 121', 3900, 7000.40522879183, 6481.85669332577, -162.046417333144, '0', 0, 6319.81027599263, -2711.59664228689, 3608.21363370573, 70, '1. Low', 0.6019261726501, 0.676663724472687, 'FLAG', 'FLAG', '737.0129288012777', '2405.6182889772817', 795.97396310538, 2598.06775209546, '0.11370398385391092', '0', 11),
(50798, 2, 'Profit Center 2', 'Differentiated', '', 'Coatings', 754, 'Customer SoldTo 754', 12, 'Material 12', '49', 'Customer Pickup', 'Sales Person 19', 'EU', 'EU', 'Coatings', 'Product Family 121', 4100, 4882.7694320028, 4521.08280741, 0, '0', -36.5191457089171, 4484.56366170108, -2848.77592415059, 1635.78773755049, 65, '1. Low', 0.6019261726501, 0.676663724472687, 'FLAG', 'FLAG', '2727.0577927088434', '4402.428992044069', 2945.22241612555, 4754.62331140759, '0.6031868711272504', '0', 11),
(50799, 1, 'Profit Center 1', 'Differentiated', '', 'Coatings', 431, 'Customer SoldTo 431', 12, 'Material 12', '3', 'Indent', 'Sales Person 61', 'EU', 'AP', 'Coatings', 'Product Family 121', 4200, 14237.6800622607, 9887.27782101439, -288.143111090062, '0', 0, 9599.13470992433, -2711.59664228689, 6887.53806763743, 80, '1. Low', 0.6019261726501, 0.676663724472687, '', '', '0', '0', 0, 0, '0', '0', 11),
(50800, 1, 'Profit Center 1', 'Differentiated', '', 'Coatings', 473, 'Customer SoldTo 473', 12, 'Material 12', '51', 'Prepaid', 'Sales Person 2', 'EU', 'EU', 'Coatings', 'Product Family 121', 4300, 11969.0450692171, 8311.836853623, -349.097147852166, '0', 0, 7962.73970577083, -2848.78129105801, 5113.95841471283, 45, '1. Low', 0.6019261726501, 0.676663724472687, '', 'FLAG', '0', '1578.4188366638828', 0, 2272.92312479599, '0', '0', 11),
(50801, 2, 'Profit Center 2', 'Differentiated', '', 'Coatings', 109, 'Customer SoldTo 109', 12, 'Material 12', '3', 'Indent', 'Sales Person 48', 'EU', 'AP', 'Coatings', 'Product Family 121', 4400, 11935.8043240223, 8288.75300279326, -207.218825069831, '0', 0, 8081.53417772343, -2777.49045615332, 5304.04372157011, 82, '1. Low', 0.6019261726501, 0.676663724472687, '', 'FLAG', '0', '942.2226319558467', 0, 1356.80059001642, '0', '0', 11);

-- --------------------------------------------------------

--
-- Table structure for table `data_yearinfo`
--

CREATE TABLE `data_yearinfo` (
  `id` int(11) NOT NULL,
  `year` int(10) UNSIGNED DEFAULT NULL,
  `file_name` longtext COLLATE utf8_unicode_ci,
  `status` smallint(5) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `data_yearinfo`
--

INSERT INTO `data_yearinfo` (`id`, `year`, `file_name`, `status`) VALUES
(11, 2019, 'a4e51e3c-faf5-43a0-ad79-1389f566b856.xlsx', 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(10, 'authtoken', 'token'),
(5, 'contenttypes', 'contenttype'),
(8, 'data', 'pocketmargindata'),
(9, 'data', 'yearinfo'),
(6, 'sessions', 'session'),
(7, 'user', 'userinfo');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2018-12-02 20:50:53.908986'),
(2, 'auth', '0001_initial', '2018-12-02 20:50:55.616796'),
(3, 'admin', '0001_initial', '2018-12-02 20:50:56.008576'),
(4, 'admin', '0002_logentry_remove_auto_add', '2018-12-02 20:50:56.042124'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2018-12-02 20:50:56.057169'),
(6, 'contenttypes', '0002_remove_content_type_name', '2018-12-02 20:50:56.277945'),
(7, 'auth', '0002_alter_permission_name_max_length', '2018-12-02 20:50:56.448206'),
(8, 'auth', '0003_alter_user_email_max_length', '2018-12-02 20:50:56.609857'),
(9, 'auth', '0004_alter_user_username_opts', '2018-12-02 20:50:56.625302'),
(10, 'auth', '0005_alter_user_last_login_null', '2018-12-02 20:50:56.725393'),
(11, 'auth', '0006_require_contenttypes_0002', '2018-12-02 20:50:56.732294'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2018-12-02 20:50:56.761240'),
(13, 'auth', '0008_alter_user_username_max_length', '2018-12-02 20:50:56.914226'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2018-12-02 20:50:57.086462'),
(15, 'authtoken', '0001_initial', '2018-12-02 20:50:57.319909'),
(16, 'authtoken', '0002_auto_20160226_1747', '2018-12-02 20:50:57.548179'),
(17, 'data', '0001_initial', '2018-12-02 20:50:57.937455'),
(18, 'data', '0002_auto_20181202_2040', '2018-12-02 20:50:58.393298'),
(19, 'sessions', '0001_initial', '2018-12-02 20:50:58.503051'),
(20, 'user', '0001_initial', '2018-12-02 20:50:58.742888'),
(21, 'data', '0003_auto_20181204_1807', '2018-12-04 18:07:40.047301');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_userinfo`
--

CREATE TABLE `user_userinfo` (
  `id` int(11) NOT NULL,
  `security_code` longtext COLLATE utf8_unicode_ci NOT NULL,
  `type` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `user_userinfo`
--

INSERT INTO `user_userinfo` (`id`, `security_code`, `type`, `user_id`) VALUES
(1, '', 3, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD PRIMARY KEY (`key`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `data_pocketmargindata`
--
ALTER TABLE `data_pocketmargindata`
  ADD PRIMARY KEY (`id`),
  ADD KEY `data_pocketmargindata_year_info_id_a1c3bc04_fk_data_yearinfo_id` (`year_info_id`);

--
-- Indexes for table `data_yearinfo`
--
ALTER TABLE `data_yearinfo`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `user_userinfo`
--
ALTER TABLE `user_userinfo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `data_pocketmargindata`
--
ALTER TABLE `data_pocketmargindata`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=82513;

--
-- AUTO_INCREMENT for table `data_yearinfo`
--
ALTER TABLE `data_yearinfo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `user_userinfo`
--
ALTER TABLE `user_userinfo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `data_pocketmargindata`
--
ALTER TABLE `data_pocketmargindata`
  ADD CONSTRAINT `data_pocketmargindata_year_info_id_a1c3bc04_fk_data_yearinfo_id` FOREIGN KEY (`year_info_id`) REFERENCES `data_yearinfo` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `user_userinfo`
--
ALTER TABLE `user_userinfo`
  ADD CONSTRAINT `user_userinfo_user_id_778589e9_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
