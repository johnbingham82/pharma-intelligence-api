#!/usr/bin/env python3
"""
CCG to Local Authority Mapping

Maps NHS CCG/Practice data to Local Authorities using keyword matching
and geographic heuristics.

TODO: Replace with official NHS ODS postcode→LA lookup for accuracy
"""
import re
from typing import Optional

# Major UK Local Authorities with common name variations
LA_KEYWORDS = {
    # Major Cities
    'Birmingham': ['birmingham', 'bham', 'solihull'],
    'Leeds': ['leeds'],
    'Sheffield': ['sheffield'],
    'Manchester': ['manchester', 'salford', 'trafford'],
    'Liverpool': ['liverpool', 'sefton', 'knowsley'],
    'Bristol': ['bristol'],
    'Newcastle upon Tyne': ['newcastle', 'gateshead'],
    'Nottingham': ['nottingham'],
    'Leicester': ['leicester'],
    'Coventry': ['coventry'],
    'Bradford': ['bradford'],
    'Cardiff': ['cardiff'],
    'Edinburgh': ['edinburgh'],
    'Glasgow': ['glasgow'],
    
    # London Boroughs
    'Barnet': ['barnet'],
    'Brent': ['brent'],
    'Camden': ['camden'],
    'Croydon': ['croydon'],
    'Ealing': ['ealing'],
    'Enfield': ['enfield'],
    'Hackney': ['hackney'],
    'Hammersmith and Fulham': ['hammersmith', 'fulham'],
    'Haringey': ['haringey'],
    'Harrow': ['harrow'],
    'Hillingdon': ['hillingdon'],
    'Hounslow': ['hounslow'],
    'Islington': ['islington'],
    'Kensington and Chelsea': ['kensington', 'chelsea'],
    'Kingston upon Thames': ['kingston'],
    'Lambeth': ['lambeth'],
    'Lewisham': ['lewisham'],
    'Merton': ['merton'],
    'Newham': ['newham'],
    'Redbridge': ['redbridge'],
    'Richmond upon Thames': ['richmond'],
    'Southwark': ['southwark'],
    'Sutton': ['sutton'],
    'Tower Hamlets': ['tower hamlets', 'bethnal green'],
    'Waltham Forest': ['waltham'],
    'Wandsworth': ['wandsworth'],
    'Westminster': ['westminster'],
    
    # Counties & Major Towns
    'Hampshire': ['hampshire', 'portsmouth', 'southampton'],
    'Kent': ['kent', 'maidstone', 'canterbury'],
    'Essex': ['essex', 'colchester', 'southend'],
    'Surrey': ['surrey', 'guildford'],
    'Lancashire': ['lancashire', 'preston', 'blackburn', 'blackpool'],
    'West Yorkshire': ['west yorkshire', 'wakefield', 'huddersfield'],
    'Durham': ['durham', 'darlington'],
    'Northumberland': ['northumberland', 'alnwick'],
    'Cumbria': ['cumbria', 'carlisle'],
    'Devon': ['devon', 'plymouth', 'exeter'],
    'Cornwall': ['cornwall', 'truro'],
    'Somerset': ['somerset', 'taunton', 'bath'],
    'Gloucestershire': ['gloucester', 'cheltenham'],
    'Oxfordshire': ['oxford', 'banbury'],
    'Cambridgeshire': ['cambridge', 'peterborough'],
    'Norfolk': ['norfolk', 'norwich'],
    'Suffolk': ['suffolk', 'ipswich'],
    'Lincolnshire': ['lincolnshire', 'lincoln'],
    'Derbyshire': ['derby', 'chesterfield'],
    'Staffordshire': ['stafford', 'stoke'],
    'Shropshire': ['shrewsbury', 'telford'],
    'Worcestershire': ['worcester'],
    'Warwickshire': ['warwick', 'rugby'],
}


def map_practice_to_la(practice_name: str, practice_code: str = None) -> Optional[str]:
    """
    Map a GP practice name to a Local Authority
    
    Args:
        practice_name: Name of the practice
        practice_code: NHS practice code (optional)
        
    Returns:
        Local Authority name or None
    """
    if not practice_name:
        return None
    
    practice_lower = practice_name.lower()
    
    # Try exact keyword matching first
    for la_name, keywords in LA_KEYWORDS.items():
        for keyword in keywords:
            if keyword in practice_lower:
                return la_name
    
    # Fallback: extract place name from common patterns
    # "The X Surgery" → "X"
    # "X Medical Centre" → "X"
    patterns = [
        r'the\s+(\w+)\s+surgery',
        r'(\w+)\s+medical',
        r'(\w+)\s+health',
        r'(\w+)\s+doctors',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, practice_lower)
        if match:
            place = match.group(1).title()
            # Check if this place matches any LA
            for la_name, keywords in LA_KEYWORDS.items():
                if place.lower() in keywords:
                    return la_name
    
    return None


def map_ccg_to_la(ccg_name: str, ccg_code: str = None) -> Optional[str]:
    """
    Map a CCG name to a Local Authority (approximate)
    
    Args:
        ccg_name: Name of the CCG
        ccg_code: CCG code (optional)
        
    Returns:
        Local Authority name or None
    """
    if not ccg_name:
        return None
    
    # CCG names often contain geographic references
    # "NHS Birmingham and Solihull" → "Birmingham"
    ccg_clean = ccg_name.replace('NHS', '').strip().lower()
    
    # Try matching against LA keywords
    for la_name, keywords in LA_KEYWORDS.items():
        for keyword in keywords:
            if keyword in ccg_clean:
                return la_name
    
    return None


def get_fallback_la_for_region(region_name: str) -> str:
    """
    Get a default LA for a region (for practices that can't be mapped)
    
    Args:
        region_name: NHS region name
        
    Returns:
        A representative Local Authority name
    """
    region_to_la = {
        'NHS England North East and Yorkshire': 'Newcastle upon Tyne',
        'NHS England North West': 'Manchester',
        'NHS England Midlands': 'Birmingham',
        'NHS England East of England': 'Cambridge',
        'NHS England London': 'Westminster',
        'NHS England South East': 'Surrey',
        'NHS England South West': 'Bristol',
    }
    
    return region_to_la.get(region_name, 'Unknown')


if __name__ == '__main__':
    # Test the mapping
    test_practices = [
        'THE DENSHAM SURGERY',
        'MANCHESTER MEDICAL CENTRE',
        'LEEDS CITY PRACTICE',
        'BRISTOL CENTRAL SURGERY',
        'BARNET HEALTH GROUP',
        'CAMBRIDGE DOCTORS',
    ]
    
    print("Testing practice → LA mapping:")
    for practice in test_practices:
        la = map_practice_to_la(practice)
        print(f"  {practice} → {la}")
