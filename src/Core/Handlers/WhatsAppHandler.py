import pywhatkit
from datetime import datetime, timedelta
from src.Core.Handlers.BaseHandler import BaseHandler


class WhatsAppHandler(BaseHandler):
    """Handles sending WhatsApp messages."""

    async def run(self) -> None:
        number = self._get_number()
        if not number:
            return

        for message in self.ui.input_loop("Message: ", f"Sending to {number}. What do you want to say?"):
            schedule = self._get_schedule()
            if schedule is None:
                return
            self._send(number, message, schedule)

    def _get_number(self) -> str | None:
        while True:
            number = input("Phone number (with country code, e.g. +573001234567): ").strip()
            if not number:
                continue
            if number.lower() == "back":
                return None
            if not number.startswith("+"):
                print("❌ Number must start with country code e.g. +573001234567\n")
                continue
            return number

    def _get_schedule(self) -> tuple[int, int] | None:
        """
        Ask the user if they want to schedule the message or send instantly.
        Returns (hour, minute) tuple or (now + 1 min) for instant send.
        """
        print("\nWhen do you want to send it?")
        print("  1. Send instantly")
        print("  2. Schedule for a specific time")

        while True:
            choice = input("Choose (1 or 2): ").strip()

            if choice == "1":
                # pywhatkit needs at least 1 minute in the future
                send_time = datetime.now() + timedelta(minutes=1)
                print(f"📨 Sending in ~1 minute at {send_time.strftime('%H:%M')}...")
                return send_time.hour, send_time.minute

            elif choice == "2":
                return self._get_time_input()

            elif choice.lower() == "back":
                return None

            else:
                print("❌ Please enter 1 or 2.\n")

    def _get_time_input(self) -> tuple[int, int] | None:
        """Ask for hour and minute separately and validate them."""
        while True:
            try:
                hour = int(input("Hour (0-23): ").strip())
                minute = int(input("Minute (0-59): ").strip())

                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    print("❌ Invalid time. Hour must be 0-23 and minute 0-59.\n")
                    continue

                # Make sure the time is in the future
                now = datetime.now()
                scheduled = now.replace(hour=hour, minute=minute, second=0)
                if scheduled <= now:
                    print("❌ That time has already passed. Please enter a future time.\n")
                    continue

                print(f"📨 Scheduled for {hour:02d}:{minute:02d}...")
                return hour, minute

            except ValueError:
                print("❌ Please enter valid numbers.\n")

    def _send(self, number: str, message: str, schedule: tuple[int, int]) -> None:
        hour, minute = schedule
        pywhatkit.sendwhatmsg(
            number,
            message,
            hour,
            minute,
            wait_time=15,  # seconds to wait for WhatsApp Web to load
            tab_close=True,  # close the tab after sending
            close_time=3  # seconds to wait before closing
        )
        print("✅ Message sent!")