import csv
import datetime
import json
import pprint

from pytz import timezone

with open('stacked-data-clean.json') as f, open('stacked.csv', 'w') as o:
  stacked_data = json.load(f)
  stacked_csv_writer = csv.DictWriter(o, quoting=csv.QUOTE_NONNUMERIC, fieldnames=[
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

  stacked_csv_writer.writeheader()

  for workout in stacked_data:
    if not workout or workout['workout']['isDeleted']:
      continue

    date = datetime.datetime.strptime(workout['completedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
    date = date.replace(tzinfo=timezone('UTC'))
    date = date.astimezone(timezone('US/Pacific'))
    date = date.strftime('%Y-%m-%d %H:%M:%S')

    workout_name = workout['workoutName']
    workout_notes = workout['notes']

    for set_summary in workout['summarySets']:
      exercise_name = set_summary['exerciseName']
      set_order = set_summary['position'] + 1
      weight = set_summary['weight']
      reps = set_summary['reps']
      distance = 0
      seconds = 0
      notes = None
      rpe = None

      stacked_csv_writer.writerow({
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