import re

month_name= 'Oct_2025'
from_= "2025-10-01"
to_ = "2025-10-30"

crime_list=['forge', 'forged', 'forgery', 'drug trafficking', 'drug', 'poaching', 'poacher', 'prostitution', 'trafficking', 'bribe', 'corruption', 'insider trading', 'organ trafficking', 'cyber crime', 'scam', 'chit fund scam', 'it scam', 'nse scam', 'bse scam', 'recruitment scam', 'online scam', 'investment scam', 'smuggling', 'smuggle', 'hair smuggling', 'wildlife smuggling', 'cattle smuggling', 'gold smuggling', 'fraud', 'online fraud', 'cyber fraud', 'bank fraud', 'job fraud', 'gst fraud', 'input tax credit fraud', 'loan fraud', 'housing fraud', 'financial fraud', 'e-fraud', 'crypto fraud', 'cryptocurrency fraud', 'crypto-currency fraud', 'investment fraud', 'extorsion', 'ransom', 'kidnap', 'cheating', 'money-laundering', 'money laundering', 'gst evasion', 'tax evasion', 'terror activity', 'terrorist', 'robbery', 'robber', 'arms racket', 'illegal mining', 'hawala', 'violation', 'murder', 'black marketting', 'riot', 'counterfeit note', 'fake note', 'fake currency', 'counterfeit currency', 'fake notes', 'illegal conversion', 'drug trafficking']

lea_regex=re.compile('( \(?DGGI\)? | \(?DRI\)? | \(?IRDA\)? | \(?DVAC\)? | \(?CID\)? | \(?CBI\)? | \(?ED\)? | \(?NIA\)? | \(?CBDT\)? | \(?NCB\)? | \(?SEBI\)? | \(?CBEC\)? | \(?NCB\)? | \(?RBI\)? | \(?MCA\)? | \(?MEA\)? | \(?MHA\)? | \(?DGFT\)? | \(?IB\)? |DIRECTORATE OF ENFORCEMENT|ENFORCEMENT DIRECTORATE|CENTRAL BOARD OF DIRECT TAXES|DIRECTORATE OF REVENUE INTELLIGENCE|DIRECTORATE GENERAL OF GST INTELLIGENCE|CENTRAL BUREAU OF INVESTIGATION|NATIONAL INVESTIGATION AGENCY|NARCOTICS CONTROL BUREAU|SERIOUS FRAUD INVESTIGATION OFFICE|FOREIGNERS DIVISION|CENTRAL ECONOMIC INTELLIGENCE BUREAU|INTELLIGENCE BUREAU|RESEARCH AND ANALYSIS WING|NATIONAL SECURITY COUNCIL SECRETARIAT|RESERVE BANK OF INDIA|SECURITIES AND EXCHANGE BOARD OF INDIA|INSURANCE REGULATORY AND DEVELOPMENT AUTHORITY|BUREAU OF IMMIGRATION|MINISTRY OF EXTERNAL AFFAIRS|MINISTRY OF CORPORATE AFFAIRS|EGMONT|CENTRAL BOARD OF EXCISE AND CUSTOMS|MINISTRY OF HOME AFFAIRS|DIRECTORATE GENERAL OF FOREIGN TRADE|DIRECTORATE OF INCOME TAX|CENTRAL VIGILANCE COMMISSION|DIRECTORATE OF VIGILANCE AND ANTI(-)?CORRUPTION|DIRECTORATE GENERAL OF GST INTELLIGENCE|DIRECTORATE OF REVENUE INTELLIGENCE|INSURANCE REGULATORY AND DEVELOPMENT AUTHORITY)')

rename_lea={'ED': 'ENFORCEMENT DIRECTORATE',
'DIRECTORATE OF ENFORCEMENT': 'ENFORCEMENT DIRECTORATE',
'NIA':'NATIONAL INVESTIGATION AGENCY',
'CBDT':'CENTRAL BOARD OF DIRECT TAXES',
'NCB':'NARCOTICS CONTROL BUREAU' ,
'SEBI': 'SECURITIES AND EXCHANGE BOARD OF INDIA',
'CBEC':'CENTRAL BOARD OF EXCISE AND CUSTOMS' ,
'NCB': 'NARCOTICS CONTROL BUREAU',
'RBI': 'RESERVE BANK OF INDIA',
'MCA': 'MINISTRY OF CORPORATE AFFAIRS',
'MEA':'MINISTRY OF EXTERNAL AFFAIRS',
'MHA': 'MINISTRY OF HOME AFFAIRS',
'DGFT':'DIRECTORATE GENERAL OF FOREIGN TRADE',
'IB': 'INTELLIGENCE BUREAU',
'CBI': 'CENTRAL BUREAU OF INVESTIGATION',
'CID':'CRIMINAL INVESTIGATION DEPARTMENT',
'DVAC': 'DIRECTORATE OF VIGILANCE AND ANTI CORRUPTION',
'DGGI' : 'DIRECTORATE GENERAL OF GST INTELLIGENCE',
'DRI':'DIRECTORATE OF REVENUE INTELLIGENCE',
'IRDA': 'INSURANCE REGULATORY AND DEVELOPMENT AUTHORITY'
           }

news_providers=['ECONOMICTIMES.INDIATIMES.COM', 'ENGLISH.LOKMAT.COM', 'ANINEWS.IN', 'INDIANEXPRESS.COM', 'TIMESOFINDIA.INDIATIMES.COM', 'HINDUSTANTIMES.COM', 'INDIATODAY.IN', 'NEWINDIANEXPRESS.COM', 'REPUBLICWORLD.COM', 'TIMESNOWNEWS.COM', 'TRIBUNEINDIA.COM', 'THEPRINT.IN', 'BUSINESS-STANDARD.COM', 'BUSINESSTODAY.IN', 'FINANCIALEXPRESS.COM', 'FREEPRESSJOURNAL.IN', 'LIVELAW.IN', 'MONEYCONTROL.COM', 'NEWS18.COM', 'THEHINDUBUSINESSLINE.COM', 'THESTATESMAN.COM', 'UNIINDIA.COM', 'ENGLISH.JAGRAN.COM', 'MUMBAIMIRROR.INDIATIMES.COM', 'NEWS.ABPLIVE.COM', 'SCROLL.IN', 'TEHELKA.COM', 'THEWIRE.IN', 'BUSINESSINSIDER.IN', 'DECCANCHRONICLE.COM', 'DECCANHERALD.COM', 'DNAINDIA.COM', 'INDIATIMES.COM', 'INDIATVNEWS.COM', 'LIVEMINT.COM', 'NDTV.COM', 'NEWS24.COM', 'THEHITAVADA.COM', 'ZEENEWS.INDIA.COM']

rss_dict=['("Crypto" OR "Cryptocurrency") AND ("scam" OR "fraud" OR "cheating" OR "duped" OR "pyramid")',
'"ransomware" AND ("crore" OR "crores")',
'("China" OR "Chinese") AND "fraud"',
'"Organised crime"',
'"Human trafficking"',
'"Black money"',
'Benami',
'"Sanctions List"',
'"Kashmir" AND "funding"',
'"Separatist" AND "India"',
'"Criminal proceeds"',
'"Denied Persons List"',
'"Visa" AND "Overstaying"',
'"Ponzi" AND "Scheme"',
'"Shell Company" AND "Beneficiary"',
'forge AND (billion OR million OR crores OR crore OR " cr ")',
'trafficking AND (billion OR million OR crores OR crore OR " cr ")',
'bribe AND (billion OR million OR crores OR crore OR " cr ")',
'corruption AND (billion OR million OR crores OR crore OR " cr ")',
'"insider trading" AND (billion OR million OR crores OR crore OR " cr ")',
'smuggle AND (billion OR million OR crores OR crore OR " cr ")',
'ransom AND (billion OR million OR crores OR crore OR " cr ")',
'kidnap AND (billion OR million OR crores OR crore OR " cr ")',
'robbery AND (billion OR million OR crores OR crore OR " cr ")',
'racket AND (billion OR million OR crores OR crore OR " cr ")',
'"illegal mining" AND (billion OR million OR crores OR crore OR " cr ")',
'hawala AND (billion OR million OR crores OR crore OR " cr ")',
'"black marketing" AND (billion OR million OR crores OR crore OR " cr ")',
'"fake currency" AND (billion OR million OR crores OR crore OR " cr ")',
'"counterfeit currency" AND (billion OR million OR crores OR crore OR " cr ")',
'"illegal conversion" AND (billion OR million OR crores OR crore OR " cr ")',
'crime AND (billion OR million OR crores OR crore OR " cr ")',
'scam AND (billion OR million OR crores OR crore OR " cr ")',
'fraud AND (billion OR million OR crores OR crore OR " cr ")',
'evasion AND (billion OR million OR crores OR crore OR " cr ")',
'extortion AND (billion OR million OR crores OR crore OR " cr ")',
'"money laundering" AND (billion OR million OR crores OR crore OR " cr ")',     
'"Enforcement Directorate" OR "Directorate of Enforcement" OR "ED"',
'"Directorate General of GST Intelligence" OR "DGGI"',
'"Directorate of Revenue Intelligence"',
'"Central Bureau of Investigation" OR "CBI"',
'"National Investigation Agency" OR "NIA"',
'("Income Tax Department" OR "I-T Department" OR "IT Department") AND (Seizure OR seized OR Raid OR fine OR fraud)',
'("Securities and Exchange Board of India" OR "SEBI") AND (Seizure OR seized OR Penalty OR Raid OR fine OR fraud)',
'("Reserve Bank of India" OR "RBI") AND (Penalty OR Raid OR fine OR seizure OR seized OR fraud)',
'("Insurance Regulatory and Development Authority" OR "IRDA") AND (Penalty OR Raid OR fine OR seized OR Seizure OR fraud)',
'"Narcotics Control Bureau" OR "NCB"',
'("GST" OR "Goods and Service Tax") AND (seized OR Seizure OR Customs OR Raid OR fine OR fraud)',
'"Under-invoicing" OR Underinvoicing OR misinvoicing',
'"Over-invoicing" OR Overinvoicing OR misinvoicing',
'"cyber fraud" OR "online fraud" OR "cyber crime" OR cybercrime',
'"cyber police" OR "police special cell"',
'"insurance fraud"',
'"Drug Trafficking"',
'"Illegal mining"',
'"Input Tax Credit Fraud" or "tax credit fraud" or "tax fraud"',
'"Anti Terrorist Squad" OR "Anti-Terrorist Squad" OR "Anti terrorism Squad" OR "Anti-terrorism Squad" OR "anti-terror unit" OR "anti terror unit"',
'"Counterfeit Currency" OR "Fake Indian Currency" OR "Fake currency Racket" OR "Fake currency found"',
'("Wild life" OR Hunting OR Animals OR Wildlife) AND (Rhino OR Smuggl OR syndicate OR racket OR gang OR poaching OR MAFIA)']




news_keywords = {
    "Money Laundering": ["money laundering",
    "layering",
    "placement",
    "integration",
    "shell companies",
    "benami transactions",
    "hawala",
    "round-tripping",
    "trade-based money laundering",
    "over-invoicing",
    "under-invoicing"], 

   "Terrorist Financing":
    ["terrorist financing",
     'kashmir separatist',
    "terror funding",
    "front organizations",
    "charity misuse",
    "cross-border terror funding",
    'anti terrorist squad',
    'anti terror unit',
    'national investigation agency' ],

    "Fraud":
    ["financial fraud",
    "bank fraud",
    "phishing",
    "ponzi scheme",
    "pyramid scheme",
    "identity theft",
    'fraud',
    'cheating',
    'forge',
    'duped', 
    'scam',
    "deepfake fraud"], 

    "Corruption":
    ["corruption",
    "bribery",
    "kickbacks",
    "abuse of office",
    'extortion',
    "bribe"],

    "Politically Exposed Persons (PEP)":
    ["politically exposed person",
    "minister",
    "member of parliament",
    "lawmaker",
    "bureaucrat",
    "political donations"],

    "Sanctions":
    ["economic sanctions",
    "sanctioned entity",
    "sanctions evasion",
    "asset freeze",
    'sanctions list',
    'denied persons list',
    "arms embargo"],

    "Organized Crime":
    ["organized crime",
    "drug trafficking",
    "human trafficking",
    "wildlife trafficking",
    "illegal mining"],

    "Cybercrime":
    ["cybercrime",
     'cyber fraud',
     'online fraud',
     'cyber police',
    "ransomware",
    "dark web",
    "cryptocurrency laundering"],

    "Cryptocurrency":
    ["cryptocurrency",
    "privacy coins",
    "monero",
    'crypto',   
    "mixer",
    "rug pull"],

    "Tax Crimes":
    ["tax evasion",
    "black money",
    'input tax credit fraud',
    "offshore accounts",
    "panama papers",
    'underinvoicing',
    'income tax department',
    'property seizure'
    'misinvoicing'],

    "Regulatory / Compliance":
    ["suspicious transaction",
    "cash transaction",
    "kyc violation",
    "aml non-compliance"],

    "Cross-Border Risk":
    ["cross-border remittance",
    "high-risk country",
    "fatf grey list",
    "fatf black list"],

    "Market Abuse":
    ["insider trading",
    "market manipulation",
    "pump and dump"],

    "Asset Laundering":
    ["real estate laundering",
    "luxury asset purchase",
    'smuggle',
    'syndicate'
    "gold smuggling"],

    "Enforcement & Triggers":
    ["investigation launched",
    "enforcement directorate",
    'police special cell',
    'directorate of revenue intelligence',
    'central bureau of investigation',
    "cbi probe",
    "assets seized",
    "accounts frozen",
    "arrested"],

    "Others":
    ['visa overstaying',
    'shell company',
    'trafficking',
    'kidnap',
    'robbery',
    'racket',
    'black marketing',
    'fake currency',
    'counterfeit currency',
    'illegal conversion',
    'securities exchange board of india',
    'reserve bank of india',
    'penalty insurance regulatory and development authority',
    'narcotics control bureau',
    'goods and service tax',
    'insurance fraud',
    'drug trafficking',
    'illegal mining',
    'counterfeit currency',
    'underworld',
    'gang',
    'poaching',
    'mafia',
    'modern slavery']
    
}

news_domains= ['NEWINDIANEXPRESS.COM',
    'THEPRINT.IN',
    'HINDUSTANTIMES.COM',
    'TEHELKA.COM',
    'BUSINESSTODAY.IN',
    'INDIATIMES.COM',
    'NDTV.COM',
    'INDIATODAY.IN',
    'DECCANHERALD.COM',
    'REPUBLICWORLD.COM',
    'THEWIRE.IN',
    'BUSINESS-STANDARD.COM',
    'MONEYCONTROL.COM',
    'SCROLL.IN',
    'LIVELAW.IN',
    'TIMESNOWNEWS.COM',
    'LOKMAT.COM',
    'JAGRAN.COM',
    'BUSINESSINSIDER.IN',
    'DECCANCHRONICLE.COM',
    'INDIATVNEWS.COM',
    'LIVEMINT.COM',
    'FINANCIALEXPRESS.COM',
    'THESTATESMAN.COM',
    'ANINEWS.IN',
    'DNAINDIA.COM',
    'FREEPRESSJOURNAL.IN',
    'UNIINDIA.COM',
    'INDIANEXPRESS.COM',
    'THEHITAVADA.COM',
    'NEWS18.COM',
    'NEWS24.COM',
    'ZEENEWS.INDIA.COM',
    'THEHINDUBUSINESSLINE.COM',
    'ABPLIVE.COM',
    'TRIBUNEINDIA.COM']

# keywords
keywords = []
for key in news_keywords.keys():
    keywords = keywords + news_keywords[key]
keywords = set(keywords)

# domains
domains = set(news_domains)
domains = [domain.lower() for domain in domains]

