"""
Medicine Reminder Agent - Core Module
A Python-based medicine reminder system for Indian families

This module contains the core MedicineReminderAgent class that can be used
in both the Kaggle notebook demo and the future mobile app implementation.
"""

import datetime
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

# TTS imports (conditional)
try:
    from gtts import gTTS
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    gTTS = None  # type: ignore


class MedicineReminderAgent:
    """
    Smart Medicine Reminder Agent for Indian Families
    
    Features:
    - Multilingual reminder support (Hindi, English, mixed)
    - Custom personalized messages
    - Voice-based reminders using TTS
    - Easy schedule management
    - Export/Import functionality
    """
    
    def __init__(self):
        """Initialize the reminder agent"""
        self.reminders: List[Dict] = []
        self.reminder_id_counter = 1
        
    def add_reminder(self, 
                    medicine_name: str, 
                    reminder_time: str, 
                    custom_message: str,
                    frequency: str = "daily") -> Dict:
        """
        Add a new medicine reminder
        
        Args:
            medicine_name: Name of the medicine
            reminder_time: Time in HH:MM format (24-hour)
            custom_message: Personalized reminder message in any language
            frequency: How often (daily, weekly, etc.)
            
        Returns:
            Dictionary containing reminder details
        """
        reminder = {
            'id': self.reminder_id_counter,
            'medicine_name': medicine_name,
            'time': reminder_time,
            'message': custom_message,
            'frequency': frequency,
            'active': True,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.reminders.append(reminder)
        self.reminder_id_counter += 1
        
        print(f"✅ Reminder added successfully! (ID: {reminder['id']})")
        return reminder
    
    def view_reminders(self) -> List[Dict]:
        """
        View all active reminders as a formatted list
        
        Returns:
            List of active reminder dictionaries
        """
        if not self.reminders:
            print("📭 No reminders scheduled yet.")
            return []
        
        active_reminders = [r for r in self.reminders if r['active']]
        
        if not active_reminders:
            print("📭 No active reminders.")
            return []
        
        # Print in table format
        print("\n" + "="*80)
        print(f"{'ID':<5} {'Medicine':<20} {'Time':<10} {'Frequency':<12} {'Message':<30}")
        print("="*80)
        for r in active_reminders:
            print(f"{r['id']:<5} {r['medicine_name']:<20} {r['time']:<10} {r['frequency']:<12} {r['message'][:28]:<30}")
        print("="*80 + "\n")
        
        return active_reminders
    
    def get_reminder_by_id(self, reminder_id: int) -> Optional[Dict]:
        """
        Get a specific reminder by ID
        
        Args:
            reminder_id: ID of the reminder
            
        Returns:
            Reminder dictionary if found, None otherwise
        """
        for reminder in self.reminders:
            if reminder['id'] == reminder_id and reminder['active']:
                return reminder
        return None
    
    def delete_reminder(self, reminder_id: int) -> bool:
        """
        Delete a reminder by ID
        
        Args:
            reminder_id: ID of the reminder to delete
            
        Returns:
            True if deleted, False if not found
        """
        for reminder in self.reminders:
            if reminder['id'] == reminder_id and reminder['active']:
                reminder['active'] = False
                print(f"🗑️ Reminder {reminder_id} deleted successfully.")
                return True
        
        print(f"❌ Reminder {reminder_id} not found.")
        return False
    
    def edit_reminder(self, 
                     reminder_id: int, 
                     medicine_name: Optional[str] = None,
                     reminder_time: Optional[str] = None,
                     custom_message: Optional[str] = None,
                     frequency: Optional[str] = None) -> bool:
        """
        Edit an existing reminder
        
        Args:
            reminder_id: ID of reminder to edit
            medicine_name: New medicine name (optional)
            reminder_time: New time (optional)
            custom_message: New message (optional)
            frequency: New frequency (optional)
            
        Returns:
            True if edited, False if not found
        """
        for reminder in self.reminders:
            if reminder['id'] == reminder_id and reminder['active']:
                if medicine_name:
                    reminder['medicine_name'] = medicine_name
                if reminder_time:
                    reminder['time'] = reminder_time
                if custom_message:
                    reminder['message'] = custom_message
                if frequency:
                    reminder['frequency'] = frequency
                    
                print(f"✏️ Reminder {reminder_id} updated successfully.")
                return True
        
        print(f"❌ Reminder {reminder_id} not found.")
        return False
    
    def generate_tts(self, message: str, filename: str = "reminder.mp3") -> Optional[str]:
        """
        Generate TTS audio from message
        
        Args:
            message: Text to convert to speech
            filename: Output audio filename
            
        Returns:
            Filename if successful, None otherwise
        """
        if not TTS_AVAILABLE or gTTS is None:
            print("⚠️ TTS not available. Message would be: " + message)
            return None
        
        try:
            # Auto-detect language (supports Hindi, English, and mixed)
            tts = gTTS(text=message, lang='hi', slow=False)  # type: ignore
            tts.save(filename)
            print(f"🔊 Audio generated: {filename}")
            return filename
        except Exception as e:
            print(f"⚠️ TTS Error: {e}")
            return None
    
    def check_and_trigger_reminders(self, current_time: Optional[str] = None) -> List[Dict]:
        """
        Check if any reminders need to be triggered
        
        Args:
            current_time: Time to check (HH:MM format). If None, uses current time.
            
        Returns:
            List of triggered reminders
        """
        if current_time is None:
            current_time = datetime.now().strftime("%H:%M")
        
        triggered = []
        
        for reminder in self.reminders:
            if reminder['active'] and reminder['time'] == current_time:
                triggered.append(reminder)
                print(f"\n⏰ REMINDER TRIGGERED at {current_time}")
                print(f"💊 Medicine: {reminder['medicine_name']}")
                print(f"📢 Message: {reminder['message']}")
                print("─" * 50)
                
                # Generate TTS
                self.generate_tts(reminder['message'], f"reminder_{reminder['id']}.mp3")
        
        return triggered
    
    def simulate_day(self, times_to_check: List[str]):
        """
        Simulate checking reminders at multiple times throughout a day
        
        Args:
            times_to_check: List of times in HH:MM format
        """
        print("\n🌅 Starting Day Simulation...\n")
        
        for check_time in sorted(times_to_check):
            print(f"\n🕐 Current Time: {check_time}")
            triggered = self.check_and_trigger_reminders(check_time)
            
            if not triggered:
                print("   No reminders at this time.")
        
        print("\n🌙 Day Simulation Complete!\n")
    
    def export_schedule(self, filename: str = "medicine_schedule.json"):
        """
        Export reminder schedule to JSON file
        
        Args:
            filename: Output JSON filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.reminders, f, ensure_ascii=False, indent=2)
        print(f"💾 Schedule exported to {filename}")
    
    def import_schedule(self, filename: str = "medicine_schedule.json"):
        """
        Import reminder schedule from JSON file
        
        Args:
            filename: Input JSON filename
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.reminders = json.load(f)
            
            # Update counter to avoid ID conflicts
            if self.reminders:
                max_id = max(r['id'] for r in self.reminders)
                self.reminder_id_counter = max_id + 1
            
            print(f"📥 Schedule imported from {filename}")
        except FileNotFoundError:
            print(f"❌ File {filename} not found.")
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about the reminder schedule
        
        Returns:
            Dictionary containing various statistics
        """
        active_reminders = [r for r in self.reminders if r['active']]
        
        stats = {
            'total_created': self.reminder_id_counter - 1,
            'active': len(active_reminders),
            'deleted': len(self.reminders) - len(active_reminders),
            'times': {},
            'medicines': []
        }
        
        # Count reminders per time
        for reminder in active_reminders:
            time = reminder['time']
            stats['times'][time] = stats['times'].get(time, 0) + 1
            stats['medicines'].append({
                'name': reminder['medicine_name'],
                'time': reminder['time']
            })
        
        return stats
    
    def get_upcoming_reminders(self, hours: int = 24) -> List[Dict]:
        """
        Get reminders scheduled within the next N hours
        
        Args:
            hours: Number of hours to look ahead
            
        Returns:
            List of upcoming reminders sorted by time
        """
        current_time = datetime.now()
        current_hour_min = current_time.strftime("%H:%M")
        
        upcoming = []
        
        for reminder in self.reminders:
            if reminder['active']:
                # For simplicity, just check if time is after current time today
                if reminder['time'] >= current_hour_min:
                    upcoming.append(reminder)
        
        # Sort by time
        upcoming.sort(key=lambda x: x['time'])
        
        return upcoming


# Sample usage demonstration
if __name__ == "__main__":
    print("🤖 Medicine Reminder Agent - Core Module")
    print("=" * 60)
    
    # Create agent instance
    agent = MedicineReminderAgent()
    
    # Add sample reminders
    agent.add_reminder(
        "Amlodipine (BP)",
        "08:00",
        "Are uncle, aapki BP ki dawai ka time ho gaya hai!"
    )
    
    agent.add_reminder(
        "Metformin (Diabetes)",
        "08:30",
        "Good morning! Time for your diabetes medicine."
    )
    
    # View schedule
    print("\n📅 Current Schedule:")
    print(agent.view_reminders())
    
    # Get statistics
    stats = agent.get_statistics()
    print(f"\n📊 Statistics:")
    print(f"   Active Reminders: {stats['active']}")
    print(f"   Total Created: {stats['total_created']}")
    
    print("\n✅ Module demonstration complete!")
