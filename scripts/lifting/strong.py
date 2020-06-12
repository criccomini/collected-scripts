#!/usr/bin/env python

"""
Date,Workout Name,Exercise Name,Set Order,Weight,Reps,Distance,Seconds,Notes,Workout Notes,RPE
2020-02-03 15:55:27,"Reload (Deadlift)","Deadlift (Barbell)",1,135.0,5,0,0,"","",
"""

import collections
import csv
import string
import sys

EXERCISES = {'Deadlift (Barbell)', 'Squat (Barbell)', 'Bench Press (Barbell)', 'Overhead Press (Barbell)'}

def calc_rm(weight, reps):
  # Wendler's 5/3/1 formula
  return int((weight * reps / 30) + weight)

def get_rm_stats(strong_csv_loc):
  rm_stats = []

  with open(strong_csv_loc) as strong_csv_fp:
    strong_csv = csv.reader(strong_csv_fp)
    strong_csv.next() # skip header

    for row in strong_csv:
      date, workout, exercise, set_num, set_weight, set_reps, distance, seconds, notes, workout_notes, rpe = row

      # Strip time from date, and format some strings as ints
      date = date[:10]
      set_reps = int(set_reps)
      set_weight = int(float(set_weight))

      if exercise in EXERCISES:
        rm = set_weight if set_reps == 1 else calc_rm(set_weight, set_reps)

        rm_stats.append({
          'date': date,
          'rm': rm,
          'tested': 'Tested' if set_reps == 1 else 'Estimated ({}@{}lbs)'.format(set_reps, set_weight),
          'program': workout,
          'exercise': exercise
        })

  return rm_stats

def group_rm_stats(rm_stats):
  grouped_rm_stats = {}

  for rm_stat in rm_stats:
    grouped_rm_stats.setdefault(rm_stat['exercise'], []).append(rm_stat)

  return grouped_rm_stats

def filter_rm_stats(rm_stats):
  filtered_rm_stats = []
  sorted_rm_stats = sorted(rm_stats, key=lambda entry: (entry['date'], entry['tested'], entry['rm']))
  current_max_estimated_rm = -1

  for entry in sorted_rm_stats:
    # Always include the largest tested RM for a day, but only include new estimated RMs.
    if entry['tested'] == 'Tested' or entry['rm'] > current_max_estimated_rm:
      last_entry = filtered_rm_stats[-1] if filtered_rm_stats else None

      # This is a hack to check the first N characters of 'tested' to see if they match.
      # Have to do this becuase "Estimated" containus rep and weight counts in its value.
      same_test_type = last_entry['tested'][:5] == entry['tested'][:5] if last_entry else False

      # Only keep the largest entry per-date/test combination.
      # Otherwise, you see multiple entries per-day as I work up to and break multiple RMs.
      # This works because the rm_stats are sorted by (date, test, rm) ascending
      if same_test_type and last_entry['date'] == entry['date'] and last_entry['rm'] <= entry['rm']:
        filtered_rm_stats.pop()

      filtered_rm_stats.append(entry)

      if entry['tested'] != 'Tested':
        current_max_estimated_rm = entry['rm']

  return filtered_rm_stats

def render_md(rm_stats):
  lines = [
    '| Date       | 1RM | {tested: <22} | {program: <30} |'.format(tested='Type', program='Program'),
    '|------------|-----|{}|{}|'.format('-' * 24, '-' * 32)
  ]

  for entry in rm_stats:
    lines.append('| {date} | {rm: <3} | {tested: <22} | {program: <30} |'.format(**entry))

  return '\n'.join(lines)

def render_template_to_file(template_loc, output_loc, vars):
  with open(template_loc, 'r') as i, open(output_loc, 'w') as o:
    t = string.Template(i.read())
    o.write(t.substitute(vars))

if __name__=='__main__':
  if len(sys.argv) < 3:
    raise ValueError("Missing parameters for [template file] [render file] [strong.csv file location...]")
  
  rm_stats = []

  template_loc = sys.argv[1]
  render_loc = sys.argv[2]

  # Load RM stats
  for file_loc in sys.argv[3:]:
    rm_stats = rm_stats + get_rm_stats(file_loc)

  grouped_rm_stats = group_rm_stats(rm_stats)
  rendered_rm_stats = {}

  for exercise in sorted(list(EXERCISES)):
    template_key = exercise.replace(' (Barbell)', '').replace(' ', '_').lower() + '_table'
    filtered_rm_stats = filter_rm_stats(grouped_rm_stats[exercise])
    rendered_rm_stats[template_key] = render_md(reversed(filtered_rm_stats))

  render_template_to_file(template_loc, render_loc, rendered_rm_stats)
