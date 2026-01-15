# season
season_map = {
    'fa19': 'F19',
    'sp21': 'S21', 'fa21': 'F21', 'fa22': 'F22',
    'sp23': 'S23', 'fa23': 'F23', 'sp24': 'S24', 'fa24': 'F24'
}
season_list = ['fa19', 'sp21', 'fa21', 'fa22', 'sp23', 'fa23','sp24', 'fa24']
season_display = [season_map[s] for s in season_list]

# division
division_dict = {
    'Northeast': [
        'Boston-Worcester-Providence_MA-RI-NH',
        'NewYork-Newark_NY-NJ-CT-PA',
        'Philadelphia-Reading-Camden_PA-NJ-DE-MD'
    ],
    'Midwest': [
        'Chicago-Naperville_IL-IN-WI',
        'Cleveland-Akron-Canton_OH',
        'Detroit-Warren-AnnArbor_MI',
        'StLouis-StCharles-Farmington_MO-IL'
    ],
    'South': [
        'Atlanta--Athens-ClarkeCounty--SandySprings_GA-AL',
        'Dallas-FortWorth_TX-OK',
        'Houston-Pasadena_TX',
        'Orlando-Lakeland-Deltona_FL'
    ],
    'West': [
        'LosAngeles-LongBeach_CA',
        'Phoenix-Mesa_AZ',
        'Sacramento-Roseville_CA',
        'SanJose-SanFrancisco-Oakland_CA'
    ]
}

# CSA
acr_list = [
    'atl', 'bos', 'chi', 'clv', 'dal', 'dtr', 'hou',
    'la', 'ny', 'orl', 'phi', 'pnx', 'sac', 'sf', 'stl'
]

acr_city_dict = {
    'atl': 'Atlanta',
    'bos': 'Boston',
    'chi': 'Chicago',
    'clv': 'Cleveland',
    'dal': 'Dallas',
    'dtr': 'Detroit',
    'hou': 'Houston',
    'la':  'Los Angeles',
    'ny':  'New York',
    'orl': 'Orlando',
    'phi': 'Philadelphia',
    'pnx': 'Phoenix',
    'sac': 'Sacramento',
    'sf':  'San Jose',
    'stl': 'St. Louis'
}

acr_color = {
    'atl': '#C8AD7F', 'bos': 'lightblue', 'chi': 'red',
    'clv': 'orchid', 'dal': 'crimson', 'dtr': '#CECECE',
    'hou': 'green', 'la': 'orange', 'ny': 'cyan',
    'orl': 'pink', 'phi': 'purple', 'pnx': '#9F8C76',
    'sac': 'coral', 'sf': 'blue', 'stl': 'brown'
}

acr_marker = {
    'atl': 'h', 'bos': 'P', 'chi': 'x', 'clv': 'd',
    'dal': 's', 'dtr': 'v', 'hou': '8', 'la': 'o',
    'ny': '*', 'orl': '^', 'phi': '+', 'pnx': '>',
    'sac': '<', 'sf': 'D', 'stl': 'H'
}

acr_csa_dict = {
    'atl': 'Atlanta--Athens-ClarkeCounty--SandySprings_GA-AL',
    'bos': 'Boston-Worcester-Providence_MA-RI-NH',
    'chi': 'Chicago-Naperville_IL-IN-WI',
    'clv': 'Cleveland-Akron-Canton_OH',
    'dal': 'Dallas-FortWorth_TX-OK',
    'dtr': 'Detroit-Warren-AnnArbor_MI',
    'hou': 'Houston-Pasadena_TX',
    'la':  'LosAngeles-LongBeach_CA',
    'ny':  'NewYork-Newark_NY-NJ-CT-PA',
    'orl': 'Orlando-Lakeland-Deltona_FL',
    'phi': 'Philadelphia-Reading-Camden_PA-NJ-DE-MD',
    'pnx': 'Phoenix-Mesa_AZ',
    'sac': 'Sacramento-Roseville_CA',
    'sf':  'SanJose-SanFrancisco-Oakland_CA',
    'stl': 'StLouis-StCharles-Farmington_MO-IL'
}

csa_city_dict = {
    'Atlanta--Athens-ClarkeCounty--SandySprings_GA-AL': 'Atlanta',
    'Boston-Worcester-Providence_MA-RI-NH': 'Boston',
    'Chicago-Naperville_IL-IN-WI': 'Chicago',
    'Cleveland-Akron-Canton_OH': 'Cleveland',
    'Dallas-FortWorth_TX-OK': 'Dallas',
    'Detroit-Warren-AnnArbor_MI': 'Detroit',
    'Houston-Pasadena_TX': 'Houston',
    'LosAngeles-LongBeach_CA': 'Los Angeles',
    'NewYork-Newark_NY-NJ-CT-PA': 'New York',
    'Orlando-Lakeland-Deltona_FL': 'Orlando',
    'Philadelphia-Reading-Camden_PA-NJ-DE-MD': 'Philadelphia',
    'Phoenix-Mesa_AZ': 'Phoenix',
    'Sacramento-Roseville_CA': 'Sacramento',
    'SanJose-SanFrancisco-Oakland_CA': 'San Jose',
    'StLouis-StCharles-Farmington_MO-IL': 'St. Louis'
}

csa_order = []
for region in ['Northeast', 'Midwest', 'South', 'West']:
    csa_order.extend(division_dict[region])

csa_color = {
    'Atlanta--Athens-ClarkeCounty--SandySprings_GA-AL': '#C8AD7F',
    'Boston-Worcester-Providence_MA-RI-NH': 'lightblue',
    'Chicago-Naperville_IL-IN-WI': 'red',
    'Cleveland-Akron-Canton_OH': 'orchid',
    'Dallas-FortWorth_TX-OK': 'crimson',
    'Detroit-Warren-AnnArbor_MI': '#CECECE',
    'Houston-Pasadena_TX': 'green',
    'LosAngeles-LongBeach_CA': 'orange',
    'NewYork-Newark_NY-NJ-CT-PA': 'cyan',
    'Orlando-Lakeland-Deltona_FL': 'pink',
    'Philadelphia-Reading-Camden_PA-NJ-DE-MD': 'purple',
    'Phoenix-Mesa_AZ': '#9F8C76',
    'Sacramento-Roseville_CA': 'coral',
    'SanJose-SanFrancisco-Oakland_CA': 'blue',
    'StLouis-StCharles-Farmington_MO-IL': 'brown'
}

csa_marker = {
    'Atlanta--Athens-ClarkeCounty--SandySprings_GA-AL': 'h',
    'Boston-Worcester-Providence_MA-RI-NH': 'P',
    'Chicago-Naperville_IL-IN-WI': 'x',
    'Cleveland-Akron-Canton_OH': 'd',
    'Dallas-FortWorth_TX-OK': 's',
    'Detroit-Warren-AnnArbor_MI': 'v',
    'Houston-Pasadena_TX': '8',
    'LosAngeles-LongBeach_CA': 'o',
    'NewYork-Newark_NY-NJ-CT-PA': '*',
    'Orlando-Lakeland-Deltona_FL': '^',
    'Philadelphia-Reading-Camden_PA-NJ-DE-MD': '+',
    'Phoenix-Mesa_AZ': '>',
    'Sacramento-Roseville_CA': '<',
    'SanJose-SanFrancisco-Oakland_CA': 'D',
    'StLouis-StCharles-Farmington_MO-IL': 'H'
}

csa_acr_map = {v: k for k, v in acr_csa_dict.items()}

# NAICS
naics_dict = {
    'total_naics_11': 'Agriculture, Forestry, Fishing and Hunting',
    'total_naics_21': 'Mining, Quarrying, and Oil and Gas Extraction',
    'total_naics_22': 'Utilities',
    'total_naics_23': 'Construction',
    'total_naics_31-33': 'Manufacturing',
    'total_naics_42': 'Wholesale Trade',
    'total_naics_44-45': 'Retail Trade',
    'total_naics_48-49': 'Transportation and Warehousing',
    'total_naics_51': 'Information',
    'total_naics_52': 'Finance and Insurance',
    'total_naics_53': 'Real Estate and Rental and Leasing',
    'total_naics_54': 'Professional, Scientific, and Technical Services',
    'total_naics_55': 'Management of Companies and Enterprises',
    'total_naics_56': 'Administrative and Support Services',
    'total_naics_61': 'Educational Services',
    'total_naics_62': 'Health Care and Social Assistance',
    'total_naics_71': 'Arts, Entertainment, and Recreation',
    'total_naics_72': 'Accommodation and Food Services',
    'total_naics_81': 'Other Services',
    'total_naics_92': 'Public Administration'
}
naics_sector = list(naics_dict.keys())

naics_color = [
    '#F2D7D5', '#FDE2CE', '#F8F0DC', '#D8E2DC', '#CCD5AE', '#DCE2F0',
    '#D3CCE3', '#EAD5DC', '#F5E8C7', '#EFE7BC', '#E3E8D2', '#F0F1EC',
    '#FCE2DB', '#F5CAC3', '#F4F0DE', '#E6E1DE', '#CDEEDE', '#F9CF93',
    '#DAD7CD', '#C7D9B7', '#D2E6D6'
]

naics_color_dict = {
    'total_naics_62': '#F2D7D5',
    'total_naics_44-45': '#FDE2CE',
    'total_naics_31-33': '#D8E2DC',
    'total_naics_61': '#F8F0DC',
    'total_naics_54': '#CCD5AE',
    'total_naics_72': '#DCE2F0',
    'total_naics_23': '#D3CCE3',
    'total_naics_48-49': '#EAD5DC',
    'total_naics_52': '#F5E8C7',
    'total_naics_81': '#EFE7BC',
    'total_naics_56': '#E3E8D2',
    'total_naics_92': '#F0F1EC',
    'total_naics_42': '#FCE2DB',
    'total_naics_51': '#F5CAC3',
    'total_naics_71': '#F4F0DE',
    'total_naics_53': '#E6E1DE',
    'total_naics_22': '#CDEEDE',
    'total_naics_11': '#F9CF93',
    'total_naics_21': '#DAD7CD',
    'total_naics_55': '#C7D9B7'
}

sector_class = {
    'Agriculture, Forestry, Fishing and Hunting': 'primary',
    'Mining, Quarrying, and Oil and Gas Extraction': 'primary',
    'Construction': 'secondary',
    'Manufacturing': 'secondary',
    'Utilities': 'tertiary',
    'Wholesale Trade': 'tertiary',
    'Retail Trade': 'tertiary',
    'Transportation and Warehousing': 'tertiary',
    'Finance and Insurance': 'tertiary',
    'Real Estate and Rental and Leasing': 'tertiary',
    'Administrative and Support Services': 'tertiary',
    'Educational Services': 'tertiary',
    'Health Care and Social Assistance': 'tertiary',
    'Arts, Entertainment, and Recreation': 'tertiary',
    'Accommodation and Food Services': 'tertiary',
    'Other Services': 'tertiary',
    'Public Administration': 'tertiary',
    'Information': 'quaternary',
    'Professional, Scientific, and Technical Services': 'quaternary',
    'Management of Companies and Enterprises': 'quaternary'
}

sector_markers = {
    'primary': 'o',
    'secondary': 's',
    'tertiary': '^',
    'quaternary': 'D'
}

naics2colors = {
   'Health Care and Social Assistance': '#F2D7D5',
   'Retail Trade': '#FDE2CE',
   'Educational Services': '#F8F0DC',
   'Manufacturing': '#D8E2DC',
   'Professional, Scientific, and Technical Services': '#CCD5AE',
   'Accommodation and Food Services': '#DCE2F0',
   'Construction': '#D3CCE3',
   'Transportation and Warehousing': '#EAD5DC',
   'Finance and Insurance': '#F5E8C7',
   'Other Services': '#EFE7BC',
   'Administrative and Support Services': '#E3E8D2',
   'Public Administration': '#F0F1EC',
   'Wholesale Trade': '#FCE2DB',
   'Information': '#F5CAC3',
   'Arts, Entertainment, and Recreation': '#F4F0DE',
   'Real Estate and Rental and Leasing': '#E6E1DE',
   'Utilities': '#CDEEDE',
   'Agriculture, Forestry, Fishing and Hunting': '#F9CF93',
   'Mining, Quarrying, and Oil and Gas Extraction': '#DAD7CD',
   'Management of Companies and Enterprises': '#C7D9B7',
}

name_mapping = {
   'Other Services (except Public Administration)': 'Other Services',
   'Administrative and Support and Waste Management and Remediation Services': 'Administrative and Support Services'
}

abbr_mapping = {
    'Professional, Scientific, and Technical Services': 'Science/Tech',
    'Finance and Insurance': 'Finance',
    'Information': 'Information',
    'Manufacturing': 'Manufacturing',
    'Management of Companies and Enterprises': 'Management',
    'Public Administration': 'Public Administration',
    'Real Estate and Rental and Leasing': 'Real Estate',
    'Retail Trade': 'Retail Trade',
    'Utilities': 'Utilities',
    'Wholesale Trade': 'Wholesale Trade',
    'Mining, Quarrying, and Oil and Gas Extraction': 'Mining',
    'Educational Services': 'Education',
    'Arts, Entertainment, and Recreation': 'Arts',
    'Transportation and Warehousing': 'Transportation',
    'Health Care and Social Assistance': 'Health Care',
    'Agriculture, Forestry, Fishing and Hunting': 'Agriculture',
    'Construction': 'Construction',
    'Accommodation and Food Services': 'Accommodation/Food',
    'Other Services': 'Other Services',
    'Administrative and Support Services': 'Admin Services'
}

# raincloud
season_order = ['S21','F21', 'F22', 'S23', 'F23', 'S24', 'F24']
violin_colors = ["#F2D57F", '#B2D28E', '#F393C4', '#BAB7D9', '#ECAE80', '#e5e5e5', '#92C5DD']
box_colors = ["#E6AA03",'#66A51F', '#E6298A', '#7570B2', '#D95E01', '#bfbfbf', '#3D93C4']

# regression
groups = {
    'mobility_behavior': ['dtmt', 'dauto_trip', 'davg_rg'],
    'urban_form': ['deltaKS_f19', 'pop_gini_f19', 'uci_f19'],
    'vkt_baseline': ['vmt_f19']
}

labels = {
    'dtmt': r'$\Delta$ TKT', 'dauto_trip': r'$\Delta$ Car Trip', 'davg_rg': r'$\Delta R_g$',
    'vmt_f19': r'Baseline $VKT$', 'deltaKS_f19': r'Baseline $\Delta KS$', 'uci_f19': r'Baseline $UCI$', 'pop_gini_f19': r'Baseline $PopGini$'
}

colors = {'mobility_behavior': '#8b97c5', 'urban_form': '#262624', 'vkt_baseline': '#bebebe'}