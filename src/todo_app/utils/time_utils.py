"""Time parsing and validation utilities for the Todo application.

This module provides functions for parsing and validating time strings, reminder inputs,
and performing time-related calculations for task scheduling.
"""

import re
from datetime import datetime, timedelta
from typing import Optional, Tuple


def validate_time(time_str: str) -> bool:
    """Validate time string format (HH:MM in 24-hour format).

    Args:
        time_str: Time string to validate (e.g., "14:30", "09:00")

    Returns:
        True if valid time format, False otherwise

    Examples:
        >>> validate_time("14:30")
        True
        >>> validate_time("23:59")
        True
        >>> validate_time("25:00")
        False
        >>> validate_time("13:75")
        False
    """
    if not time_str or not isinstance(time_str, str):
        return False

    # Regex pattern: HH:MM where HH is 00-23 and MM is 00-59
    pattern = r'^([01][0-9]|2[0-3]):[0-5][0-9]$'
    return bool(re.match(pattern, time_str))


def parse_time(time_str: str) -> Optional[str]:
    """Parse and validate time string, returning normalized format or None.

    Args:
        time_str: Time string to parse (e.g., "14:30", "9:00", "23:59")

    Returns:
        Normalized time string "HH:MM" if valid, None otherwise

    Examples:
        >>> parse_time("14:30")
        '14:30'
        >>> parse_time("9:00")
        None  # Invalid - must be zero-padded "09:00"
        >>> parse_time("invalid")
        None
    """
    if not time_str:
        return None

    time_str = time_str.strip()

    if validate_time(time_str):
        return time_str

    return None


def parse_reminder(reminder_str: str) -> Optional[dict]:
    """Parse reminder string into offset dictionary.

    Supports formats like:
    - "15 minutes", "15 minute", "15 min"
    - "2 hours", "2 hour", "2 hr"
    - "1 day", "1 days"

    Args:
        reminder_str: Reminder string to parse (e.g., "15 minutes", "1 hour", "2 days")

    Returns:
        Dictionary with {offset_value: int, offset_unit: str, sent: bool, sent_at: None}
        or None if invalid format

    Examples:
        >>> parse_reminder("15 minutes")
        {'offset_value': 15, 'offset_unit': 'minutes', 'sent': False, 'sent_at': None}
        >>> parse_reminder("1 hour")
        {'offset_value': 1, 'offset_unit': 'hours', 'sent': False, 'sent_at': None}
        >>> parse_reminder("invalid")
        None
    """
    if not reminder_str:
        return None

    reminder_str = reminder_str.strip().lower()

    # Pattern: number + whitespace + unit
    pattern = r'^(\d+)\s+(minute|minutes|min|hour|hours|hr|day|days)$'
    match = re.match(pattern, reminder_str)

    if not match:
        return None

    value_str, unit_str = match.groups()
    value = int(value_str)

    # Normalize unit to plural form
    if unit_str in ('minute', 'minutes', 'min'):
        unit = 'minutes'
    elif unit_str in ('hour', 'hours', 'hr'):
        unit = 'hours'
    elif unit_str in ('day', 'days'):
        unit = 'days'
    else:
        return None

    return {
        'offset_value': value,
        'offset_unit': unit,
        'sent': False,
        'sent_at': None
    }


def format_reminder_display(reminder: dict) -> str:
    """Format reminder dictionary for display.

    Args:
        reminder: Reminder dictionary with offset_value, offset_unit, sent, sent_at

    Returns:
        Formatted string for display (e.g., "15 minutes before (pending)")

    Examples:
        >>> format_reminder_display({'offset_value': 15, 'offset_unit': 'minutes', 'sent': False, 'sent_at': None})
        '15 minutes before (pending)'
        >>> format_reminder_display({'offset_value': 1, 'offset_unit': 'hours', 'sent': True, 'sent_at': datetime(2026, 1, 15, 14, 30)})
        '1 hour before (sent on 2026-01-15 14:30)'
    """
    value = reminder['offset_value']
    unit = reminder['offset_unit']
    sent = reminder['sent']
    sent_at = reminder.get('sent_at')

    # Format offset
    unit_singular = unit.rstrip('s') if value == 1 else unit
    offset_str = f"{value} {unit_singular} before"

    # Format status
    if sent and sent_at:
        status_str = f"sent on {sent_at.strftime('%Y-%m-%d %H:%M')}"
    elif sent:
        status_str = "sent"
    else:
        status_str = "pending"

    return f"{offset_str} ({status_str})"


def calculate_reminder_trigger_time(due_datetime: datetime, reminder: dict) -> Optional[datetime]:
    """Calculate absolute time when reminder should trigger.

    Args:
        due_datetime: The task's due datetime
        reminder: Reminder dictionary with offset_value and offset_unit

    Returns:
        datetime when reminder should trigger, or None if invalid

    Examples:
        >>> due = datetime(2026, 1, 15, 14, 30)
        >>> reminder = {'offset_value': 15, 'offset_unit': 'minutes', 'sent': False, 'sent_at': None}
        >>> calculate_reminder_trigger_time(due, reminder)
        datetime.datetime(2026, 1, 15, 14, 15)
    """
    if not due_datetime:
        return None

    offset_value = reminder.get('offset_value')
    offset_unit = reminder.get('offset_unit')

    if offset_value is None or not offset_unit:
        return None

    # Convert offset to timedelta
    if offset_unit == 'minutes':
        delta = timedelta(minutes=offset_value)
    elif offset_unit == 'hours':
        delta = timedelta(hours=offset_value)
    elif offset_unit == 'days':
        delta = timedelta(days=offset_value)
    else:
        return None

    return due_datetime - delta
