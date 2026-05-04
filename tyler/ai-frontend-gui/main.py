import os
import random

from dataclasses import dataclass, fields

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pandas as pd
import pulp
import pygame
import webview


@dataclass
class ButtonInput:
    num_office_hours: int
    excel_file_path: str
    unavailable_hours: str

    def pyprint(self):
        fieldvals = [_ for _ in fields(self)]
        for fieldval in fieldvals:
            val = getattr(self, fieldval.name)
            if val == None: continue
            print(f"{fieldval.name}: {val}-{type(val)}")

class MainApi:
    """Main bridge for frontend javascript to execute python."""
    def __init__(self):
        self._window: webview.Window|None = None

    @property
    def window(self) -> webview.Window:
        assert self._window is not None
        return self._window
    @window.setter
    def window(self, win):
        self._window = win

    def open_file_dialog(self):
        file_types = ("Excel File (*.xlsx)",)
        result = self.window.create_file_dialog(
            webview.FileDialog.OPEN, allow_multiple=False, file_types=file_types
        )
        return result;

    def _play_button_sound(self):
        button_sound = pygame.mixer.Sound(random.choice(["vova-buhh.ogg", "tyler-buhh.ogg", "ollie-buhh.ogg", "jake-buhh.ogg"]))
        button_sound.set_volume(random.choice([.7, .9, 1]))
        button_sound.play()

    def button_pressed(self, input: list):
        self._play_button_sound();
        if len(input) != len(fields(ButtonInput)): return

        button_input = ButtonInput(*input)
        button_input.unavailable_hours = button_input.unavailable_hours.replace(" ", "")
        #button_input.pyprint()

        df = pd.read_excel(button_input.excel_file_path) # FIND BETTER WAY TO INPUT INTO APP
        #print(df.head()) # Input data

        df = df.set_index(df.columns[0])  # makes student names the index
        availability = 1 - df
        #availability = availability.drop(columns=['M10', 'W10', 'F10'])
        availability = availability.drop(columns=button_input.unavailable_hours.split(","))

        # Drop Professor Unavailability (Constraints)
        availability = availability.drop(columns=['M8', 'M12', 'T12', 'W12','R8', 'R9', 'R10', 'R12','F8', 'F12']) # MAKE APP INPUT

        # Get list of students and time slots
        students = availability.index.tolist()
        times = availability.columns.tolist()

        # Create problem
        model = pulp.LpProblem("OfficeHoursOptimization", pulp.LpMaximize)

        # Decision variables
        x = pulp.LpVariable.dicts("timeslot", times, cat='Binary')
        y = pulp.LpVariable.dicts("student", students, cat='Binary')

        # Objective: maximize covered students
        model += pulp.lpSum([y[s] for s in students])

        # Constraint: pick exactly 5 time slots
        model += pulp.lpSum([x[t] for t in times]) == button_input.num_office_hours

        # Constraint: student coverage
        for s in students:
            model += y[s] <= pulp.lpSum([availability.loc[s, t] * x[t] for t in times])

        # Solve
        model.solve(pulp.PULP_CBC_CMD(msg=0))

        # Results
        selected_times = [t for t in times if x[t].value() == 1]
        covered_students = sum(y[s].value() for s in students)
        total_students = len(students)
        coverage_percent = (covered_students / total_students) * 100

        selected_times = [t for t in times if x[t].value() == 1]
        covered_students = sum(y[s].value() for s in students)

        total_students = len(students)
        coverage_percent = (covered_students / total_students) * 100

        #print("Optimal Office Hours:", selected_times)
        #print(f"Student Coverage: {covered_students}/{total_students} ({coverage_percent:.1f}%)")

        return [selected_times, covered_students, total_students, coverage_percent]

        # Find more workable algorithm to use
        # README and ROBOTS file (Look at their project for reference)
        # Turn into a desktop application

    def pyprint(self, s):
        print("val:", s)

def main():
    pygame.mixer.init()
    api = MainApi()

    api.window = webview.create_window(
        title="Webview for Tyler AI project",
        url="./index.html",
        js_api=api,
        resizable=True,
    )

    webview.start()
    pygame.quit()

if __name__ == "__main__":
    main()
