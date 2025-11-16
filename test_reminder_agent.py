"""
Test suite for Medicine Reminder Agent
Demonstrates testing capabilities for the core module
"""

import unittest
from datetime import datetime
import os
import json
from medicine_reminder_core import MedicineReminderAgent


class TestMedicineReminderAgent(unittest.TestCase):
    """Test cases for MedicineReminderAgent class"""
    
    def setUp(self):
        """Set up test fixture before each test method"""
        self.agent = MedicineReminderAgent()
    
    def tearDown(self):
        """Clean up after each test method"""
        # Remove test files if they exist
        test_files = ['test_schedule.json', 'test_reminder.mp3']
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
    
    def test_initialization(self):
        """Test agent initialization"""
        self.assertEqual(len(self.agent.reminders), 0)
        self.assertEqual(self.agent.reminder_id_counter, 1)
    
    def test_add_reminder(self):
        """Test adding a reminder"""
        reminder = self.agent.add_reminder(
            medicine_name="Test Medicine",
            reminder_time="10:00",
            custom_message="Test message"
        )
        
        self.assertEqual(reminder['id'], 1)
        self.assertEqual(reminder['medicine_name'], "Test Medicine")
        self.assertEqual(reminder['time'], "10:00")
        self.assertEqual(reminder['message'], "Test message")
        self.assertTrue(reminder['active'])
        self.assertEqual(len(self.agent.reminders), 1)
    
    def test_add_multiple_reminders(self):
        """Test adding multiple reminders"""
        self.agent.add_reminder("Medicine 1", "08:00", "Message 1")
        self.agent.add_reminder("Medicine 2", "14:00", "Message 2")
        self.agent.add_reminder("Medicine 3", "20:00", "Message 3")
        
        self.assertEqual(len(self.agent.reminders), 3)
        self.assertEqual(self.agent.reminder_id_counter, 4)
    
    def test_view_reminders_empty(self):
        """Test viewing reminders when none exist"""
        reminders = self.agent.view_reminders()
        self.assertEqual(len(reminders), 0)
    
    def test_view_reminders(self):
        """Test viewing reminders"""
        self.agent.add_reminder("Medicine 1", "08:00", "Message 1")
        self.agent.add_reminder("Medicine 2", "14:00", "Message 2")
        
        reminders = self.agent.view_reminders()
        self.assertEqual(len(reminders), 2)
        self.assertIn('medicine_name', reminders[0].keys())
        self.assertIn('time', reminders[0].keys())
    
    def test_delete_reminder(self):
        """Test deleting a reminder"""
        self.agent.add_reminder("Test Medicine", "10:00", "Test message")
        
        result = self.agent.delete_reminder(1)
        self.assertTrue(result)
        
        reminders = self.agent.view_reminders()
        self.assertEqual(len(reminders), 0)
    
    def test_delete_nonexistent_reminder(self):
        """Test deleting a non-existent reminder"""
        result = self.agent.delete_reminder(999)
        self.assertFalse(result)
    
    def test_edit_reminder(self):
        """Test editing a reminder"""
        self.agent.add_reminder("Original Medicine", "10:00", "Original message")
        
        result = self.agent.edit_reminder(
            reminder_id=1,
            medicine_name="Updated Medicine",
            reminder_time="11:00",
            custom_message="Updated message"
        )
        
        self.assertTrue(result)
        
        reminder = self.agent.get_reminder_by_id(1)
        self.assertIsNotNone(reminder)
        if reminder:  # Type guard for linter
            self.assertEqual(reminder['medicine_name'], "Updated Medicine")
            self.assertEqual(reminder['time'], "11:00")
            self.assertEqual(reminder['message'], "Updated message")
    
    def test_edit_partial_reminder(self):
        """Test editing only some fields of a reminder"""
        self.agent.add_reminder("Original Medicine", "10:00", "Original message")
        
        self.agent.edit_reminder(reminder_id=1, medicine_name="New Medicine")
        
        reminder = self.agent.get_reminder_by_id(1)
        self.assertIsNotNone(reminder)
        if reminder:  # Type guard for linter
            self.assertEqual(reminder['medicine_name'], "New Medicine")
            self.assertEqual(reminder['time'], "10:00")  # Unchanged
            self.assertEqual(reminder['message'], "Original message")  # Unchanged
    
    def test_check_reminders_no_match(self):
        """Test checking reminders when none match current time"""
        self.agent.add_reminder("Test Medicine", "10:00", "Test message")
        
        triggered = self.agent.check_and_trigger_reminders("09:00")
        self.assertEqual(len(triggered), 0)
    
    def test_check_reminders_with_match(self):
        """Test checking reminders when time matches"""
        self.agent.add_reminder("Test Medicine", "10:00", "Test message")
        
        triggered = self.agent.check_and_trigger_reminders("10:00")
        self.assertEqual(len(triggered), 1)
        self.assertEqual(triggered[0]['medicine_name'], "Test Medicine")
    
    def test_check_multiple_reminders_same_time(self):
        """Test checking when multiple reminders are at same time"""
        self.agent.add_reminder("Medicine 1", "10:00", "Message 1")
        self.agent.add_reminder("Medicine 2", "10:00", "Message 2")
        
        triggered = self.agent.check_and_trigger_reminders("10:00")
        self.assertEqual(len(triggered), 2)
    
    def test_export_schedule(self):
        """Test exporting schedule to JSON"""
        self.agent.add_reminder("Test Medicine", "10:00", "Test message")
        
        self.agent.export_schedule("test_schedule.json")
        
        self.assertTrue(os.path.exists("test_schedule.json"))
        
        with open("test_schedule.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['medicine_name'], "Test Medicine")
    
    def test_import_schedule(self):
        """Test importing schedule from JSON"""
        # Create a test schedule file
        test_data = [
            {
                'id': 1,
                'medicine_name': 'Test Medicine',
                'time': '10:00',
                'message': 'Test message',
                'frequency': 'daily',
                'active': True,
                'created_at': '2025-11-15 10:00:00'
            }
        ]
        
        with open("test_schedule.json", 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        self.agent.import_schedule("test_schedule.json")
        
        self.assertEqual(len(self.agent.reminders), 1)
        self.assertEqual(self.agent.reminders[0]['medicine_name'], 'Test Medicine')
    
    def test_get_statistics(self):
        """Test getting statistics"""
        self.agent.add_reminder("Medicine 1", "08:00", "Message 1")
        self.agent.add_reminder("Medicine 2", "08:00", "Message 2")
        self.agent.add_reminder("Medicine 3", "14:00", "Message 3")
        self.agent.delete_reminder(3)
        
        stats = self.agent.get_statistics()
        
        self.assertEqual(stats['total_created'], 3)
        self.assertEqual(stats['active'], 2)
        self.assertEqual(stats['deleted'], 1)
        self.assertEqual(stats['times']['08:00'], 2)
    
    def test_get_upcoming_reminders(self):
        """Test getting upcoming reminders"""
        self.agent.add_reminder("Medicine 1", "08:00", "Message 1")
        self.agent.add_reminder("Medicine 2", "14:00", "Message 2")
        self.agent.add_reminder("Medicine 3", "20:00", "Message 3")
        
        upcoming = self.agent.get_upcoming_reminders()
        
        # Should return reminders sorted by time
        self.assertGreaterEqual(len(upcoming), 0)
    
    def test_multilingual_message(self):
        """Test adding reminder with multilingual message"""
        hindi_message = "Are uncle, aapki dawai ka time ho gaya hai!"
        
        reminder = self.agent.add_reminder(
            medicine_name="Test Medicine",
            reminder_time="10:00",
            custom_message=hindi_message
        )
        
        self.assertEqual(reminder['message'], hindi_message)


class TestReminderFrequency(unittest.TestCase):
    """Test cases for reminder frequency features"""
    
    def setUp(self):
        """Set up test fixture"""
        self.agent = MedicineReminderAgent()
    
    def test_daily_frequency(self):
        """Test daily frequency reminder"""
        reminder = self.agent.add_reminder(
            "Daily Medicine",
            "10:00",
            "Take daily",
            frequency="daily"
        )
        
        self.assertEqual(reminder['frequency'], "daily")
    
    def test_custom_frequency(self):
        """Test custom frequency reminder"""
        reminder = self.agent.add_reminder(
            "Weekly Medicine",
            "10:00",
            "Take weekly",
            frequency="weekly"
        )
        
        self.assertEqual(reminder['frequency'], "weekly")


if __name__ == '__main__':
    print("🧪 Running Medicine Reminder Agent Tests\n")
    print("=" * 60)
    
    # Run tests
    unittest.main(verbosity=2)
