import datetime
import threading

class BddAsJson():

	def __init__(self):
		self.json_bdd=[]
		self.obj_number=0
		self.task_per_page=None

	def save_entry(self):
		task = ToDo()
		task.create_entry()
		self.obj_number+=1
		insert = task.get_priority()
		if insert >= len(self.json_bdd):
			self.json_bdd.append(task)
		else:
			self.json_bdd.insert(insert, task)

	def delete_entry(self):
		self.show_list()
		del_id = input("Select the task to delete by writing down the priority number of the task\n->")
		try:
			del_id = int(del_id)
			if del_id < len(self.json_bdd):
				del self.json_bdd[del_id]
			else:
				print("Write a good number\n")
		except:
			print("Priority number is a number\n")

	def show_list(self):
		print("List of ToDo in priority order:\n")
		for priority, obj in enumerate(self.json_bdd[:self.task_per_page]):
			print("ID:{}\nThe task {} have to be done before {} and was created at {}\n".format(priority, obj.name, obj.end_date, obj.created_date))
	
	def editing_task(self):
		self.show_list()
		edit_id = input("Select the task to edit by writing down the priority number of the task\n->")
		try:
			edit_id = int(edit_id)
			if edit_id < len(self.json_bdd):
				self.json_bdd[edit_id].edit_object()
			else:
				print("Write a good number\n")
		except:
			print("Priority number is a number\n")

	def priority_number(self):
		self.show_list()
		try:
			priority_id = input("Select the task to change it priority by writing down the priority number of the task\n->")
			priority_id = int(priority_id)
			if priority_id >= len(self.json_bdd):
				print("Wrong priority number")
			else:
				priority_id_new = input("Select the new priority number of the task\n->")
			try:
				priority_id_new = int(priority_id_new)
				task = self.json_bdd[priority_id]
				del self.json_bdd[priority_id]
				if priority_id_new >= len(self.json_bdd):
					self.json_bdd.append(task)
				else:
					self.json_bdd.insert(priority_id_new, task)
			except:
				print("this is not a number")
		except:
			print("this is not a number")
			
	def set_end_date_to_none(self):
		#map(lambda x: x.set_end_date(None), self.json_bdd)
		for obj in self.json_bdd:
			obj.set_end_date(None)

	def add_hour_to_all(self):
		hours = input("How much hours you want to add to every task?\n->")
		try:
			hours = datetime.timedelta(hours=int(hours))
			for obj in self.json_bdd:
				obj.add_hours_to_end_date(hours)
			#map(lambda x: x.add_hours_to_end_date(hours), self.json_bdd)
		except:
			print("You have to put a real number")

	def activate_reminder(self):
		self.show_list()
		obj_id = input("Select the task to activate the reminder by writing down the priority number of the task\n->")
		try:
			obj_id = int(obj_id)
			if obj_id < len(self.json_bdd):
				self.json_bdd[obj_id].print_reminder()
			else:
				print("Write a good number\n")
		except:
			print("Priority number is a number\n")

	def change_task_per_page(self):
		page = input("How much task you want to show per page?\n->")
		try:
			self.task_per_page = int(page)
			if self.task_per_page is 0:
				self.task_per_page = None
		except:
			print("You have to put a real number")

	def show_task_number(self):
		print("Number of task saved {} ".format(len(self.json_bdd)))

	def show_task_created(self):
		print("Number of task created from the begining {} ".format(self.obj_number))

class ToDo():

	def __init__(self):
		self.name = ""
		self.created_date = datetime.datetime.now()
		self.end_date = None
		self.priority = 0
		self.reminder = datetime.time(minute=5)

	def create_entry(self):
		self.name = input("Name:")

		state = ""
		while (state != "pass"):
			state = input("End_date:")
			try:
				self.end_date = datetime.datetime.strptime(state, '%b %d %Y %I:%M%p')
				state = "pass"
			except:
				print("The format you have to use is:\nJun 1 2005  1:33PM\nor you can write \"pass\" to set the end date to infinite\n")
		
		state = ""
		while (state != "pass"):
			state = input("Priority:")
			try:
				self.priority =int(state)
				state = "pass"
			except:
				print("You have to write a number or write 'pass'\n")
		self.print_date()

	def get_priority(self):
		return self.priority

	def edit_object(self):
		name = input("Write a new name, write nothing to not change the value\n->")
		if name != "":
			self.name = name
		date = input("Write a new end date, write nothing to not change the value, write None to set infinite for the end_date")
		if date == "None":
			self.end_date = None
		elif date != "":
			try:
				self.end_date = datetime.datetime.strptime(date, '%b %d %Y %I:%M%p')
			except:
				print("The format you have to use is:\nJun 1 2005  1:33PM\n")

	def print_date(self):
		if self.end_date is not None and self.end_date > datetime.datetime.now():
			threading.Timer(1, self.print_date).start()
		else:
			print("Your task {} end now\n->".format(self.name))

	def print_reminder(self):
		if self.end_date is None:
			print("No end date set\n")
		if self.end_date - self.reminder > datetime.datetime.now():
			threading.Timer(1, self.print_reminder).start()
		else:
			print("Your task {} will end in 5 minutes\n->".format(self.name))

	def set_end_date(self, new_end_date):
		self.end_date = new_end_date

	def add_hours_to_end_date(self, hours):
		print("foo")
		if self.end_date is not None:
			self.end_date = self.end_date + hours
			print(self.end_date)


def create_choice_list(bdd):
	choice_list = {'change task per page':bdd.change_task_per_page,  'activate reminder':bdd.activate_reminder, 'show task number':bdd.show_task_number, 'show task created':bdd.show_task_created, 'editing task':bdd.editing_task, 'add hour to all task':bdd.add_hour_to_all, 'set all date to None':bdd.set_end_date_to_none, 'change priority':bdd.priority_number, 'add entry': bdd.save_entry, 'delete entry': bdd.delete_entry, 'show list': bdd.show_list, 'quit': True}
	return choice_list


def menu_loop():
	bdd = BddAsJson()
	choice_list = create_choice_list(bdd)
	choice = ""
	while(choice != "quit"):
		for choose in choice_list:
			print(choose)
		print("\nWrite down the command name\n")
		choice = input("->")
		try:
			choice_list[choice]()
		except:
			print("wrong choice\n")

if __name__ == '__main__':
    menu_loop()

