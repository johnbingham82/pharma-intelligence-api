#!/usr/bin/env python3
"""
NHS Practice Postcode Geocoding
Maps NHS practices to Local Authorities using postcodes.io (free, no API key)
"""
import requests
import json
import os
import time
from typing import Dict, Optional, Tuple

# Cache file for postcode lookups
CACHE_FILE = os.path.join(os.path.dirname(__file__), 'cache', 'postcode_cache.json')


class PostcodeGeocoder:
    """Geocode NHS practices using postcodes.io"""
    
    def __init__(self):
        self.cache = self._load_cache()
        self.nhs_ods_base = "https://directory.spineservices.nhs.uk/ORD/2-0-0/organisations"
        self.postcodes_io_base = "https://api.postcodes.io"
        self.session = requests.Session()
        
    def _load_cache(self) -> Dict:
        """Load cached postcode lookups"""
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load cache: {e}")
        return {}
    
    def _save_cache(self):
        """Save cache to disk"""
        try:
            os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
            with open(CACHE_FILE, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save cache: {e}")
    
    def get_practice_postcode(self, practice_code: str) -> Optional[str]:
        """
        Get postcode for an NHS practice using ODS API
        
        Args:
            practice_code: NHS practice code (e.g., 'A81001')
            
        Returns:
            Postcode string or None
        """
        cache_key = f"ods_{practice_code}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        url = f"{self.nhs_ods_base}/{practice_code}"
        
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Extract postcode from address
                location = data.get('Organisation', {}).get('GeoLoc', {}).get('Location', {})
                postcode = location.get('PostCode')
                
                if postcode:
                    self.cache[cache_key] = postcode
                    return postcode
                    
        except Exception as e:
            print(f"Error fetching postcode for {practice_code}: {e}")
        
        return None
    
    def get_local_authority_from_postcode(self, postcode: str) -> Optional[Tuple[str, str, float, float]]:
        """
        Get Local Authority info from postcode using postcodes.io
        
        Args:
            postcode: UK postcode
            
        Returns:
            Tuple of (LA code, LA name, latitude, longitude) or None
        """
        if not postcode:
            return None
        
        # Clean postcode
        postcode_clean = postcode.replace(' ', '').upper()
        
        cache_key = f"pc_{postcode_clean}"
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            return (cached['la_code'], cached['la_name'], cached['lat'], cached['lng'])
        
        url = f"{self.postcodes_io_base}/postcodes/{postcode_clean}"
        
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                result = data.get('result', {})
                
                la_code = result.get('admin_district')  # Local Authority code
                la_name = result.get('admin_district')  # Same as code usually
                lat = result.get('latitude')
                lng = result.get('longitude')
                
                if la_code and lat and lng:
                    # Cache the result
                    self.cache[cache_key] = {
                        'la_code': la_code,
                        'la_name': la_name,
                        'lat': lat,
                        'lng': lng
                    }
                    return (la_code, la_name, lat, lng)
                    
        except Exception as e:
            print(f"Error geocoding postcode {postcode}: {e}")
        
        return None
    
    def get_practice_location_and_la(self, practice_code: str) -> Optional[Dict]:
        """
        Get full location info for a practice (postcode, LA, lat/lng)
        
        Args:
            practice_code: NHS practice code
            
        Returns:
            Dict with postcode, la_code, la_name, lat, lng or None
        """
        # Check full cache first
        cache_key = f"full_{practice_code}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Get postcode from ODS
        postcode = self.get_practice_postcode(practice_code)
        if not postcode:
            return None
        
        # Get LA and coordinates from postcode
        la_info = self.get_local_authority_from_postcode(postcode)
        if not la_info:
            return None
        
        la_code, la_name, lat, lng = la_info
        
        result = {
            'postcode': postcode,
            'la_code': la_code,
            'la_name': la_name,
            'lat': lat,
            'lng': lng
        }
        
        # Cache the full result
        self.cache[cache_key] = result
        
        return result
    
    def batch_geocode_practices(self, practice_codes: list, rate_limit_delay: float = 0.1) -> Dict[str, Dict]:
        """
        Geocode multiple practices in batch
        
        Args:
            practice_codes: List of NHS practice codes
            rate_limit_delay: Delay between API calls (seconds)
            
        Returns:
            Dict mapping practice_code → location info
        """
        results = {}
        total = len(practice_codes)
        
        for i, code in enumerate(practice_codes):
            if i % 50 == 0:
                print(f"  Geocoding: {i}/{total} practices...")
                self._save_cache()  # Save periodically
            
            location = self.get_practice_location_and_la(code)
            if location:
                results[code] = location
            
            # Rate limiting
            if rate_limit_delay > 0:
                time.sleep(rate_limit_delay)
        
        # Final save
        self._save_cache()
        print(f"  ✓ Geocoded {len(results)}/{total} practices")
        
        return results


def test_geocoder():
    """Test the geocoder with sample practices"""
    print("Testing PostcodeGeocoder...\n")
    
    geocoder = PostcodeGeocoder()
    
    # Test practice codes
    test_codes = ['A81001', 'Y00249', 'B82010']
    
    for code in test_codes:
        print(f"Practice: {code}")
        location = geocoder.get_practice_location_and_la(code)
        if location:
            print(f"  Postcode: {location['postcode']}")
            print(f"  LA: {location['la_name']} ({location['la_code']})")
            print(f"  Coordinates: {location['lat']}, {location['lng']}")
        else:
            print(f"  ⚠️  Could not geocode")
        print()


if __name__ == '__main__':
    test_geocoder()
