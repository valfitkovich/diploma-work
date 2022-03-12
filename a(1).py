import random

count_of_days = 4
count_of_rooms = 3
count_of_times = 5
group_class_list = [(101, 'math'), (101, 'physics'), (101, 'chemists'),
                    (101, 'math'), (101, 'physics'), (101, 'chemists'),
                    (101, 'music'), (101, 'english'), (101, 'history'),
                    (102, 'math'), (102, 'physics'), (102, 'chemists'),
                    (102, 'music'), (102, 'english'), (102, 'history'),
                    (103, 'math'), (103, 'physics'), (103, 'chemists'),
                    (103, 'music'), (103, 'english'), (103, 'history')
                    ]
group_class_list = [(101, 'math'),(101, 'math'),(101, 'math'),(101, 'math'),(101, 'math'),(101, 'math'),(101, 'math'),(101, 'math'),(101, 'math'),(101, 'math'),(101, 'math'),
(102, 'math'),(102, 'math'),(102, 'math'),(102, 'math'),(102, 'math'),(102, 'math'),(102, 'math'),(102, 'math'),(102, 'math'),(102, 'math'),(102, 'math'),(102, 'math'),
(103, 'math'),(103, 'math'),(103, 'math'),(103, 'math'),(103, 'math'),(103, 'math'),(103, 'math'),(103, 'math')]
# group_class_list = [(101, 'math'),(101, 'math'),(101, 'math'), (101, 'physics'), (101, 'chemists'),
#                     (101, 'math'), (101, 'physics'), (101, 'chemists'),
#                     (101, 'music'), (101, 'english'), (101, 'history'),
#                     (102, 'math'), (102, 'physics'), (102, 'chemists'),
#                     (102, 'music'), (102, 'english'), (102, 'history'),
#                     (103, 'math'), (103, 'physics'), (103, 'chemists'),
#                     (103, 'music'), (103, 'english'), (103, 'history')
#                     ]


class Timetable:
	def __init__(self, cnt_day, cnt_room, cnt_lesson, schema):
		self.cnt_day = cnt_day
		self.cnt_room = cnt_room
		self.cnt_lesson = cnt_lesson
		self.schema = schema
		self.timetable = [[[None] * cnt_room for i in range(cnt_lesson)] for j in range(cnt_day)]
		self.count_of_generations = 1000

	def gen_cond(self, type_cond):
		# todo: дописать разные виды условий!!!
		cond = dict()
		
		set_of_groups = set()
		for group, subject in self.schema:
			set_of_groups.add(group)

		set_of_subjects = set()
		for group, subject in self.schema:
			set_of_subjects.add(subject)

		if type_cond == 0:
		 # рассписание для отдельных групп			
			for gruop in set_of_groups:
				cond[gruop] = [[0] * self.cnt_lesson for _ in range(self.cnt_day)]

			for day in range(len(self.timetable)):
				for lesson in range(len(self.timetable[day])):
					for room in range(len(self.timetable[day][lesson])):
						group_subj = self.timetable[day][lesson][room]
						if group_subj is not None:
							group, subj = group_subj
							cond[group][day][lesson] += 1
		
		elif type_cond == 1:
			for group in set_of_groups:
				cond[group] = dict()
				for subject in set_of_subjects:
					cond[group][subject] = [0] * self.cnt_day 

			for day in range(len(self.timetable)):
				for lesson in range(len(self.timetable[day])):
					for room in range(len(self.timetable[day][lesson])):
						group_subj = self.timetable[day][lesson][room]
						if group_subj is not None:
							group, subj = group_subj
							cond[group][subj][day] += 1

		elif type_cond == 2:
			for group in set_of_groups:
				cond[group] = dict()
				for subject in set_of_subjects:
					cond[group][subject] = [0] * self.cnt_day 

			for day in range(len(self.timetable)):
				for lesson in range(len(self.timetable[day])):
					for room in range(len(self.timetable[day][lesson])):
						group_subj = self.timetable[day][lesson][room]
						if group_subj is not None:
							group, subj = group_subj
							cond[group][subj][day] += 1
							if (day + 1 < self.cnt_day):
								cond[group][subj][day + 1] += 1
							if (day - 1 >= 0):
								cond[group][subj][day - 1] += 1

		return cond		
		

	def __str__(self):
		ans = '-----------\n'
		for day in range(len(self.timetable)):
			ans += f'day {day}\n'
			for lesson in range(len(self.timetable[day])):
				ans += f'lesson {lesson}: ' + str(self.timetable[day][lesson]) + '\n'
		ans += '-----------\n'

		return ans


	def gen_timetable_type_cond(self, type_cond):
		
		def generate_slot():
		    day = random.randrange(self.cnt_day)
		    time = random.randrange(self.cnt_lesson)
		    room = random.randrange(self.cnt_room)
		    return (day, time, room)

		
		if type_cond == 0:

			def check_setup(group, day, time, room):
				conditionals = self.gen_cond(0)
				return conditionals[group][day][time] == 0 and self.timetable[day][time][room] is None

			
			def check_swap():
				conditionals = self.gen_cond(0)
				for group in conditionals:
					for day in range(len(conditionals[group])):
						for lesson in range(len(conditionals[group][day])):
							if conditionals[group][day][lesson] >= 2:
								return False
				return True
			

			for item in self.schema:
				group = item[0]
				day, time, room = generate_slot()
				while not check_setup(group, day, time, room):
					day, time, room = generate_slot()
				self.timetable[day][time][room] = item #simple first gen

			print(self)
			for _ in range(self.count_of_generations):
				day_r1, time_r1, room_r1 = generate_slot()
				day_r2, time_r2, room_r2 = generate_slot()
				self.timetable[day_r1][time_r1][room_r1], self.timetable[day_r2][time_r2][room_r2] = self.timetable[day_r2][time_r2][room_r2], self.timetable[day_r1][time_r1][room_r1]
				while not check_swap():
					self.timetable[day_r1][time_r1][room_r1], self.timetable[day_r2][time_r2][room_r2] = self.timetable[day_r2][time_r2][room_r2], self.timetable[day_r1][time_r1][room_r1]
					day_r1, time_r1, room_r1 = generate_slot()
					day_r2, time_r2, room_r2 = generate_slot()
					self.timetable[day_r1][time_r1][room_r1], self.timetable[day_r2][time_r2][room_r2] = self.timetable[day_r2][time_r2][room_r2], self.timetable[day_r1][time_r1][room_r1]
			print(self)
		
		elif type_cond == 1:
			def check_setup(group, day, time, room, subject):
				conditionals = self.gen_cond(0)
				cond_oneclassonday = self.gen_cond(1)
				return conditionals[group][day][time] == 0 and self.timetable[day][time][room] is None and cond_oneclassonday[group][subject][day] == 0

			def check_swap():
				conditionals = self.gen_cond(0)
				cond_oneclassonday = self.gen_cond(1)
				for group in conditionals:
					for day in range(len(conditionals[group])):
						for lesson in range(len(conditionals[group][day])):
							if conditionals[group][day][lesson] >= 2:
								return False

				for group in cond_oneclassonday:
					for subject in cond_oneclassonday[group]:
						for day in range(len(cond_oneclassonday[group][subject])):
							if cond_oneclassonday[group][subject][day] > 1:
								return False
				return True


			for item in self.schema:
				group, subject = item
				day, time, room = generate_slot()
				while not check_setup(group, day, time, room, subject):
					day, time, room = generate_slot()
				self.timetable[day][time][room] = item #one_class_day gen
			print(self)

			for _ in range(self.count_of_generations):
				# print(_)
				day_r1, time_r1, room_r1 = generate_slot()
				day_r2, time_r2, room_r2 = generate_slot()
				self.timetable[day_r1][time_r1][room_r1], self.timetable[day_r2][time_r2][room_r2] = self.timetable[day_r2][time_r2][room_r2], self.timetable[day_r1][time_r1][room_r1]
				while not check_swap():
					self.timetable[day_r1][time_r1][room_r1], self.timetable[day_r2][time_r2][room_r2] = self.timetable[day_r2][time_r2][room_r2], self.timetable[day_r1][time_r1][room_r1]
					day_r1, time_r1, room_r1 = generate_slot()
					day_r2, time_r2, room_r2 = generate_slot()
					self.timetable[day_r1][time_r1][room_r1], self.timetable[day_r2][time_r2][room_r2] = self.timetable[day_r2][time_r2][room_r2], self.timetable[day_r1][time_r1][room_r1]
			print(self)


		elif type_cond == 2:
			def check_setup(group, day, time, room, subject):
				conditionals = self.gen_cond(0)
				cond_oneclassonday_breakday = self.gen_cond(2)
				return conditionals[group][day][time] == 0 and self.timetable[day][time][room] is None and cond_oneclassonday_breakday[group][subject][day] == 0



			def check_swap():
				conditionals = self.gen_cond(0)
				cond_oneclassonday_breakday = self.gen_cond(2)
				for group in conditionals:
					for day in range(len(conditionals[group])):
						for lesson in range(len(conditionals[group][day])):
							if conditionals[group][day][lesson] >= 2:
								return False

				for group in cond_oneclassonday_breakday:
					for subject in cond_oneclassonday_breakday[group]:
						for day in range(len(cond_oneclassonday_breakday[group][subject])):
							if cond_oneclassonday_breakday[group][subject][day] > 1 and ((day + 1 < self.cnt_day and cond_oneclassonday_breakday[group][subject][day + 1] > 1) or (day - 1) >= 0 and cond_oneclassonday_breakday[group][subject][day + 1] > 1):
								return False

				return True

			for item in self.schema:
				group, subject = item
				day, time, room = generate_slot()
				while not check_setup(group, day, time, room, subject):
					day, time, room = generate_slot()
				self.timetable[day][time][room] = item #one_class_day gen
			print(self)

			for _ in range(self.count_of_generations):
				day_r1, time_r1, room_r1 = generate_slot()
				day_r2, time_r2, room_r2 = generate_slot()
				self.timetable[day_r1][time_r1][room_r1], self.timetable[day_r2][time_r2][room_r2] = self.timetable[day_r2][time_r2][room_r2], self.timetable[day_r1][time_r1][room_r1]
				while not check_swap():
					self.timetable[day_r1][time_r1][room_r1], self.timetable[day_r2][time_r2][room_r2] = self.timetable[day_r2][time_r2][room_r2], self.timetable[day_r1][time_r1][room_r1]
					day_r1, time_r1, room_r1 = generate_slot()
					day_r2, time_r2, room_r2 = generate_slot()
					self.timetable[day_r1][time_r1][room_r1], self.timetable[day_r2][time_r2][room_r2] = self.timetable[day_r2][time_r2][room_r2], self.timetable[day_r1][time_r1][room_r1]
			print(self)



		elif type_cond == 3:
			def check_setup(group, day, time, room):
				conditionals = self.gen_cond(0)
				return conditionals[group][day][time] == 0 and self.timetable[day][time][room] is None and (sum(conditionals[group][day]) == 0 or (time - 1 >= 0 and conditionals[group][day][time - 1] == 1) or (time + 1 < self.cnt_lesson
				 and conditionals[group][day][time + 1] == 1))

			def check_day(conditionals, group, day):
				ar = conditionals[group][day]
				if sum(ar) == 0:
					return True
				else:
					lst = 0
					cnt_segm = 0
					for i in range(len(ar)):
						if lst == 0 and ar[i] == 1:
							lst = 1
							cnt_segm += 1
						elif ar[i] == 0:
							lst = 0
					if cnt_segm == 1:
						return True
				return False

			def check_swap():
				conditionals = self.gen_cond(0)
				for group in conditionals:
					for day in range(len(conditionals[group])):
						for lesson in range(len(conditionals[group][day])):
							if conditionals[group][day][lesson] >= 2:
								return False


				for group in conditionals:
					for day in range(len(conditionals[group])):
						if not check_day(conditionals, group, day):
							return False
				return True

			
			for item in self.schema:
				group = item[0]
				day, time, room = generate_slot()
				while not check_setup(group, day, time, room):
					day, time, room = generate_slot()
				self.timetable[day][time][room] = item #simple first gen
			print(self)

			for _ in range(self.count_of_generations):
				day_r1, time_r1, room_r1 = generate_slot()
				day_r2, time_r2, room_r2 = generate_slot()
				self.timetable[day_r1][time_r1][room_r1], self.timetable[day_r2][time_r2][room_r2] = self.timetable[day_r2][time_r2][room_r2], self.timetable[day_r1][time_r1][room_r1]
				while not check_swap():
					self.timetable[day_r1][time_r1][room_r1], self.timetable[day_r2][time_r2][room_r2] = self.timetable[day_r2][time_r2][room_r2], self.timetable[day_r1][time_r1][room_r1]
					day_r1, time_r1, room_r1 = generate_slot()
					day_r2, time_r2, room_r2 = generate_slot()
					self.timetable[day_r1][time_r1][room_r1], self.timetable[day_r2][time_r2][room_r2] = self.timetable[day_r2][time_r2][room_r2], self.timetable[day_r1][time_r1][room_r1]
			print(self)

		elif type_cond == 4:
			def get_day(conditionals, group):
				cnt_lst = []
				for i in range(len(conditionals[group])):
					cnt_lst.append((sum(conditionals[group][i]), i))
				cnt_lst.sort()
				return cnt_lst[0][1]

			def check_setup(group, day, time, room):
				conditionals = self.gen_cond(0)
				return conditionals[group][day][time] == 0 and self.timetable[day][time][room] is None


			def check_day(conditionals, group, day):
				sm = sum(conditionals[group][day])
				return (sm >= 2 and sm <= 5)

			def first_gen():
				for item in self.schema:
					group, subject = item
					conditionals = self.gen_cond(0)
					day = get_day(conditionals, group)
					flag = False
					for time in range(self.cnt_lesson):
						for room in range(self.cnt_room):
							if check_setup(group, day, time, room):
								self.timetable[day][time][room] = item
								flag = True
							if flag:
								break
						if flag:
							break
				for _ in range(100):
					day_r1, time_r1, room_r1 = generate_slot()
					day_r2, time_r2, room_r2 = generate_slot()
					self.timetable[day_r1][time_r1][room_r1], self.timetable[day_r2][time_r2][room_r2] = self.timetable[day_r2][time_r2][room_r2], self.timetable[day_r1][time_r1][room_r1]
					while not check_swap():
						self.timetable[day_r1][time_r1][room_r1], self.timetable[day_r2][time_r2][room_r2] = self.timetable[day_r2][time_r2][room_r2], self.timetable[day_r1][time_r1][room_r1]
						day_r1, time_r1, room_r1 = generate_slot()
						day_r2, time_r2, room_r2 = generate_slot()
						self.timetable[day_r1][time_r1][room_r1], self.timetable[day_r2][time_r2][room_r2] = self.timetable[day_r2][time_r2][room_r2], self.timetable[day_r1][time_r1][room_r1]



			def check_swap():
				conditionals = self.gen_cond(0)
				for group in conditionals:
					for day in range(len(conditionals[group])):
						for lesson in range(len(conditionals[group][day])):
							if conditionals[group][day][lesson] >= 2:
								return False


				for group in conditionals:
					for day in range(len(conditionals[group])):
						if not check_day(conditionals, group, day):
							return False
				return True

			first_gen()
			print(self)
			
			for _ in range(self.count_of_generations):
				day_r1, time_r1, room_r1 = generate_slot()
				day_r2, time_r2, room_r2 = generate_slot()
				self.timetable[day_r1][time_r1][room_r1], self.timetable[day_r2][time_r2][room_r2] = self.timetable[day_r2][time_r2][room_r2], self.timetable[day_r1][time_r1][room_r1]
				while not check_swap():
					self.timetable[day_r1][time_r1][room_r1], self.timetable[day_r2][time_r2][room_r2] = self.timetable[day_r2][time_r2][room_r2], self.timetable[day_r1][time_r1][room_r1]
					day_r1, time_r1, room_r1 = generate_slot()
					day_r2, time_r2, room_r2 = generate_slot()
					self.timetable[day_r1][time_r1][room_r1], self.timetable[day_r2][time_r2][room_r2] = self.timetable[day_r2][time_r2][room_r2], self.timetable[day_r1][time_r1][room_r1]
			print(self)



t = Timetable(count_of_days, count_of_rooms, count_of_times, group_class_list)
# print(t.gen_cond(0))
t.gen_timetable_type_cond(4)

# print(t.gen_cond(0))

