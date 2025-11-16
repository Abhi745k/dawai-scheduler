"""
Quick Demo Script for Medicine Reminder Agent
Run this to see the agent in action without opening the notebook
"""

from medicine_reminder_core import MedicineReminderAgent
import time


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def main():
    """Main demo function"""
    print("\n🤖 Medicine Reminder Agent - Quick Demo")
    print("=" * 70)
    
    # Initialize agent
    print("\n📝 Initializing agent...")
    agent = MedicineReminderAgent()
    
    # Add sample reminders
    print_header("➕ ADDING SAMPLE REMINDERS")
    
    print("Adding reminder 1: BP Medicine (Hindi)")
    agent.add_reminder(
        medicine_name="Amlodipine (BP)",
        reminder_time="08:00",
        custom_message="Are uncle, aapki BP ki dawai ka time ho gaya hai! Subah ki dawai le lijiye.",
        frequency="daily"
    )
    
    print("\nAdding reminder 2: Diabetes Medicine (English)")
    agent.add_reminder(
        medicine_name="Metformin (Diabetes)",
        reminder_time="08:30",
        custom_message="Good morning! It's time for your diabetes medicine. Please take it with breakfast.",
        frequency="daily"
    )
    
    print("\nAdding reminder 3: Heart Medicine (Mixed Hindi-English)")
    agent.add_reminder(
        medicine_name="Atorvastatin (Heart)",
        reminder_time="21:00",
        custom_message="Namaste ji! Raat ki heart medicine lena mat bhooliye. Dinner ke baad le lijiye.",
        frequency="daily"
    )
    
    print("\nAdding reminder 4: Thyroid Medicine (Hindi)")
    agent.add_reminder(
        medicine_name="Thyroxine (Thyroid)",
        reminder_time="06:00",
        custom_message="Suprabhat! Aapki thyroid ki dawai ka samay hai. Khali pet lena hai.",
        frequency="daily"
    )
    
    # View schedule
    print_header("📋 VIEWING REMINDER SCHEDULE")
    agent.view_reminders()
    
    # Get statistics
    print_header("📊 STATISTICS")
    stats = agent.get_statistics()
    print(f"Total Reminders Created: {stats['total_created']}")
    print(f"Active Reminders: {stats['active']}")
    print(f"Deleted Reminders: {stats['deleted']}")
    
    print("\nReminders by Time:")
    for time_slot, count in sorted(stats['times'].items()):
        print(f"  {time_slot} - {count} reminder(s)")
    
    # Edit a reminder
    print_header("✏️ EDITING REMINDER")
    print("Editing reminder ID 1 (changing time and message)...")
    agent.edit_reminder(
        reminder_id=1,
        reminder_time="08:15",
        custom_message="Are uncle, BP ki dawai lena yaad hai na? Jaldi se le lijiye!"
    )
    print("\nUpdated schedule:")
    agent.view_reminders()
    
    # Delete a reminder
    print_header("🗑️ DELETING REMINDER")
    print("Deleting reminder ID 4 (Thyroid medicine)...")
    agent.delete_reminder(4)
    print("\nUpdated schedule:")
    agent.view_reminders()
    
    # Simulate reminders at different times
    print_header("⏰ SIMULATING REMINDER TRIGGERS")
    
    test_times = ["08:00", "08:15", "08:30", "21:00"]
    
    for test_time in test_times:
        print(f"\n🕐 Checking time: {test_time}")
        triggered = agent.check_and_trigger_reminders(test_time)
        if not triggered:
            print("   No reminders at this time.")
    
    # Export schedule
    print_header("💾 EXPORTING SCHEDULE")
    agent.export_schedule("demo_schedule.json")
    print("Schedule saved to: demo_schedule.json")
    
    # Generate TTS sample
    print_header("🔊 TEXT-TO-SPEECH DEMO")
    print("Generating TTS for sample message...")
    sample_message = "Namaste! Aapki dawai ka time ho gaya hai."
    audio_file = agent.generate_tts(sample_message, "demo_reminder.mp3")
    
    if audio_file:
        print(f"\n✅ Audio file generated: {audio_file}")
        print("   You can play this file to hear the reminder!")
    else:
        print("\n⚠️ TTS not available (install gtts: pip install gtts)")
        print(f"   Message would be: {sample_message}")
    
    # Summary
    print_header("✅ DEMO COMPLETE")
    print("Features demonstrated:")
    print("  ✓ Adding reminders with multilingual messages")
    print("  ✓ Viewing and managing schedules")
    print("  ✓ Editing and deleting reminders")
    print("  ✓ Checking and triggering reminders")
    print("  ✓ Getting statistics")
    print("  ✓ Exporting schedules")
    print("  ✓ Text-to-speech generation")
    
    print("\n💡 Next Steps:")
    print("  1. Open medicine_reminder_agent.ipynb for full interactive demo")
    print("  2. Run main.py to try the mobile app prototype")
    print("  3. Run test_reminder_agent.py to verify functionality")
    
    print("\n" + "=" * 70)
    print("🙏 Thank you for trying the Medicine Reminder Agent!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
