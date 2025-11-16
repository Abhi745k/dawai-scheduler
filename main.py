"""
Mobile App Main Entry Point
Medicine Reminder App using Kivy Framework

This is the main application file for the mobile version.
For the Kaggle demo, use the medicine_reminder_agent.ipynb notebook instead.
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window

from medicine_reminder_core import MedicineReminderAgent
from datetime import datetime
import json


class ReminderListItem(BoxLayout):
    """Widget for displaying a single reminder in the list"""
    
    def __init__(self, reminder_data, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 100
        self.padding = 10
        self.spacing = 10
        
        self.reminder_data = reminder_data
        self.app_instance = app_instance
        
        # Reminder info layout
        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)
        
        # Medicine name with white text
        name_label = Label(
            text=f"💊 {reminder_data['medicine_name']}", 
            font_size='18sp',
            halign='left',
            valign='middle',
            text_size=(self.width, None),
            color=(1, 1, 1, 1)  # White text on black
        )
        
        # Time with white text
        time_label = Label(
            text=f"⏰ {reminder_data['time']}", 
            font_size='16sp',
            halign='left',
            valign='middle',
            text_size=(self.width, None),
            color=(0.9, 0.9, 0.9, 1)  # Light gray
        )
        
        info_layout.add_widget(name_label)
        info_layout.add_widget(time_label)
        
        # Action buttons layout
        button_layout = BoxLayout(orientation='horizontal', size_hint_x=0.3)
        
        # Edit button - Blue
        edit_btn = Button(
            text='✏️ Edit',
            size_hint_x=0.5,
            background_color=(0.1, 0.5, 0.9, 1),  # Bright blue
            color=(1, 1, 1, 1)  # White text
        )
        edit_btn.bind(on_press=self.on_edit)
        
        # Delete button - Red
        delete_btn = Button(
            text='🗑️ Del',
            size_hint_x=0.5,
            background_color=(0.9, 0.1, 0.1, 1),  # Bright red
            color=(1, 1, 1, 1)  # White text
        )
        delete_btn.bind(on_press=self.on_delete)
        
        button_layout.add_widget(edit_btn)
        button_layout.add_widget(delete_btn)
        
        self.add_widget(info_layout)
        self.add_widget(button_layout)
    
    def on_edit(self, instance):
        """Handle edit button press"""
        self.app_instance.show_edit_screen(self.reminder_data)
    
    def on_delete(self, instance):
        """Handle delete button press"""
        self.app_instance.delete_reminder(self.reminder_data['id'])


class MedicineReminderApp(App):
    """Main Kivy application for Medicine Reminder"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent = MedicineReminderAgent()
        self.main_layout = None
        
        # Try to load existing schedule
        try:
            self.agent.import_schedule('app_schedule.json')
        except:
            pass
    
    def build(self):
        """Build the main application UI"""
        # Professional Black Background
        Window.clearcolor = (0, 0, 0, 1)  # Pure black
        
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header with white text on black
        header = Label(
            text='💊 Medicine Reminder',
            font_size='24sp',
            size_hint_y=0.1,
            bold=True,
            color=(1, 1, 1, 1)  # White text
        )
        
        # Add reminder button with professional green
        add_btn = Button(
            text='➕ Add New Reminder',
            size_hint_y=0.08,
            background_color=(0.1, 0.8, 0.3, 1),  # Bright green
            color=(1, 1, 1, 1),  # White text
            font_size='18sp',
            bold=True
        )
        add_btn.bind(on_press=self.show_add_screen)
        
        # Reminders list
        self.reminders_container = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None
        )
        self.reminders_container.bind(minimum_height=self.reminders_container.setter('height'))
        
        scroll_view = ScrollView(size_hint=(1, 0.82))
        scroll_view.add_widget(self.reminders_container)
        
        self.main_layout.add_widget(header)
        self.main_layout.add_widget(add_btn)
        self.main_layout.add_widget(scroll_view)
        
        # Refresh reminders list
        self.refresh_reminders()
        
        # Schedule reminder checking every minute
        Clock.schedule_interval(self.check_reminders, 60)
        
        return self.main_layout
    
    def refresh_reminders(self):
        """Refresh the reminders list display"""
        self.reminders_container.clear_widgets()
        
        reminders = self.agent.view_reminders()
        
        if len(reminders) == 0:
            no_reminders = Label(
                text='📭 No reminders scheduled yet.\nTap "Add New Reminder" to get started!',
                font_size='16sp',
                color=(0.7, 0.7, 0.7, 1)  # Gray text
            )
            self.reminders_container.add_widget(no_reminders)
        else:
            # Sort by time
            active_reminders = [r for r in self.agent.reminders if r['active']]
            active_reminders.sort(key=lambda x: x['time'])
            
            for reminder in active_reminders:
                item = ReminderListItem(reminder, self)
                self.reminders_container.add_widget(item)
    
    def show_add_screen(self, instance):
        """Show the add reminder screen"""
        # Clear main layout
        self.main_layout.clear_widgets()
        
        # Create add screen
        add_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Header
        header = Label(
            text='➕ Add New Reminder',
            font_size='22sp',
            size_hint_y=0.1,
            bold=True
        )
        
        # Form fields
        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.7)
        
        # Medicine name
        form_layout.add_widget(Label(text='Medicine Name:', font_size='16sp'))
        self.medicine_input = TextInput(
            hint_text='e.g., Amlodipine (BP)',
            multiline=False,
            font_size='16sp'
        )
        form_layout.add_widget(self.medicine_input)
        
        # Time
        form_layout.add_widget(Label(text='Time (HH:MM):', font_size='16sp'))
        self.time_input = TextInput(
            hint_text='e.g., 08:00',
            multiline=False,
            font_size='16sp'
        )
        form_layout.add_widget(self.time_input)
        
        # Custom message
        form_layout.add_widget(Label(text='Reminder Message:', font_size='16sp'))
        self.message_input = TextInput(
            hint_text='Enter your custom message in any language...',
            multiline=True,
            font_size='16sp'
        )
        form_layout.add_widget(self.message_input)
        
        # Buttons layout
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.1)
        
        cancel_btn = Button(
            text='❌ Cancel',
            background_color=(0.7, 0.7, 0.7, 1),
            font_size='18sp'
        )
        cancel_btn.bind(on_press=self.back_to_main)
        
        save_btn = Button(
            text='✅ Save Reminder',
            background_color=(0.2, 0.7, 0.3, 1),
            font_size='18sp'
        )
        save_btn.bind(on_press=self.save_new_reminder)
        
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(save_btn)
        
        add_layout.add_widget(header)
        add_layout.add_widget(form_layout)
        add_layout.add_widget(button_layout)
        
        self.main_layout.add_widget(add_layout)
    
    def save_new_reminder(self, instance):
        """Save the new reminder"""
        medicine = self.medicine_input.text.strip()
        time = self.time_input.text.strip()
        message = self.message_input.text.strip()
        
        if not medicine or not time or not message:
            # Show error (in production, use a popup)
            print("⚠️ Please fill all fields")
            return
        
        # Add reminder
        self.agent.add_reminder(
            medicine_name=medicine,
            reminder_time=time,
            custom_message=message
        )
        
        # Save to file
        self.agent.export_schedule('app_schedule.json')
        
        # Return to main screen
        self.back_to_main(instance)
    
    def show_edit_screen(self, reminder_data):
        """Show edit screen for a reminder"""
        # Similar to add screen but pre-populated
        # Implementation similar to show_add_screen
        print(f"Edit reminder {reminder_data['id']}")
    
    def delete_reminder(self, reminder_id):
        """Delete a reminder"""
        self.agent.delete_reminder(reminder_id)
        self.agent.export_schedule('app_schedule.json')
        self.refresh_reminders()
    
    def back_to_main(self, instance):
        """Return to main screen"""
        self.main_layout.clear_widgets()
        self.build()
    
    def check_reminders(self, dt):
        """Check and trigger reminders (called every minute)"""
        current_time = datetime.now().strftime("%H:%M")
        triggered = self.agent.check_and_trigger_reminders(current_time)
        
        # In production, this would trigger notifications
        # For now, just print
        if triggered:
            print(f"⏰ {len(triggered)} reminder(s) triggered!")
    
    def on_stop(self):
        """Called when app is closing"""
        # Save schedule
        try:
            self.agent.export_schedule('app_schedule.json')
        except:
            pass


if __name__ == '__main__':
    MedicineReminderApp().run()
