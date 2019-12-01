import datetime
import re

from collections import defaultdict
from functools import reduce

import numpy as np

from aoc.challenge_base import ChallengeBase

class GuardSleepingLog:
    """
    Guard's sleep patterns for a day
    """
    def __init__(self, guard_id, sleep_periods):
        """
        Constructor
        """
        self.guard_id = guard_id
        self.sleep_periods = sleep_periods

    def total_sleep_duration(self):
        """
        Compute total sleeping time
        """
        return reduce(lambda x, y: x + (y[1] - y[0]), self.sleep_periods, 0)

class Challenge(ChallengeBase):
    """
    Day 4 challenges
    """
    def parse_guard_patterns(self):
        """
        Parse guard sleeping patterns
        """
        # First, sort the entries by datetime
        entries = []
        for line in self.lines:
            # Get the date/time
            date_part, desc = line.split("] ")
            date = datetime.datetime.fromisoformat(date_part[1:])
            entries.append((date, desc))
            
        entries.sort(key=lambda x: x[0])

        # Now, parse each guard's activities
        begin_re = re.compile(r"Guard #(\d+) begins shift")
        self.guard_patterns = []
        current_guard_id = None
        current_sleep_periods = []

        for index, (date, desc) in enumerate(entries):
            # If we're just starting out, ensure the first line is a begin line!
            begin_match = begin_re.match(desc)
            if not current_guard_id and not begin_match:
                raise ValueError("Need a guard beginning shift to start!")

            # What kind of event is it?
            if begin_match:
                # Save the previous guard, if any
                if current_guard_id:
                    self.guard_patterns.append(GuardSleepingLog(current_guard_id, current_sleep_periods))

                # Start recording new guard
                current_guard_id = int(begin_match.group(1))
                current_sleep_periods = []
            elif desc.startswith("falls asleep"):
                current_sleep_periods.append([date.minute])
            elif desc.startswith("wakes up"):
                current_sleep_periods[-1].append(date.minute)
            else:
                raise ValueError(f"Unexpected guard status in entry {index}: {desc}")
        
        # Save the last guard
        self.guard_patterns.append(GuardSleepingLog(current_guard_id, current_sleep_periods))

    def challenge1(self):
        """
        Day 4 challenge 1
        """
        self.parse_guard_patterns()

        # Find the guard with the longest total sleep duration
        guard_durations = defaultdict(int)
        for log_entry in self.guard_patterns:
            guard_durations[log_entry.guard_id] += log_entry.total_sleep_duration()

        sleepiest_guard = max(guard_durations, key=lambda k: guard_durations[k])

        # Find the modal minute for this guard
        minute_array = np.zeros((60), dtype=np.uint32)
        for log_entry in self.guard_patterns:
            if log_entry.guard_id == sleepiest_guard:
                for sleep_period in log_entry.sleep_periods:
                    minute_array[sleep_period[0]:sleep_period[1]] += 1
        
        modal_minute = np.argmax(minute_array)
        print(f"Sleepiest guard: {sleepiest_guard}, modal minute: {modal_minute}")

    def challenge2(self):
        """
        Day 4 challenge 2
        """
        # We have all the guard patterns already.
        # Which one is most frequently asleep on the same minute?
        max_guard_id = max([log_entry.guard_id for log_entry in self.guard_patterns])
        guard_minute_counts = np.zeros((max_guard_id + 1, 60), dtype=np.uint32)
        for log_entry in self.guard_patterns:
            for sleep_period in log_entry.sleep_periods:
                guard_minute_counts[log_entry.guard_id, sleep_period[0]:sleep_period[1]] += 1

        guard_id, minute = np.unravel_index(np.argmax(guard_minute_counts), np.shape(guard_minute_counts))
        print(f"Modal guard: {guard_id} at minute {minute}")
