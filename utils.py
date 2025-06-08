import re
import json
import os
import threading
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

def validate_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_phone(phone: str) -> bool:
    return phone.isdigit() and len(phone) >= 10

# Global flag and lock for duplicate prevention
_save_operations = {}
_save_lock = threading.Lock()

def _cleanup_old_operations():
    """Clean up old save operations (older than 30 seconds)"""
    current_time = time.time()
    cutoff_time = current_time - 30  # 30 seconds timeout
    
    keys_to_remove = []
    for key, timestamp in _save_operations.items():
        if timestamp < cutoff_time:
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        _save_operations.pop(key, None)

def _generate_candidate_key(data: Dict[str, Any]) -> str:
    """Generate a unique key for the candidate based on email and phone"""
    email = data.get('email', '').lower().strip()
    phone = data.get('phone', '').strip()
    return f"{email}|{phone}"

def _is_duplicate_candidate(candidates: List[Dict], new_data: Dict[str, Any]) -> bool:
    """Check if candidate already exists in the list"""
    new_email = new_data.get('email', '').lower().strip()
    new_phone = new_data.get('phone', '').strip()
    
    if not new_email and not new_phone:
        return False
    
    for existing in candidates:
        existing_email = existing.get('email', '').lower().strip()
        existing_phone = existing.get('phone', '').strip()
        
        # Check for email match (if both have emails)
        if new_email and existing_email and new_email == existing_email:
            print(f"⚠️ Duplicate found: Email {new_email} already exists")
            return True
        
        # Check for phone match (if both have phones)
        if new_phone and existing_phone and new_phone == existing_phone:
            print(f"⚠️ Duplicate found: Phone {new_phone} already exists")
            return True
    
    return False

def save_candidate_data(data: Dict[str, Any], filename: str = "data/candidates.json") -> Optional[str]:
    """Save candidate data to JSON file with duplicate prevention and thread safety"""
    
    # Generate unique key for this candidate
    candidate_key = _generate_candidate_key(data)
    current_time = time.time()
    
    with _save_lock:
        # Clean up old operations first
        _cleanup_old_operations()
        
        # Check if this exact candidate is currently being saved
        if candidate_key in _save_operations:
            time_diff = current_time - _save_operations[candidate_key]
            if time_diff < 10:  # 10 seconds timeout
                print(f"⚠️ Save operation already in progress for this candidate, skipping...")
                return filename
        
        # Mark this operation as in progress
        _save_operations[candidate_key] = current_time
    
    try:
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Initialize candidates list
        candidates = []
        
        # Try to read existing data - handle all possible errors
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding='utf-8') as f:
                    file_content = f.read().strip()
                    if file_content:  # File has content
                        candidates = json.loads(file_content)
                    # If file is empty, candidates remains []
            except (json.JSONDecodeError, UnicodeDecodeError):
                print("⚠️ Existing file corrupted, starting fresh")
                candidates = []
        
        # Check for duplicates in existing data
        if _is_duplicate_candidate(candidates, data):
            print(f"❌ Candidate already exists, not saving duplicate")
            return filename
        
        # Add enhanced data
        enhanced_data = {
            **data,
            "timestamp": datetime.now().isoformat(),
            "status": "questions_sent",
            "submission_deadline": (datetime.now() + timedelta(hours=48)).isoformat(),
            "assessment_email": "talentscout.tech.assessment@gmail.com"
        }
        
        candidates.append(enhanced_data)
        
        # Save to file with atomic write (write to temp file first, then rename)
        temp_filename = filename + ".tmp"
        with open(temp_filename, "w", encoding='utf-8') as f:
            json.dump(candidates, f, indent=2, ensure_ascii=False)
        
        # Atomic rename (prevents corruption if interrupted)
        os.replace(temp_filename, filename)
        
        print(f"✅ Candidate data saved successfully!")
        return filename
        
    except Exception as e:
        print(f"❌ Error saving candidate data: {str(e)}")
        # Try to save to backup file
        try:
            backup_filename = f"data/candidates_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_filename, "w", encoding='utf-8') as f:
                json.dump([data], f, indent=2, ensure_ascii=False)
            print(f"💾 Saved to backup file: {backup_filename}")
        except:
            pass
        return None
    
    finally:
        # Clean up the operation flag
        with _save_lock:
            _save_operations.pop(candidate_key, None)

def load_candidate_data(filename: str = "data/candidates.json") -> List[Dict[str, Any]]:
    """Load all candidate data from JSON file"""
    try:
        if not os.path.exists(filename):
            return []
            
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
            
    except Exception as e:
        print(f"❌ Error loading candidate data: {str(e)}")
        return []

def get_latest_candidates(limit: int = 10) -> List[Dict[str, Any]]:
    """Get the most recent candidates"""
    try:
        candidates = load_candidate_data()
        if not candidates:
            return []
        # Sort by timestamp (most recent first)
        sorted_candidates = sorted(candidates, key=lambda x: x.get('timestamp', ''), reverse=True)
        return sorted_candidates[:limit]
    except Exception as e:
        print(f"❌ Error getting latest candidates: {str(e)}")
        return []

def remove_duplicates_from_file(filename: str = "data/candidates.json") -> int:
    """Remove duplicates from existing candidates file and return count of duplicates removed"""
    try:
        candidates = load_candidate_data(filename)
        if not candidates:
            return 0
        
        unique_candidates = []
        seen_emails = set()
        seen_phones = set()
        duplicates_count = 0
        
        for candidate in candidates:
            email = candidate.get('email', '').lower().strip()
            phone = candidate.get('phone', '').strip()
            
            is_duplicate = False
            
            # Check email duplicate
            if email and email in seen_emails:
                is_duplicate = True
            
            # Check phone duplicate
            if phone and phone in seen_phones:
                is_duplicate = True
            
            if is_duplicate:
                duplicates_count += 1
                print(f"Removing duplicate: {email} | {phone}")
            else:
                unique_candidates.append(candidate)
                if email:
                    seen_emails.add(email)
                if phone:
                    seen_phones.add(phone)
        
        # Save cleaned data back to file
        if duplicates_count > 0:
            with open(filename, "w", encoding='utf-8') as f:
                json.dump(unique_candidates, f, indent=2, ensure_ascii=False)
            print(f"✅ Removed {duplicates_count} duplicates from {filename}")
        
        return duplicates_count
        
    except Exception as e:
        print(f"❌ Error removing duplicates: {str(e)}")
        return 0

def get_candidate_stats() -> Dict[str, Any]:
    """Get statistics about candidates"""
    try:
        candidates = load_candidate_data()
        total_count = len(candidates)
        
        if total_count == 0:
            return {"total": 0, "recent_24h": 0, "recent_7d": 0}
        
        now = datetime.now()
        day_ago = now - timedelta(days=1)
        week_ago = now - timedelta(days=7)
        
        recent_24h = 0
        recent_7d = 0
        
        for candidate in candidates:
            timestamp_str = candidate.get('timestamp', '')
            if timestamp_str:
                try:
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    if timestamp >= day_ago:
                        recent_24h += 1
                    if timestamp >= week_ago:
                        recent_7d += 1
                except:
                    pass
        
        return {
            "total": total_count,
            "recent_24h": recent_24h,
            "recent_7d": recent_7d
        }
        
    except Exception as e:
        print(f"❌ Error getting candidate stats: {str(e)}")
        return {"total": 0, "recent_24h": 0, "recent_7d": 0}