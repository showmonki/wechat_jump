import cv2
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import wda
import time
import random

c = wda.Client("http://192.168.0.103:8100")
s = c.session()
c.screenshot("/users/nanzou/documents/test.png")

def examine():
	pic = cv2.imread("/users/nanzou/documents/test.png", 0)
	temp_end = cv2.imread("/users/nanzou/documents/end.png", 0)
	res_end = cv2.matchTemplate(pic, temp_end, cv2.TM_CCOEFF_NORMED)
	end = cv2.minMaxLoc(res_end)[1]
	return pic,end

def load(pic):

	template = cv2.imread("/users/nanzou/documents/circle.png", 0)
	w, h = template.shape[::-1]
	res = cv2.matchTemplate(pic, template, cv2.TM_CCOEFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	template_center = int(max_loc[0] + w / 2), int(max_loc[1] + h / 2)
	return template_center,max_loc,w,h

def juli(pic):
	template_center, max_loc, w, h = load(pic)
	pic_1 = cv2.imread("/users/nanzou/documents/test.png")
	gaussed = cv2.GaussianBlur(pic_1, (3,3), 0)
	cannyed = cv2.Canny(gaussed, 10, 70)
	cannyed2 = cv2.cvtColor(cannyed, cv2.COLOR_GRAY2BGR)
	#plt.imshow(cannyed2)
	y,x = np.where(cannyed2==[255,255,255])[0:2]
	test=np.vstack((y,x))
	if y[y>240][0]<max_loc[1]:
		final_x = test[1][test[0]>240][0]
		final_y = test[0][test[0]>240][0]+h/2
	else:
		result = pd.DataFrame({"x": x, "y": y})
		result['mark'] = int()
		result.mark[(result.x > max_loc[0]) & (result.x < (max_loc[0]+h))] = 1
		y_for_x = result.y[(result.mark == 0) & (result.y > 240)].min()
		final_x = result.x[(result.y == y_for_x) & (result.mark == 0)].min()
		final_y = y_for_x+h/2
	dist = np.sqrt(np.square(template_center[0]-final_x)+np.square(template_center[1]-final_y))
	cv2.rectangle(pic_1, max_loc, (max_loc[0] + w, max_loc[1] + h), 0, 2)
	cv2.circle(pic_1, (final_x, int(final_y)), 10, (255, 255, 255), -1)
	cv2.circle(pic_1, template_center, 2, (255, 255, 255), -1)
	cv2.imwrite("/users/nanzou/documents/result.png", pic_1)
	press_time = dist * np.square(0.047122135)
	return press_time



def j():
	press_time = juli(pic)
	s.tap_hold(293,516,press_time)

for i in range(80):
#for i in range(random.randint(20,30)):
		pic, end = examine()
		#str = input()
		#while str==1:
		if end >0.95:
			print("Game Over")
			break
		else:
			j()
			print("第", i + 1, "次跳跃")
			time.sleep(1.1)
			c.screenshot("/users/nanzou/documents/test.png")

