#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Date,Cycle,Week,Set,Name,Completed,Reps,Weights,Notes
Jan 31  2020,7,4,Warmup sets,Overhead Press,Y;Y;Y;,5;5;3;,55.0;70.0;85.0;,
"""

import csv
import datetime

with open('531-raw.csv') as f, open('531.csv', 'w') as o:
  rows = csv.reader(f)
  csv_writer = csv.DictWriter(o, quoting=csv.QUOTE_NONNUMERIC, fieldnames=[
    'Date',
    'Workout Name',
    'Exercise Name',
    'Set Order',
    'Weight',
    'Reps',
    'Distance',
    'Seconds',
    'Notes',
    'Workout Notes',
    'RPE'
  ])

  csv_writer.writeheader()

  for row in rows:
    if row[0] == 'Date':
      continue

    date, cycle, week, workout_set, exercise_name, completed, reps, weights, notes = row

    date = date.replace(',', ' ')
    date = datetime.datetime.strptime(date, '%b %d  %Y')
    date = date.strftime('%Y-%m-%d 16:00:00')

    exercise_name = exercise_name \
      .replace('Dead Lift', 'Deadlift (Barbell)') \
      .replace('Bench Press', 'Bench Press (Barbell)') \
      .replace('Squat', 'Squat (Barbell)') \
      .replace('Overhead Press', 'Overhead Press (Barbell)')

    set_order = 0
    set_reps = reps.split(';')
    set_weights = weights.split(';')

    distance = 0
    seconds = 0
    notes = None
    rpe = None
    workout_name = '5/3/1 (Cycle {}, Week {})'.format(cycle, week)
    workout_notes = None

    for set_completed in completed.split(';'):
      if set_completed == '✔︎':
        weight = set_weights[set_order]
        reps = set_reps[set_order]

        csv_writer.writerow({
          'Date': date,
          'Workout Name': workout_name,
          'Exercise Name': exercise_name,
          'Set Order': set_order,
          'Weight': weight,
          'Reps': reps,
          'Distance': distance,
          'Seconds': seconds,
          'Notes': notes,
          'Workout Notes': workout_notes,
          'RPE': rpe
        })

        set_order += 1