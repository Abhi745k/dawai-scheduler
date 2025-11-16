"""
Live Reminder Monitor - Continuously checks and triggers reminders
"""
from medicine_reminder_core import MedicineReminderAgent
from datetime import datetime
import time

def auto_correct_message(text):
    """
    Auto-correct common Hindi/English spelling mistakes in medicine messages
    """
    corrections = {
        # Common Hindi medicine words
        'dwai': 'dawai',
        'dawa': 'dawai',
        'dwae': 'dawai',
        'dwaii': 'dawai',
        'dwayi': 'dawai',
        'dwaayi': 'dawai',
        'dwa': 'dawai',
        
        # Time related
        'tym': 'time',
        'tyme': 'time',
        'tym': 'time',
        'ho gya': 'ho gaya',
        'hogya': 'ho gaya',
        'hogaya': 'ho gaya',
        
        # Common words
        'lena': 'lena',
        'lene': 'lene',
        'lelo': 'le lo',
        'lelijiye': 'le lijiye',
        'lelena': 'le lena',
        'lelo': 'le lo',
        'khana': 'khana',
        'khane': 'khane',
        'baad': 'baad',
        'bad': 'baad',
        'pahle': 'pehle',
        'pahele': 'pehle',
        'subha': 'subah',
        'subh': 'subah',
        'rat': 'raat',
        'dophar': 'dopahar',
        'dopaher': 'dopahar',
        
        # Medicine types
        'bp': 'BP',
        'dabetes': 'diabetes',
        'diabetis': 'diabetes',
        'diabeties': 'diabetes',
        'sugar': 'sugar',
        'thyrod': 'thyroid',
        'thyrode': 'thyroid',
        'hart': 'heart',
        'hert': 'heart',
        
        # Actions
        'bhul': 'bhool',
        'bhule': 'bhoole',
        'bhulna': 'bhoolna',
        'yaad': 'yaad',
        'yad': 'yaad',
        'dhyan': 'dhyan',
        'dyan': 'dhyan',
    }
    
    # Create corrected version
    corrected = text
    changes_made = []
    
    # Check each word
    words = text.split()
    corrected_words = []
    
    for word in words:
        original_word = word
        lower_word = word.lower()
        
        # Check if word needs correction
        if lower_word in corrections:
            # Preserve original case pattern
            if word.isupper():
                corrected_word = corrections[lower_word].upper()
            elif word[0].isupper():
                corrected_word = corrections[lower_word].capitalize()
            else:
                corrected_word = corrections[lower_word]
            
            corrected_words.append(corrected_word)
            if original_word != corrected_word:
                changes_made.append(f"'{original_word}' → '{corrected_word}'")
        else:
            corrected_words.append(word)
    
    corrected = ' '.join(corrected_words)
    
    return corrected, changes_made

# Initialize agent
agent = MedicineReminderAgent()

# User Options
print("\n" + "="*50)
print("   MEDICINE REMINDER SETUP")
print("="*50)

# Get reminder details from user
medicine = input("\n💊 Medicine Name: ")
time_input = input("⏰ Time (HH:MM format, e.g., 13:30): ")
original_message = input("📢 Custom Message: ")

# Auto-correct the message
corrected_message, corrections = auto_correct_message(original_message)

# Show corrections if any
if corrections:
    print("\n" + "="*50)
    print("🔍 AUTO-CORRECTION DETECTED")
    print("="*50)
    print("\n📝 Original Message:")
    print(f"   {original_message}")
    print("\n✅ Corrected Message:")
    print(f"   {corrected_message}")
    print("\n🔄 Changes Made:")
    for change in corrections:
        print(f"   • {change}")
    print("\n" + "="*50)
    
    # Ask user to confirm
    choice = input("\n✓ Use corrected message? (y/n): ").lower()
    if choice == 'y' or choice == 'yes' or choice == '':
        message = corrected_message
        print("✅ Using corrected message")
    else:
        message = original_message
        print("📌 Using original message as typed")
else:
    message = original_message
    print("✅ No corrections needed - message looks good!")

# Frequency options
print("\n🔄 Frequency Options:")
print("  1. Daily (har din)")
print("  2. One-time (sirf ek baar)")
print("  3. Custom days (specific days)")
freq_choice = input("Select option (1/2/3): ")

if freq_choice == "1":
    frequency = "daily"
    repeat_msg = "Daily"
elif freq_choice == "2":
    frequency = "once"
    repeat_msg = "One-time only"
elif freq_choice == "3":
    days = input("How many days? (e.g., 7): ")
    frequency = f"{days}_days"
    repeat_msg = f"For {days} days"
else:
    frequency = "daily"
    repeat_msg = "Daily (default)"

# Message repeat options
print("\n🔁 Message Play Options:")
print("  1. Play once at scheduled time")
print("  2. Repeat multiple times")
play_choice = input("Select option (1/2): ")

if play_choice == "2":
    repeat_count = int(input("How many times to repeat? (e.g., 3): "))
    repeat_interval = int(input("Interval in minutes? (e.g., 5): "))
else:
    repeat_count = 1
    repeat_interval = 0

# Add your reminder
agent.add_reminder(
    medicine_name=medicine,
    reminder_time=time_input,
    custom_message=message,
    frequency=frequency
)

print("\n" + "="*50)
print("✅ Reminder Monitor Started!")
print(f"⏰ Watching for {time_input}...")
print(f"🔄 Frequency: {repeat_msg}")
print(f"🔁 Will play {repeat_count} time(s)")
print("📢 Press Ctrl+C to stop\n")
print("="*50)

# Continuous monitoring
try:
    while True:
        current_time = datetime.now().strftime("%H:%M")
        
        # Check every minute
        triggered = agent.check_and_trigger_reminders(current_time)
        
        if triggered:
            print(f"\n🔔 REMINDER TRIGGERED at {current_time}!")
            
            # Play audio multiple times if requested
            for i in range(repeat_count):
                print(f"🔊 Playing audio (Play {i+1}/{repeat_count})...")
                try:
                    import os
                    os.system("start reminder_1.mp3")  # Windows
                except:
                    print("Audio file: reminder_1.mp3")
                
                # Wait between repeats
                if i < repeat_count - 1:
                    print(f"⏳ Waiting {repeat_interval} minutes before next play...")
                    time.sleep(repeat_interval * 60)
            
            # If one-time only, stop the monitor
            if frequency == "once":
                print("\n✅ One-time reminder completed. Stopping monitor.")
                break
        
        # Wait 30 seconds before next check
        time.sleep(30)
        
except KeyboardInterrupt:
    print("\n\n⏹️ Reminder monitor stopped.")
