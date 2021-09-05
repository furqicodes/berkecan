#import rovpy
import time
import movement_demo


def main():
	hedef = movement_demo.detect()
	mesafe = 0 # sensör çağır
	
	if !hedef:
		if mesafe < 50:
			print("Sola dönülüyor")
			yaw(1400)
		else:
			priny("Düz ilerleniyor")
			forward(1600)
	else
		print("Hedefe ilerleniyor")	# hedefe ilerle

if __name__ == "__main__":
	main()
