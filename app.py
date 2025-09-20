from flask import Flask, render_template, request, redirect, url_for, flash, session
import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'iron_sight_armory_secret_key_change_in_production')

# Admin credentials (in production, use a proper authentication system)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'ISA3232'

# Customer storage (in production, use a database)
customers = []
customer_id_counter = 1

# In-memory storage for orders (in production, use a database)
orders = []
order_id_counter = 1

# Updated Product catalog with military categories - 30 products per category
PRODUCT_CATALOG = {
    'rifles': {
        'name': 'Rifles',
        'description': 'Precision rifles for professional applications',
        'products': [
            {'id': 'rf_001', 'name': 'M4A1 Carbine', 'price': 1299.99, 'description': 'Standard issue carbine with rail system'},
            {'id': 'rf_002', 'name': 'HK416 Assault Rifle', 'price': 2899.99, 'description': 'German precision assault rifle'},
            {'id': 'rf_003', 'name': 'FN SCAR-L', 'price': 3199.99, 'description': 'Special operations forces combat rifle'},
            {'id': 'rf_004', 'name': 'AK-74M', 'price': 1899.99, 'description': 'Modernized Kalashnikov rifle'},
            {'id': 'rf_005', 'name': 'Steyr AUG A3', 'price': 2299.99, 'description': 'Austrian bullpup assault rifle'},
            {'id': 'rf_006', 'name': 'IWI Tavor X95', 'price': 2599.99, 'description': 'Israeli bullpup assault rifle'},
            {'id': 'rf_007', 'name': 'SIG MCX Virtus', 'price': 2199.99, 'description': 'Modular assault rifle platform'},
            {'id': 'rf_008', 'name': 'FN SCAR-H', 'price': 3599.99, 'description': 'Heavy assault rifle 7.62x51mm'},
            {'id': 'rf_009', 'name': 'Galil ACE', 'price': 1799.99, 'description': 'Modern assault rifle system'},
            {'id': 'rf_010', 'name': 'CZ BREN 2', 'price': 2099.99, 'description': 'Czech modular assault rifle'},
            {'id': 'rf_011', 'name': 'AR-15 Block II', 'price': 1599.99, 'description': 'Special operations carbine'},
            {'id': 'rf_012', 'name': 'AK-12', 'price': 2199.99, 'description': 'Next generation Kalashnikov'},
            {'id': 'rf_013', 'name': 'G36K', 'price': 2399.99, 'description': 'German carbine assault rifle'},
            {'id': 'rf_014', 'name': 'FAMAS F1', 'price': 2799.99, 'description': 'French bullpup assault rifle'},
            {'id': 'rf_015', 'name': 'SA80 A2', 'price': 2299.99, 'description': 'British service rifle'},
            {'id': 'rf_016', 'name': 'Type 95', 'price': 1899.99, 'description': 'Chinese bullpup rifle'},
            {'id': 'rf_017', 'name': 'ARX-160', 'price': 2599.99, 'description': 'Italian modular assault rifle'},
            {'id': 'rf_018', 'name': 'VHS-2', 'price': 2199.99, 'description': 'Croatian bullpup rifle'},
            {'id': 'rf_019', 'name': 'MSBS Grot', 'price': 1999.99, 'description': 'Polish modular rifle system'},
            {'id': 'rf_020', 'name': 'AEK-971', 'price': 2399.99, 'description': 'Russian balanced recoil rifle'},
            {'id': 'rf_021', 'name': 'AN-94 Abakan', 'price': 2799.99, 'description': 'Russian hyperburst rifle'},
            {'id': 'rf_022', 'name': 'XM8 Prototype', 'price': 3299.99, 'description': 'Advanced modular rifle system'},
            {'id': 'rf_023', 'name': 'ACR Magpul', 'price': 2599.99, 'description': 'Adaptive combat rifle'},
            {'id': 'rf_024', 'name': 'IMBEL MD-97', 'price': 1799.99, 'description': 'Brazilian assault rifle'},
            {'id': 'rf_025', 'name': 'K2 Daewoo', 'price': 1999.99, 'description': 'South Korean service rifle'},
            {'id': 'rf_026', 'name': 'T91 Assault Rifle', 'price': 2199.99, 'description': 'Taiwanese combat rifle'},
            {'id': 'rf_027', 'name': 'INSAS Rifle', 'price': 1599.99, 'description': 'Indian small arms system'},
            {'id': 'rf_028', 'name': 'SG 550', 'price': 2899.99, 'description': 'Swiss precision assault rifle'},
            {'id': 'rf_029', 'name': 'AUG HBAR', 'price': 2699.99, 'description': 'Heavy barrel support variant'},
            {'id': 'rf_030', 'name': 'M16A4', 'price': 1499.99, 'description': 'Fourth generation battle rifle'}
        ]
    },
    'smgs': {
        'name': 'SMGs',
        'description': 'Submachine guns for close quarters operations',
        'products': [
            {'id': 'smg_001', 'name': 'MP5A5', 'price': 1899.99, 'description': 'Legendary German submachine gun'},
            {'id': 'smg_002', 'name': 'UMP-45', 'price': 1599.99, 'description': 'Compact .45 ACP submachine gun'},
            {'id': 'smg_003', 'name': 'P90 TR', 'price': 2199.99, 'description': 'Belgian personal defense weapon'},
            {'id': 'smg_004', 'name': 'Kriss Vector', 'price': 1799.99, 'description': 'Advanced recoil mitigation system'},
            {'id': 'smg_005', 'name': 'CZ Scorpion EVO 3', 'price': 1299.99, 'description': 'Czech compact submachine gun'},
            {'id': 'smg_006', 'name': 'MP7A1', 'price': 2299.99, 'description': 'German personal defense weapon'},
            {'id': 'smg_007', 'name': 'Uzi Pro', 'price': 1699.99, 'description': 'Israeli compact submachine gun'},
            {'id': 'smg_008', 'name': 'MP5K PDW', 'price': 1999.99, 'description': 'Compact variant of MP5'},
            {'id': 'smg_009', 'name': 'Mac-10', 'price': 899.99, 'description': 'Compact American submachine gun'},
            {'id': 'smg_010', 'name': 'Thompson M1A1', 'price': 1399.99, 'description': 'Classic American submachine gun'},
            {'id': 'smg_011', 'name': 'PPSh-41', 'price': 1199.99, 'description': 'Soviet wartime submachine gun'},
            {'id': 'smg_012', 'name': 'Sten Gun', 'price': 799.99, 'description': 'British wartime submachine gun'},
            {'id': 'smg_013', 'name': 'Sterling L2A3', 'price': 1099.99, 'description': 'British post-war submachine gun'},
            {'id': 'smg_014', 'name': 'MAT-49', 'price': 1299.99, 'description': 'French submachine gun'},
            {'id': 'smg_015', 'name': 'Beretta M12', 'price': 1399.99, 'description': 'Italian submachine gun'},
            {'id': 'smg_016', 'name': 'Carl Gustaf M/45', 'price': 1199.99, 'description': 'Swedish submachine gun'},
            {'id': 'smg_017', 'name': 'Star Z-70', 'price': 1099.99, 'description': 'Spanish submachine gun'},
            {'id': 'smg_018', 'name': 'FMK-3', 'price': 999.99, 'description': 'Argentine submachine gun'},
            {'id': 'smg_019', 'name': 'PM-63 RAK', 'price': 899.99, 'description': 'Polish machine pistol'},
            {'id': 'smg_020', 'name': 'Sa vz. 23', 'price': 1199.99, 'description': 'Czech submachine gun'},
            {'id': 'smg_021', 'name': 'PP-2000', 'price': 1599.99, 'description': 'Russian submachine gun'},
            {'id': 'smg_022', 'name': 'AEK-919K Kashtan', 'price': 1799.99, 'description': 'Russian compact SMG'},
            {'id': 'smg_023', 'name': 'Vityaz-SN', 'price': 1699.99, 'description': 'Russian 9mm submachine gun'},
            {'id': 'smg_024', 'name': 'QCW-05', 'price': 1399.99, 'description': 'Chinese submachine gun'},
            {'id': 'smg_025', 'name': 'K6-92', 'price': 1299.99, 'description': 'South Korean submachine gun'},
            {'id': 'smg_026', 'name': 'FAMAE SAF', 'price': 1199.99, 'description': 'Chilean submachine gun'},
            {'id': 'smg_027', 'name': 'B&T APC9', 'price': 2199.99, 'description': 'Swiss advanced SMG'},
            {'id': 'smg_028', 'name': 'SIG MPX', 'price': 1999.99, 'description': 'Modular submachine gun platform'},
            {'id': 'smg_029', 'name': 'LWRC SMG-45', 'price': 2299.99, 'description': 'American .45 ACP submachine gun'},
            {'id': 'smg_030', 'name': 'Honey Badger PDW', 'price': 2499.99, 'description': 'Compact personal defense weapon'}
        ]
    },
    'shotguns': {
        'name': 'Shotguns',
        'description': 'Tactical shotguns for breaching and close combat',
        'products': [
            {'id': 'sg_001', 'name': 'Benelli M4 Super 90', 'price': 1999.99, 'description': 'Semi-automatic combat shotgun'},
            {'id': 'sg_002', 'name': 'Remington 870 MCS', 'price': 899.99, 'description': 'Modular combat shotgun system'},
            {'id': 'sg_003', 'name': 'Mossberg 590A1', 'price': 799.99, 'description': 'Military specification pump shotgun'},
            {'id': 'sg_004', 'name': 'FN SLP Mark I', 'price': 1399.99, 'description': 'Self-loading police shotgun'},
            {'id': 'sg_005', 'name': 'AA-12', 'price': 4999.99, 'description': 'Full-auto combat shotgun'},
            {'id': 'sg_006', 'name': 'SPAS-12', 'price': 2199.99, 'description': 'Italian combat shotgun'},
            {'id': 'sg_007', 'name': 'Benelli M1014', 'price': 1799.99, 'description': 'Joint service combat shotgun'},
            {'id': 'sg_008', 'name': 'Winchester 1300 Defender', 'price': 699.99, 'description': 'Pump-action defense shotgun'},
            {'id': 'sg_009', 'name': 'Ithaca 37 Trench Gun', 'price': 899.99, 'description': 'Military trench shotgun'},
            {'id': 'sg_010', 'name': 'KSG Bullpup', 'price': 1199.99, 'description': 'Compact bullpup shotgun'},
            {'id': 'sg_011', 'name': 'Saiga-12', 'price': 1599.99, 'description': 'Russian semi-auto shotgun'},
            {'id': 'sg_012', 'name': 'Mossberg 500 Cruiser', 'price': 599.99, 'description': 'Compact pump shotgun'},
            {'id': 'sg_013', 'name': 'Beretta 1301 Tactical', 'price': 1299.99, 'description': 'Italian tactical shotgun'},
            {'id': 'sg_014', 'name': 'Franchi SPAS-15', 'price': 2499.99, 'description': 'Magazine-fed combat shotgun'},
            {'id': 'sg_015', 'name': 'Pancor Jackhammer', 'price': 3999.99, 'description': 'Experimental combat shotgun'},
            {'id': 'sg_016', 'name': 'Striker/Protecta', 'price': 2299.99, 'description': 'Revolving cylinder shotgun'},
            {'id': 'sg_017', 'name': 'M26 MASS', 'price': 1799.99, 'description': 'Modular accessory shotgun'},
            {'id': 'sg_018', 'name': 'Neostead 2000', 'price': 2199.99, 'description': 'South African bullpup shotgun'},
            {'id': 'sg_019', 'name': 'USAS-12', 'price': 3599.99, 'description': 'Automatic shotgun system'},
            {'id': 'sg_020', 'name': 'Vepr-12', 'price': 1399.99, 'description': 'Russian tactical shotgun'},
            {'id': 'sg_021', 'name': 'Fostech Origin-12', 'price': 1699.99, 'description': 'Semi-automatic combat shotgun'},
            {'id': 'sg_022', 'name': 'Typhoon Defense F12', 'price': 999.99, 'description': 'Turkish tactical shotgun'},
            {'id': 'sg_023', 'name': 'SRM 1216', 'price': 2799.99, 'description': 'Revolving shotgun system'},
            {'id': 'sg_024', 'name': 'Citadel RSS1', 'price': 799.99, 'description': 'Semi-auto tactical shotgun'},
            {'id': 'sg_025', 'name': 'Genesis Arms Gen-12', 'price': 1199.99, 'description': 'AK-pattern shotgun'},
            {'id': 'sg_026', 'name': 'Rock Island VR80', 'price': 899.99, 'description': 'Semi-automatic shotgun'},
            {'id': 'sg_027', 'name': 'Dissident Arms KL-12', 'price': 1499.99, 'description': 'Modular shotgun platform'},
            {'id': 'sg_028', 'name': 'DERYA MK-12', 'price': 1099.99, 'description': 'Turkish semi-auto shotgun'},
            {'id': 'sg_029', 'name': 'Black Aces Tactical Pro', 'price': 799.99, 'description': 'Bullpup shotgun system'},
            {'id': 'sg_030', 'name': 'Kalashnikov USA KS-12', 'price': 1299.99, 'description': 'AK-style shotgun platform'}
        ]
    },
    'snipers': {
        'name': 'Snipers',
        'description': 'Precision long-range sniper systems',
        'products': [
            {'id': 'sn_001', 'name': 'Barrett M82A1', 'price': 8999.99, 'description': '.50 BMG anti-materiel rifle'},
            {'id': 'sn_002', 'name': 'CheyTac M200', 'price': 12999.99, 'description': 'Long-range precision rifle system'},
            {'id': 'sn_003', 'name': 'Accuracy International AWM', 'price': 6799.99, 'description': 'British precision sniper rifle'},
            {'id': 'sn_004', 'name': 'Remington M24 SWS', 'price': 4999.99, 'description': 'Sniper weapon system'},
            {'id': 'sn_005', 'name': 'DSR-50', 'price': 9999.99, 'description': 'German .50 BMG sniper rifle'},
            {'id': 'sn_006', 'name': 'Barrett M107A1', 'price': 11999.99, 'description': 'Advanced .50 cal sniper rifle'},
            {'id': 'sn_007', 'name': 'PGM 338', 'price': 8799.99, 'description': 'French precision rifle'},
            {'id': 'sn_008', 'name': 'Sako TRG-42', 'price': 5999.99, 'description': 'Finnish sniper rifle'},
            {'id': 'sn_009', 'name': 'McMillan TAC-50', 'price': 9499.99, 'description': 'Canadian long-range rifle'},
            {'id': 'sn_010', 'name': 'FN Ballista', 'price': 7999.99, 'description': 'Modular sniper weapon system'},
            {'id': 'sn_011', 'name': 'Victrix Armaments Gladius', 'price': 6999.99, 'description': 'Italian precision rifle'},
            {'id': 'sn_012', 'name': 'Savage 110 BA', 'price': 3999.99, 'description': 'American precision rifle'},
            {'id': 'sn_013', 'name': 'Howa M1500 APC', 'price': 3499.99, 'description': 'Japanese precision rifle'},
            {'id': 'sn_014', 'name': 'Tikka T3x TAC A1', 'price': 4299.99, 'description': 'Finnish tactical rifle'},
            {'id': 'sn_015', 'name': 'Steyr HS .50', 'price': 8499.99, 'description': 'Austrian anti-materiel rifle'},
            {'id': 'sn_016', 'name': 'Blaser R93 LRS2', 'price': 7299.99, 'description': 'German long-range system'},
            {'id': 'sn_017', 'name': 'M40A5', 'price': 5499.99, 'description': 'USMC sniper rifle'},
            {'id': 'sn_018', 'name': 'MK 13 Mod 7', 'price': 6799.99, 'description': 'Navy SEAL sniper rifle'},
            {'id': 'sn_019', 'name': 'L115A3 Long Range Rifle', 'price': 7999.99, 'description': 'British military sniper rifle'},
            {'id': 'sn_020', 'name': 'PSG1', 'price': 8999.99, 'description': 'German precision rifle'},
            {'id': 'sn_021', 'name': 'MSG90', 'price': 7999.99, 'description': 'German marksman rifle'},
            {'id': 'sn_022', 'name': 'FR F2', 'price': 5999.99, 'description': 'French military sniper rifle'},
            {'id': 'sn_023', 'name': 'AW50', 'price': 9999.99, 'description': 'British .50 cal sniper rifle'},
            {'id': 'sn_024', 'name': 'VSS Vintorez', 'price': 6499.99, 'description': 'Russian suppressed sniper rifle'},
            {'id': 'sn_025', 'name': 'SVD Dragunov', 'price': 4999.99, 'description': 'Soviet designated marksman rifle'},
            {'id': 'sn_026', 'name': 'SV-98', 'price': 3999.99, 'description': 'Russian police sniper rifle'},
            {'id': 'sn_027', 'name': 'Type 88', 'price': 4499.99, 'description': 'Chinese sniper rifle'},
            {'id': 'sn_028', 'name': 'JNG-90', 'price': 5999.99, 'description': 'Spanish precision rifle'},
            {'id': 'sn_029', 'name': 'M2010 ESR', 'price': 7499.99, 'description': 'Enhanced sniper rifle'},
            {'id': 'sn_030', 'name': 'MK14 EBR', 'price': 5499.99, 'description': 'Enhanced battle rifle'}
        ]
    },
    'explosives': {
        'name': 'Explosives',
        'description': 'Demolition and breach charges',
        'products': [
            {'id': 'exp_001', 'name': 'C4 Demolition Kit', 'price': 2999.99, 'description': 'Professional demolition package'},
            {'id': 'exp_002', 'name': 'Breaching Charges', 'price': 1499.99, 'description': 'Door and wall breaching system'},
            {'id': 'exp_003', 'name': 'Semtex Package', 'price': 3499.99, 'description': 'High-performance plastic explosive'},
            {'id': 'exp_004', 'name': 'Thermite Grenades', 'price': 899.99, 'description': 'Anti-material incendiary devices'},
            {'id': 'exp_005', 'name': 'Claymore Mines', 'price': 1999.99, 'description': 'Directional anti-personnel mines'},
            {'id': 'exp_006', 'name': 'TNT Blocks', 'price': 1299.99, 'description': 'Traditional trinitrotoluene explosive'},
            {'id': 'exp_007', 'name': 'RDX Charges', 'price': 2199.99, 'description': 'High-explosive demolition charges'},
            {'id': 'exp_008', 'name': 'PETN Cord', 'price': 799.99, 'description': 'Detonating cord system'},
            {'id': 'exp_009', 'name': 'Shape Charges', 'price': 3299.99, 'description': 'Directed explosive charges'},
            {'id': 'exp_010', 'name': 'M18A1 Claymore', 'price': 2299.99, 'description': 'Directional fragmentation mine'},
            {'id': 'exp_011', 'name': 'M67 Fragmentation Grenade', 'price': 199.99, 'description': 'Standard fragmentation grenade'},
            {'id': 'exp_012', 'name': 'M84 Stun Grenade', 'price': 149.99, 'description': 'Flashbang stun grenade'},
            {'id': 'exp_013', 'name': 'Smoke Grenades', 'price': 99.99, 'description': 'Tactical concealment grenades'},
            {'id': 'exp_014', 'name': 'Incendiary Grenades', 'price': 249.99, 'description': 'AN-M14 TH3 incendiary'},
            {'id': 'exp_015', 'name': 'CS Gas Grenades', 'price': 179.99, 'description': 'Chemical irritant grenades'},
            {'id': 'exp_016', 'name': 'Satchel Charges', 'price': 1999.99, 'description': 'Portable demolition charges'},
            {'id': 'exp_017', 'name': 'Linear Charges', 'price': 2499.99, 'description': 'Cutting charge systems'},
            {'id': 'exp_018', 'name': 'IED Simulators', 'price': 599.99, 'description': 'Training explosive devices'},
            {'id': 'exp_019', 'name': 'Bangalore Torpedoes', 'price': 1799.99, 'description': 'Wire obstacle clearing charges'},
            {'id': 'exp_020', 'name': 'APOBS Charges', 'price': 3999.99, 'description': 'Anti-personnel obstacle breaching'},
            {'id': 'exp_021', 'name': 'Cratering Charges', 'price': 4999.99, 'description': 'Runway denial munitions'},
            {'id': 'exp_022', 'name': 'Composition B', 'price': 1699.99, 'description': 'Military grade explosive'},
            {'id': 'exp_023', 'name': 'Amatol Charges', 'price': 1399.99, 'description': 'Alternative explosive compound'},
            {'id': 'exp_024', 'name': 'Plastic Explosive PE4', 'price': 2799.99, 'description': 'British military explosive'},
            {'id': 'exp_025', 'name': 'Octol Charges', 'price': 2199.99, 'description': 'High-performance explosive'},
            {'id': 'exp_026', 'name': 'Cyclotol Mix', 'price': 1899.99, 'description': 'Enhanced explosive composition'},
            {'id': 'exp_027', 'name': 'PBXN-109', 'price': 3299.99, 'description': 'Insensitive munitions explosive'},
            {'id': 'exp_028', 'name': 'HMX Charges', 'price': 3799.99, 'description': 'Ultra-high explosive compound'},
            {'id': 'exp_029', 'name': 'Tantalum Charges', 'price': 4999.99, 'description': 'Exotic metal enhanced explosives'},
            {'id': 'exp_030', 'name': 'EFP Warheads', 'price': 5999.99, 'description': 'Explosively formed penetrator'}
        ]
    },
    'armor': {
        'name': 'Armor',
        'description': 'Protective equipment and body armor',
        'products': [
            {'id': 'arm_001', 'name': 'Level IV Plate Carrier', 'price': 899.99, 'description': 'Ceramic plate body armor system'},
            {'id': 'arm_002', 'name': 'Kevlar Helmet', 'price': 599.99, 'description': 'Ballistic protection helmet'},
            {'id': 'arm_003', 'name': 'Tactical Vest System', 'price': 1299.99, 'description': 'Modular tactical load bearing vest'},
            {'id': 'arm_004', 'name': 'EOD Bomb Suit', 'price': 4999.99, 'description': 'Explosive ordnance disposal suit'},
            {'id': 'arm_005', 'name': 'Combat Boots', 'price': 299.99, 'description': 'Military grade tactical footwear'},
            {'id': 'arm_006', 'name': 'IOTV Body Armor', 'price': 1599.99, 'description': 'Improved outer tactical vest'},
            {'id': 'arm_007', 'name': 'PASGT Helmet', 'price': 399.99, 'description': 'Personnel armor system helmet'},
            {'id': 'arm_008', 'name': 'Dragon Skin Vest', 'price': 6999.99, 'description': 'Flexible ceramic armor'},
            {'id': 'arm_009', 'name': 'FAST Helmet', 'price': 799.99, 'description': 'Future assault shell technology'},
            {'id': 'arm_010', 'name': 'Interceptor Body Armor', 'price': 1199.99, 'description': 'Military body armor system'},
            {'id': 'arm_011', 'name': 'MICH Helmet', 'price': 699.99, 'description': 'Modular integrated combat helmet'},
            {'id': 'arm_012', 'name': 'Ceramic Trauma Plates', 'price': 499.99, 'description': 'Stand-alone armor plates'},
            {'id': 'arm_013', 'name': 'Kevlar Soft Armor', 'price': 799.99, 'description': 'Flexible ballistic protection'},
            {'id': 'arm_014', 'name': 'Combat Knee Pads', 'price': 149.99, 'description': 'Tactical knee protection'},
            {'id': 'arm_015', 'name': 'Ballistic Glasses', 'price': 199.99, 'description': 'Eye protection system'},
            {'id': 'arm_016', 'name': 'Nomex Flight Suit', 'price': 399.99, 'description': 'Fire-resistant flight clothing'},
            {'id': 'arm_017', 'name': 'Level IIIA Vest', 'price': 699.99, 'description': 'Concealed body armor'},
            {'id': 'arm_018', 'name': 'Ballistic Shield', 'price': 1999.99, 'description': 'Portable ballistic protection'},
            {'id': 'arm_019', 'name': 'Riot Helmet', 'price': 299.99, 'description': 'Crowd control protection'},
            {'id': 'arm_020', 'name': 'Tactical Gloves', 'price': 99.99, 'description': 'Cut-resistant tactical gloves'},
            {'id': 'arm_021', 'name': 'Ghillie Suit', 'price': 499.99, 'description': 'Camouflage concealment system'},
            {'id': 'arm_022', 'name': 'ACH Helmet', 'price': 599.99, 'description': 'Advanced combat helmet'},
            {'id': 'arm_023', 'name': 'Plate Carrier Vest', 'price': 399.99, 'description': 'Minimalist armor carrier'},
            {'id': 'arm_024', 'name': 'Battle Belt System', 'price': 249.99, 'description': 'Tactical equipment belt'},
            {'id': 'arm_025', 'name': 'Ballistic Mask', 'price': 899.99, 'description': 'Face protection system'},
            {'id': 'arm_026', 'name': 'Shoulder Armor', 'price': 199.99, 'description': 'Deltoid protection system'},
            {'id': 'arm_027', 'name': 'Throat Protection', 'price': 149.99, 'description': 'Ballistic collar system'},
            {'id': 'arm_028', 'name': 'Groin Protection', 'price': 179.99, 'description': 'Lower torso armor'},
            {'id': 'arm_029', 'name': 'Arm Guards', 'price': 199.99, 'description': 'Forearm protection system'},
            {'id': 'arm_030', 'name': 'Full Body Suit', 'price': 9999.99, 'description': 'Complete protection system'}
        ]
    },
    'attachments': {
        'name': 'Attachments',
        'description': 'Weapon accessories and tactical attachments',
        'products': [
            {'id': 'att_001', 'name': 'ACOG 4x32 Scope', 'price': 1299.99, 'description': 'Advanced combat optical gunsight'},
            {'id': 'att_002', 'name': 'PEQ-15 Laser Designator', 'price': 1899.99, 'description': 'IR laser aiming module'},
            {'id': 'att_003', 'name': 'M203 Grenade Launcher', 'price': 3999.99, 'description': 'Under-barrel grenade launcher'},
            {'id': 'att_004', 'name': 'Suppressor Kit', 'price': 899.99, 'description': 'Sound suppression system'},
            {'id': 'att_005', 'name': 'Tactical Foregrip', 'price': 199.99, 'description': 'Vertical foregrip with bipod'},
            {'id': 'att_006', 'name': 'EOTech Holographic Sight', 'price': 649.99, 'description': 'Holographic weapon sight'},
            {'id': 'att_007', 'name': 'Trijicon RMR', 'price': 749.99, 'description': 'Ruggedized miniature reflex sight'},
            {'id': 'att_008', 'name': 'M68 CCO Sight', 'price': 499.99, 'description': 'Close combat optic'},
            {'id': 'att_009', 'name': 'Night Vision Scope', 'price': 2999.99, 'description': 'Advanced night vision optics'},
            {'id': 'att_010', 'name': 'Thermal Imaging Scope', 'price': 4999.99, 'description': 'Thermal weapon sight'},
            {'id': 'att_011', 'name': 'Bipod System', 'price': 299.99, 'description': 'Adjustable weapon bipod'},
            {'id': 'att_012', 'name': 'Flashlight Mount', 'price': 149.99, 'description': 'Tactical weapon light'},
            {'id': 'att_013', 'name': 'Laser Pointer', 'price': 399.99, 'description': 'Visible laser aiming device'},
            {'id': 'att_014', 'name': 'Muzzle Brake', 'price': 199.99, 'description': 'Recoil reduction device'},
            {'id': 'att_015', 'name': 'Compensator', 'price': 249.99, 'description': 'Muzzle rise compensation'},
            {'id': 'att_016', 'name': 'Rail System', 'price': 349.99, 'description': 'Modular accessory rail'},
            {'id': 'att_017', 'name': 'Sling Mount', 'price': 79.99, 'description': 'Weapon carrying system'},
            {'id': 'att_018', 'name': 'Cheek Rest', 'price': 159.99, 'description': 'Adjustable stock cheek piece'},
            {'id': 'att_019', 'name': 'Buttpad', 'price': 89.99, 'description': 'Recoil absorption pad'},
            {'id': 'att_020', 'name': 'Iron Sights Backup', 'price': 179.99, 'description': 'Backup iron sight set'},
            {'id': 'att_021', 'name': 'Rangefinder', 'price': 799.99, 'description': 'Laser rangefinding device'},
            {'id': 'att_022', 'name': 'Wind Meter', 'price': 299.99, 'description': 'Ballistic wind measurement'},
            {'id': 'att_023', 'name': 'Magazine Coupler', 'price': 49.99, 'description': 'Dual magazine connector'},
            {'id': 'att_024', 'name': 'Quick Detach Mount', 'price': 199.99, 'description': 'Rapid release optic mount'},
            {'id': 'att_025', 'name': 'Scope Rings', 'price': 129.99, 'description': 'Precision scope mounting rings'},
            {'id': 'att_026', 'name': 'Canting Meter', 'price': 99.99, 'description': 'Weapon cant indication device'},
            {'id': 'att_027', 'name': 'Trigger Upgrade', 'price': 399.99, 'description': 'Precision trigger system'},
            {'id': 'att_028', 'name': 'Barrel Extension', 'price': 599.99, 'description': 'Extended barrel system'},
            {'id': 'att_029', 'name': 'Gas Block', 'price': 149.99, 'description': 'Adjustable gas system'},
            {'id': 'att_030', 'name': 'Charging Handle', 'price': 189.99, 'description': 'Enhanced charging handle'}
        ]
    },
    'ground_vehicles': {
        'name': 'Ground Vehicles',
        'description': 'Armored and tactical ground vehicles',
        'products': [
            {'id': 'gv_001', 'name': 'HMMWV Armored', 'price': 89999.99, 'description': 'Up-armored military utility vehicle'},
            {'id': 'gv_002', 'name': 'M1A2 Abrams Tank', 'price': 6999999.99, 'description': 'Main battle tank system'},
            {'id': 'gv_003', 'name': 'LAV-25', 'price': 2999999.99, 'description': 'Light armored reconnaissance vehicle'},
            {'id': 'gv_004', 'name': 'MRAP Vehicle', 'price': 1499999.99, 'description': 'Mine-resistant ambush protected vehicle'},
            {'id': 'gv_005', 'name': 'M-ATV', 'price': 899999.99, 'description': 'All-terrain tactical vehicle'},
            {'id': 'gv_006', 'name': 'Bradley Fighting Vehicle', 'price': 4299999.99, 'description': 'Infantry fighting vehicle'},
            {'id': 'gv_007', 'name': 'Stryker APC', 'price': 3499999.99, 'description': 'Armored personnel carrier'},
            {'id': 'gv_008', 'name': 'M113 APC', 'price': 1999999.99, 'description': 'Classic armored personnel carrier'},
            {'id': 'gv_009', 'name': 'JLTV', 'price': 799999.99, 'description': 'Joint light tactical vehicle'},
            {'id': 'gv_010', 'name': 'Buffalo MRAP', 'price': 1899999.99, 'description': 'Route clearance vehicle'},
            {'id': 'gv_011', 'name': 'Cougar MRAP', 'price': 1699999.99, 'description': 'Category I MRAP vehicle'},
            {'id': 'gv_012', 'name': 'MaxxPro MRAP', 'price': 1599999.99, 'description': 'International MaxxPro vehicle'},
            {'id': 'gv_013', 'name': 'RG-31 Nyala', 'price': 999999.99, 'description': 'South African armored vehicle'},
            {'id': 'gv_014', 'name': 'Bushmaster PMV', 'price': 1299999.99, 'description': 'Protected mobility vehicle'},
            {'id': 'gv_015', 'name': 'Fennek Reconnaissance', 'price': 2199999.99, 'description': 'European reconnaissance vehicle'},
            {'id': 'gv_016', 'name': 'Pandur APC', 'price': 2799999.99, 'description': 'Austrian wheeled APC'},
            {'id': 'gv_017', 'name': 'BTR-80 APC', 'price': 1799999.99, 'description': 'Russian armored personnel carrier'},
            {'id': 'gv_018', 'name': 'BMP-3 IFV', 'price': 3299999.99, 'description': 'Russian infantry fighting vehicle'},
            {'id': 'gv_019', 'name': 'Leopard 2A7 Tank', 'price': 7999999.99, 'description': 'German main battle tank'},
            {'id': 'gv_020', 'name': 'Challenger 2 Tank', 'price': 6799999.99, 'description': 'British main battle tank'},
            {'id': 'gv_021', 'name': 'T-90 Tank', 'price': 4999999.99, 'description': 'Russian main battle tank'},
            {'id': 'gv_022', 'name': 'Merkava Mk4 Tank', 'price': 5999999.99, 'description': 'Israeli main battle tank'},
            {'id': 'gv_023', 'name': 'Type 99 Tank', 'price': 4799999.99, 'description': 'Chinese main battle tank'},
            {'id': 'gv_024', 'name': 'K2 Black Panther', 'price': 8499999.99, 'description': 'South Korean main battle tank'},
            {'id': 'gv_025', 'name': 'AMX Leclerc Tank', 'price': 6499999.99, 'description': 'French main battle tank'},
            {'id': 'gv_026', 'name': 'Centauro Tank Destroyer', 'price': 3999999.99, 'description': 'Italian wheeled tank destroyer'},
            {'id': 'gv_027', 'name': 'M109 Paladin', 'price': 4299999.99, 'description': 'Self-propelled howitzer'},
            {'id': 'gv_028', 'name': 'HIMARS Launcher', 'price': 5999999.99, 'description': 'High mobility artillery rocket'},
            {'id': 'gv_029', 'name': 'MLRS System', 'price': 7999999.99, 'description': 'Multiple launch rocket system'},
            {'id': 'gv_030', 'name': 'Caesar Artillery', 'price': 5499999.99, 'description': 'French self-propelled howitzer'}
        ]
    },
    'air_vehicles': {
        'name': 'Air Vehicles',
        'description': 'Aircraft and aerial systems',
        'products': [
            {'id': 'av_001', 'name': 'AH-64 Apache', 'price': 31999999.99, 'description': 'Attack helicopter system'},
            {'id': 'av_002', 'name': 'UH-60 Black Hawk', 'price': 21999999.99, 'description': 'Multi-mission helicopter'},
            {'id': 'av_003', 'name': 'F-35 Lightning II', 'price': 89999999.99, 'description': 'Fifth-generation fighter aircraft'},
            {'id': 'av_004', 'name': 'C-130 Hercules', 'price': 67999999.99, 'description': 'Tactical airlift aircraft'},
            {'id': 'av_005', 'name': 'A-10 Thunderbolt II', 'price': 18999999.99, 'description': 'Close air support aircraft'},
            {'id': 'av_006', 'name': 'F-22 Raptor', 'price': 149999999.99, 'description': 'Fifth-generation air superiority fighter'},
            {'id': 'av_007', 'name': 'F-16 Fighting Falcon', 'price': 29999999.99, 'description': 'Multi-role fighter aircraft'},
            {'id': 'av_008', 'name': 'F/A-18 Super Hornet', 'price': 69999999.99, 'description': 'Carrier-based fighter'},
            {'id': 'av_009', 'name': 'AV-8B Harrier II', 'price': 24999999.99, 'description': 'Vertical takeoff attack aircraft'},
            {'id': 'av_010', 'name': 'CH-47 Chinook', 'price': 38999999.99, 'description': 'Heavy-lift transport helicopter'},
            {'id': 'av_011', 'name': 'AH-1Z Viper', 'price': 31999999.99, 'description': 'Twin-engine attack helicopter'},
            {'id': 'av_012', 'name': 'V-22 Osprey', 'price': 89999999.99, 'description': 'Tiltrotor aircraft'},
            {'id': 'av_013', 'name': 'C-17 Globemaster III', 'price': 217999999.99, 'description': 'Strategic airlift aircraft'},
            {'id': 'av_014', 'name': 'KC-135 Stratotanker', 'price': 39999999.99, 'description': 'Aerial refueling aircraft'},
            {'id': 'av_015', 'name': 'B-2 Spirit', 'price': 2199999999.99, 'description': 'Stealth strategic bomber'},
            {'id': 'av_016', 'name': 'B-1B Lancer', 'price': 283999999.99, 'description': 'Supersonic strategic bomber'},
            {'id': 'av_017', 'name': 'AC-130 Spectre', 'price': 132999999.99, 'description': 'Heavily armed ground-attack aircraft'},
            {'id': 'av_018', 'name': 'E-3 Sentry AWACS', 'price': 270999999.99, 'description': 'Airborne warning and control system'},
            {'id': 'av_019', 'name': 'RC-135 Rivet Joint', 'price': 242999999.99, 'description': 'Electronic intelligence aircraft'},
            {'id': 'av_020', 'name': 'U-2 Dragon Lady', 'price': 1899999.99, 'description': 'High-altitude reconnaissance aircraft'},
            {'id': 'av_021', 'name': 'Eurofighter Typhoon', 'price': 124999999.99, 'description': 'European multi-role fighter'},
            {'id': 'av_022', 'name': 'Rafale Fighter', 'price': 89999999.99, 'description': 'French multi-role fighter'},
            {'id': 'av_023', 'name': 'Gripen Fighter', 'price': 69999999.99, 'description': 'Swedish multi-role fighter'},
            {'id': 'av_024', 'name': 'Su-35 Flanker-E', 'price': 84999999.99, 'description': 'Russian air superiority fighter'},
            {'id': 'av_025', 'name': 'MiG-35 Fulcrum-F', 'price': 49999999.99, 'description': 'Russian multi-role fighter'},
            {'id': 'av_026', 'name': 'J-20 Mighty Dragon', 'price': 119999999.99, 'description': 'Chinese stealth fighter'},
            {'id': 'av_027', 'name': 'Mi-24 Hind', 'price': 18999999.99, 'description': 'Russian attack helicopter'},
            {'id': 'av_028', 'name': 'Ka-52 Alligator', 'price': 32999999.99, 'description': 'Russian reconnaissance attack helicopter'},
            {'id': 'av_029', 'name': 'Tiger HAP', 'price': 31999999.99, 'description': 'European attack helicopter'},
            {'id': 'av_030', 'name': 'AW159 Wildcat', 'price': 29999999.99, 'description': 'Multi-role military helicopter'}
        ]
    },
    'water_vehicles': {
        'name': 'Water Vehicles',
        'description': 'Naval and amphibious vessels',
        'products': [
            {'id': 'wv_001', 'name': 'Mark V SOC', 'price': 1999999.99, 'description': 'Special operations craft'},
            {'id': 'wv_002', 'name': 'RHIB Assault Boat', 'price': 299999.99, 'description': 'Rigid hull inflatable boat'},
            {'id': 'wv_003', 'name': 'LCAC Hovercraft', 'price': 22999999.99, 'description': 'Landing craft air cushion'},
            {'id': 'wv_004', 'name': 'Submarine Hunter', 'price': 45999999.99, 'description': 'Fast attack craft'},
            {'id': 'wv_005', 'name': 'Combat Swimmer DPV', 'price': 89999.99, 'description': 'Diver propulsion vehicle'},
            {'id': 'wv_006', 'name': 'LCU Landing Craft', 'price': 4999999.99, 'description': 'Utility landing craft'},
            {'id': 'wv_007', 'name': 'AAV-7 Amphibian', 'price': 6999999.99, 'description': 'Amphibious assault vehicle'},
            {'id': 'wv_008', 'name': 'Riverine Command Boat', 'price': 1499999.99, 'description': 'River patrol craft'},
            {'id': 'wv_009', 'name': 'CB90 Fast Assault Craft', 'price': 2999999.99, 'description': 'Swedish combat boat'},
            {'id': 'wv_010', 'name': 'Special Operations Craft', 'price': 3999999.99, 'description': 'Stealth insertion vessel'},
            {'id': 'wv_011', 'name': 'Fast Attack Craft', 'price': 19999999.99, 'description': 'High-speed missile boat'},
            {'id': 'wv_012', 'name': 'Patrol Boat River', 'price': 899999.99, 'description': 'Vietnam-era patrol craft'},
            {'id': 'wv_013', 'name': 'Cyclone-class Patrol', 'price': 24999999.99, 'description': 'Coastal patrol vessel'},
            {'id': 'wv_014', 'name': 'SURC Speed Boat', 'price': 499999.99, 'description': 'Small unit riverine craft'},
            {'id': 'wv_015', 'name': 'Zodiac Milpro', 'price': 149999.99, 'description': 'Military inflatable boat'},
            {'id': 'wv_016', 'name': 'LCM Landing Craft', 'price': 2999999.99, 'description': 'Mechanized landing craft'},
            {'id': 'wv_017', 'name': 'LCVP Higgins Boat', 'price': 199999.99, 'description': 'Vehicle/personnel landing craft'},
            {'id': 'wv_018', 'name': 'Mine Countermeasure', 'price': 89999999.99, 'description': 'Naval mine clearing vessel'},
            {'id': 'wv_019', 'name': 'Coastal Defense Boat', 'price': 12999999.99, 'description': 'Shore patrol vessel'},
            {'id': 'wv_020', 'name': 'Torpedo Boat', 'price': 15999999.99, 'description': 'Fast attack torpedo boat'},
            {'id': 'wv_021', 'name': 'Gunboat', 'price': 7999999.99, 'description': 'Armed naval patrol vessel'},
            {'id': 'wv_022', 'name': 'Corvette', 'price': 199999999.99, 'description': 'Small warship'},
            {'id': 'wv_023', 'name': 'Frigate', 'price': 599999999.99, 'description': 'Medium naval warship'},
            {'id': 'wv_024', 'name': 'Destroyer', 'price': 1799999999.99, 'description': 'Large naval warship'},
            {'id': 'wv_025', 'name': 'Submarine', 'price': 2999999999.99, 'description': 'Attack submarine'},
            {'id': 'wv_026', 'name': 'Amphibious Transport', 'price': 999999999.99, 'description': 'Dock landing ship'},
            {'id': 'wv_027', 'name': 'Aircraft Carrier', 'price': 12999999999.99, 'description': 'Naval aviation platform'},
            {'id': 'wv_028', 'name': 'Cruiser', 'price': 4999999999.99, 'description': 'Heavy naval warship'},
            {'id': 'wv_029', 'name': 'Littoral Combat Ship', 'price': 699999999.99, 'description': 'Modular coastal warship'},
            {'id': 'wv_030', 'name': 'Battleship', 'price': 9999999999.99, 'description': 'Heavy armored warship'}
        ]
    },
    'anti_aircraft': {
        'name': 'Anti-Aircraft Vehicles',
        'description': 'Air defense systems and vehicles',
        'products': [
            {'id': 'aa_001', 'name': 'Patriot Missile System', 'price': 9999999.99, 'description': 'Surface-to-air missile defense'},
            {'id': 'aa_002', 'name': 'CIWS Phalanx', 'price': 5999999.99, 'description': 'Close-in weapons system'},
            {'id': 'aa_003', 'name': 'MANPADS Stinger', 'price': 399999.99, 'description': 'Portable air defense system'},
            {'id': 'aa_004', 'name': 'Iron Dome Battery', 'price': 49999999.99, 'description': 'Missile defense system'},
            {'id': 'aa_005', 'name': 'Gepard SPAAG', 'price': 7999999.99, 'description': 'Self-propelled anti-aircraft gun'},
            {'id': 'aa_006', 'name': 'S-400 Triumf', 'price': 19999999.99, 'description': 'Russian long-range SAM system'},
            {'id': 'aa_007', 'name': 'Aegis Combat System', 'price': 199999999.99, 'description': 'Naval air defense system'},
            {'id': 'aa_008', 'name': 'THAAD System', 'price': 999999999.99, 'description': 'Terminal high altitude area defense'},
            {'id': 'aa_009', 'name': 'Arrow 3 Interceptor', 'price': 299999999.99, 'description': 'Exo-atmospheric interceptor'},
            {'id': 'aa_010', 'name': 'Pantsir-S1', 'price': 13999999.99, 'description': 'Combined gun-missile system'},
            {'id': 'aa_011', 'name': 'Roland SAM', 'price': 4999999.99, 'description': 'Short-range surface-to-air missile'},
            {'id': 'aa_012', 'name': 'Rapier System', 'price': 2999999.99, 'description': 'British surface-to-air missile'},
            {'id': 'aa_013', 'name': 'Crotale SAM', 'price': 3999999.99, 'description': 'French short-range SAM'},
            {'id': 'aa_014', 'name': 'Avenger System', 'price': 1999999.99, 'description': 'Humvee-mounted air defense'},
            {'id': 'aa_015', 'name': 'Linebacker System', 'price': 3499999.99, 'description': 'Bradley-based air defense'},
            {'id': 'aa_016', 'name': 'Chaparral SAM', 'price': 1799999.99, 'description': 'Self-propelled SAM launcher'},
            {'id': 'aa_017', 'name': 'Hawk SAM System', 'price': 7999999.99, 'description': 'Medium-range surface-to-air'},
            {'id': 'aa_018', 'name': 'Nike Hercules', 'price': 12999999.99, 'description': 'Long-range SAM system'},
            {'id': 'aa_019', 'name': 'SA-6 Gainful', 'price': 4999999.99, 'description': 'Soviet mobile SAM system'},
            {'id': 'aa_020', 'name': 'SA-8 Gecko', 'price': 3999999.99, 'description': 'Soviet short-range SAM'},
            {'id': 'aa_021', 'name': 'SA-11 Gadfly', 'price': 6999999.99, 'description': 'Soviet medium-range SAM'},
            {'id': 'aa_022', 'name': 'SA-15 Gauntlet', 'price': 8999999.99, 'description': 'Russian point defense system'},
            {'id': 'aa_023', 'name': 'NASAMS System', 'price': 19999999.99, 'description': 'Norwegian advanced SAM'},
            {'id': 'aa_024', 'name': 'SAMP/T System', 'price': 89999999.99, 'description': 'European theater air defense'},
            {'id': 'aa_025', 'name': 'Skyguard System', 'price': 5999999.99, 'description': 'Swiss air defense system'},
            {'id': 'aa_026', 'name': 'Oerlikon Millennium', 'price': 7999999.99, 'description': 'Naval gun system'},
            {'id': 'aa_027', 'name': 'SeaRAM System', 'price': 9999999.99, 'description': 'Ship self-defense system'},
            {'id': 'aa_028', 'name': 'C-RAM System', 'price': 14999999.99, 'description': 'Counter rocket artillery mortar'},
            {'id': 'aa_029', 'name': 'Goalkeeper CIWS', 'price': 6999999.99, 'description': 'Dutch close-in weapon system'},
            {'id': 'aa_030', 'name': 'AK-630 CIWS', 'price': 4999999.99, 'description': 'Soviet naval gun system'}
        ]
    },
    'drones': {
        'name': 'Drones',
        'description': 'Unmanned aerial vehicles and systems',
        'products': [
            {'id': 'dr_001', 'name': 'MQ-9 Reaper', 'price': 16999999.99, 'description': 'Hunter-killer unmanned aircraft'},
            {'id': 'dr_002', 'name': 'RQ-11 Raven', 'price': 89999.99, 'description': 'Small tactical UAV system'},
            {'id': 'dr_003', 'name': 'Global Hawk', 'price': 131999999.99, 'description': 'High-altitude surveillance drone'},
            {'id': 'dr_004', 'name': 'Switchblade 300', 'price': 199999.99, 'description': 'Loitering munition system'},
            {'id': 'dr_005', 'name': 'Black Hornet Nano', 'price': 39999.99, 'description': 'Micro reconnaissance UAV'},
            {'id': 'dr_006', 'name': 'MQ-1 Predator', 'price': 4999999.99, 'description': 'Medium-altitude surveillance UAV'},
            {'id': 'dr_007', 'name': 'X-47B UCAS', 'price': 279999999.99, 'description': 'Unmanned combat air system'},
            {'id': 'dr_008', 'name': 'RQ-4 Global Hawk', 'price': 221999999.99, 'description': 'High-altitude long endurance UAV'},
            {'id': 'dr_009', 'name': 'Shadow 200', 'price': 1299999.99, 'description': 'Tactical unmanned aircraft'},
            {'id': 'dr_010', 'name': 'ScanEagle', 'price': 699999.99, 'description': 'Small long-endurance UAV'},
            {'id': 'dr_011', 'name': 'Puma AE', 'price': 249999.99, 'description': 'Hand-launched surveillance UAV'},
            {'id': 'dr_012', 'name': 'Wasp AE', 'price': 49999.99, 'description': 'Micro air vehicle'},
            {'id': 'dr_013', 'name': 'Hunter UAV', 'price': 24999999.99, 'description': 'Multi-role unmanned aircraft'},
            {'id': 'dr_014', 'name': 'Fire Scout', 'price': 15999999.99, 'description': 'Unmanned helicopter system'},
            {'id': 'dr_015', 'name': 'Warrior Alpha', 'price': 3999999.99, 'description': 'Extended range UAV'},
            {'id': 'dr_016', 'name': 'Hermes 450', 'price': 7999999.99, 'description': 'Medium-altitude long endurance'},
            {'id': 'dr_017', 'name': 'Heron UAV', 'price': 9999999.99, 'description': 'Multi-payload surveillance UAV'},
            {'id': 'dr_018', 'name': 'Bayraktar TB2', 'price': 4999999.99, 'description': 'Turkish attack drone'},
            {'id': 'dr_019', 'name': 'Wing Loong II', 'price': 2999999.99, 'description': 'Chinese MALE UAV'},
            {'id': 'dr_020', 'name': 'CH-4 Rainbow', 'price': 3499999.99, 'description': 'Chinese medium-altitude UAV'},
            {'id': 'dr_021', 'name': 'Orion UAV', 'price': 12999999.99, 'description': 'Russian medium-altitude UAV'},
            {'id': 'dr_022', 'name': 'nEUROn UCAV', 'price': 199999999.99, 'description': 'European stealth combat drone'},
            {'id': 'dr_023', 'name': 'Taranis UCAV', 'price': 249999999.99, 'description': 'British stealth combat UAV'},
            {'id': 'dr_024', 'name': 'Loyal Wingman', 'price': 39999999.99, 'description': 'Unmanned teaming system'},
            {'id': 'dr_025', 'name': 'Kratos XQ-58', 'price': 2999999.99, 'description': 'Low-cost attritable aircraft'},
            {'id': 'dr_026', 'name': 'Coyote UAV', 'price': 199999.99, 'description': 'Expendable tube-launched UAV'},
            {'id': 'dr_027', 'name': 'Phoenix Ghost', 'price': 599999.99, 'description': 'Single-use attack drone'},
            {'id': 'dr_028', 'name': 'Harop Loitering', 'price': 2999999.99, 'description': 'Anti-radiation loitering munition'},
            {'id': 'dr_029', 'name': 'Harpy Drone', 'price': 1999999.99, 'description': 'Anti-radar loitering weapon'},
            {'id': 'dr_030', 'name': 'IAI Searcher', 'price': 5999999.99, 'description': 'Multi-mission surveillance UAV'}
        ]
    },
    'missiles': {
        'name': 'Missiles',
        'description': 'Guided missile systems and ordnance',
        'products': [
            {'id': 'ms_001', 'name': 'Hellfire AGM-114', 'price': 199999.99, 'description': 'Air-to-ground missile system'},
            {'id': 'ms_002', 'name': 'Tomahawk Cruise', 'price': 1999999.99, 'description': 'Long-range cruise missile'},
            {'id': 'ms_003', 'name': 'Javelin FGM-148', 'price': 299999.99, 'description': 'Fire-and-forget anti-tank missile'},
            {'id': 'ms_004', 'name': 'THAAD Interceptor', 'price': 9999999.99, 'description': 'Theater defense missile'},
            {'id': 'ms_005', 'name': 'Harpoon Anti-Ship', 'price': 1299999.99, 'description': 'All-weather anti-ship missile'},
            {'id': 'ms_006', 'name': 'Patriot PAC-3', 'price': 4999999.99, 'description': 'Surface-to-air interceptor'},
            {'id': 'ms_007', 'name': 'AMRAAM AIM-120', 'price': 1799999.99, 'description': 'Advanced medium-range air-to-air'},
            {'id': 'ms_008', 'name': 'Sidewinder AIM-9X', 'price': 599999.99, 'description': 'Short-range air-to-air missile'},
            {'id': 'ms_009', 'name': 'JASSM Cruise Missile', 'price': 1399999.99, 'description': 'Joint air-to-surface standoff'},
            {'id': 'ms_010', 'name': 'Storm Shadow', 'price': 1199999.99, 'description': 'Anglo-French cruise missile'},
            {'id': 'ms_011', 'name': 'Trident II D5', 'price': 59999999.99, 'description': 'Submarine-launched ballistic missile'},
            {'id': 'ms_012', 'name': 'Minuteman III', 'price': 69999999.99, 'description': 'Intercontinental ballistic missile'},
            {'id': 'ms_013', 'name': 'Aegis SM-3', 'price': 29999999.99, 'description': 'Standard missile interceptor'},
            {'id': 'ms_014', 'name': 'TOW Anti-Tank', 'price': 189999.99, 'description': 'Tube-launched optically tracked'},
            {'id': 'ms_015', 'name': 'Dragon Anti-Tank', 'price': 99999.99, 'description': 'Medium-range anti-tank missile'},
            {'id': 'ms_016', 'name': 'Milan Anti-Tank', 'price': 149999.99, 'description': 'European anti-tank guided weapon'},
            {'id': 'ms_017', 'name': 'Spike ATGM', 'price': 299999.99, 'description': 'Israeli fire-and-forget missile'},
            {'id': 'ms_018', 'name': 'Brimstone Missile', 'price': 399999.99, 'description': 'British air-to-surface missile'},
            {'id': 'ms_019', 'name': 'ATACMS Missile', 'price': 1999999.99, 'description': 'Army tactical missile system'},
            {'id': 'ms_020', 'name': 'HIMARS Rocket', 'price': 899999.99, 'description': 'High mobility artillery rocket'},
            {'id': 'ms_021', 'name': 'MLRS Rocket', 'price': 499999.99, 'description': 'Multiple launch rocket system'},
            {'id': 'ms_022', 'name': 'Exocet Anti-Ship', 'price': 1099999.99, 'description': 'French anti-ship missile'},
            {'id': 'ms_023', 'name': 'BrahMos Cruise', 'price': 2999999.99, 'description': 'Indo-Russian supersonic cruise'},
            {'id': 'ms_024', 'name': 'Kalibr Cruise', 'price': 1799999.99, 'description': 'Russian land-attack cruise missile'},
            {'id': 'ms_025', 'name': 'Kinzhal Hypersonic', 'price': 4999999.99, 'description': 'Russian air-launched ballistic'},
            {'id': 'ms_026', 'name': 'Zircon Hypersonic', 'price': 7999999.99, 'description': 'Russian hypersonic cruise missile'},
            {'id': 'ms_027', 'name': 'DF-21D Anti-Ship', 'price': 9999999.99, 'description': 'Chinese carrier-killer missile'},
            {'id': 'ms_028', 'name': 'Shahab-3 Ballistic', 'price': 14999999.99, 'description': 'Iranian medium-range ballistic'},
            {'id': 'ms_029', 'name': 'Agni-V ICBM', 'price': 49999999.99, 'description': 'Indian intercontinental ballistic'},
            {'id': 'ms_030', 'name': 'Topol-M ICBM', 'price': 89999999.99, 'description': 'Russian road-mobile ICBM'}
        ]
    }
}

def find_product(product_id):
    """Find a product by ID across all categories"""
    for category in PRODUCT_CATALOG.values():
        for product in category['products']:
            if product['id'] == product_id:
                return product
    return None

def find_category_by_product_id(product_id):
    """Find the category that contains a specific product"""
    for category_id, category in PRODUCT_CATALOG.items():
        for product in category['products']:
            if product['id'] == product_id:
                return category_id
    return None

def is_admin_logged_in():
    """Check if admin is logged in"""
    return session.get('admin_logged_in', False)

def admin_required(f):
    """Decorator to require admin login"""
    def decorated_function(*args, **kwargs):
        if not is_admin_logged_in():
            flash('Admin login required', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def find_customer(discord_id):
    """Find customer by Discord ID"""
    for customer in customers:
        if customer['discord_id'] == discord_id:
            return customer
    return None

def is_customer_logged_in():
    """Check if customer is logged in"""
    return session.get('customer_logged_in', False)

def customer_required(f):
    """Decorator to require customer login"""
    def decorated_function(*args, **kwargs):
        if not is_customer_logged_in():
            flash('Please login to place orders', 'error')
            return redirect(url_for('customer_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/')
def welcome():
    return render_template('welcome.html', vacancy_settings=vacancy_settings)

@app.route('/shop')
def index():
    search_query = request.args.get('search', '').strip()
    search_results = []
    
    if search_query:
        # Search through all products
        for category_id, category in PRODUCT_CATALOG.items():
            for product in category['products']:
                if (search_query.lower() in product['name'].lower() or 
                    search_query.lower() in product['description'].lower()):
                    search_results.append({
                        'product': product,
                        'category_id': category_id,
                        'category_name': category['name']
                    })
    
    return render_template('index.html', catalog=PRODUCT_CATALOG, 
                         search_query=search_query, search_results=search_results, vacancy_settings=vacancy_settings)

@app.route('/category/<category_id>')
def category_page(category_id):
    if category_id not in PRODUCT_CATALOG:
        flash('Category not found', 'error')
        return redirect(url_for('index'))
    
    category = PRODUCT_CATALOG[category_id]
    return render_template('category.html', category=category, category_id=category_id)

@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    if request.method == 'POST':
        global customer_id_counter
        
        discord_id = request.form.get('discord_id', '').strip()
        roleplay_is = request.form.get('roleplay_is', '').strip()
        password = request.form.get('password', '').strip()
        
        if not all([discord_id, roleplay_is, password]):
            flash('All fields are required', 'error')
            return render_template('customer_register.html')
        
        # Check if Discord ID already exists
        if find_customer(discord_id):
            flash('Discord ID already registered', 'error')
            return render_template('customer_register.html')
        
        # Create new customer
        customer = {
            'id': customer_id_counter,
            'discord_id': discord_id,
            'roleplay_is': roleplay_is,
            'password': password,
            'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        customers.append(customer)
        customer_id_counter += 1
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('customer_login'))
    
    return render_template('customer_register.html')

@app.route('/customer/login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'POST':
        discord_id = request.form.get('discord_id', '').strip()
        password = request.form.get('password', '').strip()
        
        customer = find_customer(discord_id)
        if customer and customer['password'] == password:
            session['customer_logged_in'] = True
            session['customer_id'] = customer['id']
            session['customer_discord_id'] = customer['discord_id']
            flash(f'Welcome back, {customer["roleplay_is"]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid Discord ID or password', 'error')
    
    return render_template('customer_login.html')

@app.route('/customer/logout')
def customer_logout():
    session.pop('customer_logged_in', None)
    session.pop('customer_id', None)
    session.pop('customer_discord_id', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/customer/orders')
@customer_required
def customer_orders():
    customer_id = session.get('customer_id')
    customer_orders = [order for order in orders if order['customer_id'] == customer_id]
    return render_template('customer_orders.html', orders=customer_orders, vacancy_settings=vacancy_settings)

@app.route('/order', methods=['POST'])
@customer_required
def place_order():
    global order_id_counter
    
    product_id = request.form.get('product_id')
    quantity_str = request.form.get('quantity', '1')
    
    # Get customer data from session
    customer_id = session.get('customer_id')
    customer = next((c for c in customers if c['id'] == customer_id), None)
    
    if not customer:
        flash('Customer not found', 'error')
        return redirect(url_for('customer_login'))
    
    # Validate quantity
    try:
        quantity = int(quantity_str)
        if quantity < 1:
            quantity = 1
    except ValueError:
        quantity = 1
    
    if not product_id:
        flash('Please select a product', 'error')
        return redirect(request.referrer or url_for('index'))
    
    product = find_product(product_id)
    if not product:
        flash('Product not found', 'error')
        return redirect(request.referrer or url_for('index'))
    
    # Find the category for redirect
    category_id = find_category_by_product_id(product_id)
    
    # Create order
    order = {
        'id': order_id_counter,
        'customer_id': customer['id'],
        'customer_discord_id': customer['discord_id'],
        'customer_roleplay_is': customer['roleplay_is'],
        'product_id': product_id,
        'product_name': product['name'],
        'price': product['price'],
        'quantity': quantity,
        'total': product['price'] * quantity,
        'status': 'pending',
        'category': PRODUCT_CATALOG[category_id]['name'] if category_id else 'Unknown',
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    orders.append(order)
    order_id_counter += 1
    
    flash(f'Order placed successfully! Order ID: #{order["id"]}', 'success')
    
    # Redirect back to the category page if possible
    if category_id:
        return redirect(url_for('category_page', category_id=category_id))
    else:
        return redirect(url_for('index'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Admin login successful', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin_login.html', vacancy_settings=vacancy_settings)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Admin logged out successfully', 'success')
    return redirect(url_for('index'))

# Vacancy management (in production, use a database)
vacancy_settings = {
    'title': '🎯 WANT TO APPLY FOR A POSITION?',
    'description': 'Contact Owner',
    'contact_info': 'https://discord.gg/6wpgXJAkcv',
    'image_url': '',
    'enabled': True
}

@app.route('/orders')
@admin_required
def view_orders():
    return render_template('orders.html', orders=orders, vacancy_settings=vacancy_settings)

@app.route('/order/<int:order_id>/confirm', methods=['POST'])
@admin_required
def confirm_order(order_id):
    for order in orders:
        if order['id'] == order_id:
            order['status'] = 'confirmed'
            flash(f'Order #{order_id} has been confirmed', 'success')
            break
    else:
        flash(f'Order #{order_id} not found', 'error')
    
    return redirect(url_for('view_orders'))

@app.route('/order/<int:order_id>/deny', methods=['POST'])
@admin_required
def deny_order(order_id):
    for order in orders:
        if order['id'] == order_id:
            order['status'] = 'denied'
            flash(f'Order #{order_id} has been denied', 'warning')
            break
    else:
        flash(f'Order #{order_id} not found', 'error')
    
    return redirect(url_for('view_orders'))

@app.route('/admin/vacancy', methods=['GET', 'POST'])
@admin_required
def manage_vacancy():
    if request.method == 'POST':
        vacancy_settings['title'] = request.form.get('title', '').strip()
        vacancy_settings['description'] = request.form.get('description', '').strip()
        vacancy_settings['contact_info'] = request.form.get('contact_info', '').strip()
        vacancy_settings['image_url'] = request.form.get('image_url', '').strip()
        vacancy_settings['enabled'] = 'enabled' in request.form
        
        flash('Vacancy settings updated successfully!', 'success')
        return redirect(url_for('manage_vacancy'))
    
    return render_template('admin_vacancy.html', vacancy_settings=vacancy_settings)

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    # Calculate order statistics
    total_orders = len(orders)
    pending_orders = len([o for o in orders if o['status'] == 'pending'])
    confirmed_orders = len([o for o in orders if o['status'] == 'confirmed'])
    denied_orders = len([o for o in orders if o['status'] == 'denied'])
    
    # Calculate total revenue from confirmed orders
    total_revenue = sum(o['total'] for o in orders if o['status'] == 'confirmed')
    
    # Get recent orders (last 5)
    recent_orders = orders[-5:] if len(orders) >= 5 else orders
    
    stats = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'confirmed_orders': confirmed_orders,
        'denied_orders': denied_orders,
        'total_revenue': total_revenue,
        'total_customers': len(customers),
        'recent_orders': recent_orders
    }
    
    return render_template('admin_dashboard.html', stats=stats, vacancy_settings=vacancy_settings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)