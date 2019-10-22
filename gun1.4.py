from random import randrange as rnd, choice
import tkinter as tk
import math
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


class ball():
	def __init__(self, x=40, y=450):
		""" Конструктор класса ball

		Args:
		x - начальное положение мяча по горизонтали
		y - начальное положение мяча по вертикали
		"""
		self.x = x
		self.y = y
		self.r = 10
		self.vx = 1
		self.vy = 1
		self.color = choice(['blue', 'green', 'red', 'brown'])
		self.id = canv.create_oval(
				self.x - self.r,
				self.y - self.r,
				self.x + self.r,
				self.y + self.r,
				fill=self.color
		)
		self.live = 30

	def set_coords(self):
		canv.coords(
				self.id,
				self.x - self.r,
				self.y - self.r,
				self.x + self.r,
				self.y + self.r
		)

	def move(self):
		if (self.x+self.vx<800 and self.y-self.vy<550):
			self.vy-=1
		elif (self.x+self.vx>800 or self.x+self.vx<0):
			self.vx=-self.vx
		elif (self.y-self.vy>550):
			self.vy=-int(0.6*self.vy)
			self.vx=int(0.6*self.vx)
		self.x += self.vx
		self.y -= self.vy
		self.set_coords()
		if (self.vx*self.vx+self.vx*self.vx<10):
			self.live -= 1
		if (self.live <0):
			canv.delete(self.id)
			self.x=0
        
        
	def hittest(self, obj):
		"""Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

		Args:
			obj: Обьект, с которым проверяется столкновение.
		Returns:
			Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
		"""
		if (obj.x-self.x)*(obj.x-self.x)+(obj.y-self.y)*(obj.y-self.y)<(self.r+obj.r)*(self.r+obj.r):
			return True
		else:
			return False


class gun():
	def __init__(self): 
		self.f2_power = 10
		self.f2_on = 0
		self.an = 1
		self.id = canv.create_line(20,450,50,420,width=7) # FIXME: don't know how to set it...

	def fire2_start(self, event):
		self.f2_on = 1

	def fire2_end(self, event):
		"""Выстрел мячом.

		Происходит при отпускании кнопки мыши.
		Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
		"""
		global balls, bullet
		bullet += 1
		new_ball = ball()
		new_ball.r += 5
		self.an = math.atan((event.y-new_ball.y) / (event.x-new_ball.x))
		new_ball.vx = self.f2_power * math.cos(self.an)
		new_ball.vy = - self.f2_power * math.sin(self.an)
		balls += [new_ball]
		self.f2_on = 0
		self.f2_power = 10

	def targetting(self, event=0):
		"""Прицеливание. Зависит от положения мыши."""
		if event:
			self.an = math.atan((event.y-450) / (event.x-20))
		if self.f2_on:
			canv.itemconfig(self.id, fill='orange')
		else:
			canv.itemconfig(self.id, fill='black')
		canv.coords(self.id, 20, 450,
					20 + max(self.f2_power, 20) * math.cos(self.an),
					450 + max(self.f2_power, 20) * math.sin(self.an)
					)

	def power_up(self):
		if self.f2_on:
			if self.f2_power < 100:
				self.f2_power += 1
			canv.itemconfig(self.id, fill='orange')
		else:
			canv.itemconfig(self.id, fill='black')


class target():
	def __init__(self): 
		self.points = 0
		self.live = 1
		self.vx=rnd(-10, 10)
		self.vy=rnd(-10, 10)
		self.id = canv.create_oval(0,0,0,0)
		self.id_points = canv.create_text(30,30,text = self.points,font = '28')
		self.new_target()

	def new_target(self):
		""" Инициализация новой цели. """
		x = self.x = rnd(600, 780)
		y = self.y = rnd(0, 550)
		r = self.r = rnd(20, 50)
		color = self.color = 'red'
		canv.coords(self.id, x-r, y-r, x+r, y+r)
		canv.itemconfig(self.id, fill=color)
		self.vx=rnd(-10, 10)
		self.vy=rnd(-10, 10)
	
	def move(self):
		self.x=self.x+self.vx
		self.y=self.y+self.vy
		if (self.x+self.vx>800 or self.x+self.vx<500):
			self.vx=-self.vx
		if (self.y+self.vy>550 or self.y+self.vy<0):
			self.vy=-self.vy
		canv.coords(
				self.id,
				self.x - self.r,
				self.y - self.r,
				self.x + self.r,
				self.y + self.r)

	def hit(self, points=1):
		"""Попадание шарика в цель."""
		canv.coords(self.id, -10, -10, -10, -10)
		self.x=-10000
		self.points += points
		canv.itemconfig(self.id_points, text=self.points)


screen1 = canv.create_text(400, 300, text='', font='28')
g1 = gun()
bullet = 0
balls = []

def target_all_live():
	global targets
	u=0
	for t in targets:
		if t.live==1:
			u=1
	return u


def new_game(event=''):
	global gun, screen1, balls, bullet, targets
	bullet = 0
	balls = []
	t1=target()
	t2=target()
	t3=target()
	targets=[t1, t2, t3]
	for t in targets:
		t.new_target()
	canv.bind('<Button-1>', g1.fire2_start)
	canv.bind('<ButtonRelease-1>', g1.fire2_end)
	canv.bind('<Motion>', g1.targetting)

	z = 0.03
	for t in targets:
		t.live = 1
	while target_all_live() or balls:
		for t in targets:
			t.move()
		for b in balls:
			b.move()
			for t in targets:
				if b.hittest(t) and t.live:
					t.live = 0
					t.hit()
			if target_all_live()==0:	
				canv.bind('<Button-1>', '')
				canv.bind('<ButtonRelease-1>', '')
				canv.itemconfig(screen1, text='Вы уничтожили цели за ' + str(bullet) + ' выстрелов')
		canv.update()
		time.sleep(0.03)
		g1.targetting()
		g1.power_up()
	canv.itemconfig(screen1, text='')
	canv.delete(gun)
	root.after(750, new_game)

new_game()

mainloop()
