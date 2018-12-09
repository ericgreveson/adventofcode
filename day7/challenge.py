from aoc.challenge_base import ChallengeBase

class Challenge(ChallengeBase):
    """
    Day 7 challenges
    """
    def parse_input(self):
        """
        Pre-process input
        """
        # Get dependencies as pairs (X, Y)
        self.deps = []
        for line in self.lines:
            # All lines are in following format:
            # "Step X must be finished before step Y can begin."
            x = line[5]
            y = line[36]
            self.deps.append((x, y))

        # Get set of steps
        self.steps = set()
        for dep in self.deps:
            self.steps.add(dep[0])
            self.steps.add(dep[1])

    def challenge1(self):
        """
        Day 7 challenge 1
        """
        self.parse_input()

        # Figure out the order iteratively, using alpha ordering to break ties
        remaining_deps = self.deps.copy()
        remaining_steps = self.steps.copy()
        ordered_steps = []
        while remaining_steps:
            # What are the next steps with no dependencies left?
            steps_with_no_deps = set(remaining_steps)
            for dep in remaining_deps:
                steps_with_no_deps.discard(dep[1])

            # Next step is the alphabetically lowest one
            next_step = sorted(steps_with_no_deps)[0]

            # Remove the dependencies whose steps we have satisfied
            remaining_deps = list(filter(lambda dep: dep[0] != next_step, remaining_deps))

            # Remove from steps available, and add to the ordered steps
            remaining_steps.remove(next_step)
            ordered_steps.append(next_step)

        # Write out the ordered steps in the required format
        steps_list = "".join(ordered_steps)
        print(f"Steps: {steps_list}")

    def challenge2(self):
        """
        Day 7 challenge 2
        """
        # This time we simulate the 5 workers and a "completed steps" pool
        remaining_deps = self.deps.copy()
        remaining_steps = self.steps.copy()
        
        num_workers = 5
        completed_steps = []
        worker_tasks = [None] * num_workers
        current_second = 0
        while remaining_steps:
            # What are the next steps with no dependencies left (in order)?
            steps_with_no_deps = set(remaining_steps)
            for dep in remaining_deps:
                steps_with_no_deps.discard(dep[1])
            for worker_task in worker_tasks:
                if worker_task:
                    steps_with_no_deps.discard(worker_task[0])

            steps_with_no_deps = sorted(steps_with_no_deps)

            # Assign available steps to workers, if there are any free
            for index, worker_task in enumerate(worker_tasks):
                if steps_with_no_deps and not worker_task:
                    # Assign next available step
                    next_step = steps_with_no_deps[0]
                    worker_tasks[index] = [next_step, 61 + ord(next_step) - ord('A')]
                    steps_with_no_deps = steps_with_no_deps[1:]

            # Advance the timeline!
            current_second += 1

            # Take some time off each worker's task, and figure out if anyone's finished
            for index, worker_task in enumerate(worker_tasks):
                if worker_task:
                    worker_task[1] -= 1
                    if worker_task[1] == 0:
                        # Task complete! Remove the dependencies whose steps we have satisfied
                        worker_step = worker_task[0]
                        remaining_deps = list(filter(lambda dep: dep[0] != worker_step, remaining_deps))
                        remaining_steps.remove(worker_step)
                        completed_steps.append(worker_step)
                        worker_tasks[index] = None


        print(f"Total time: {current_second}")
