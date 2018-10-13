import cv2
from darkflow.net.build import TFNet

options = {
	'model': 'cfg/yolo.cfg',
	'load': 'bin/yolov2.weights', # Weights file cannot be uploaded to GitHub due to file size
	'threshold': 0.3
}

tfnet = TFNet(options)

cap = cv2.VideoCapture('video.mp4') # Video is not included in repo
fps = cap.get(cv2.CAP_PROP_FPS)
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

results = {}

for i in range(1, int((length/fps) - 1)):
	cap.set(cv2.CAP_PROP_POS_MSEC, i*1000)
	ret, frame = cap.read()
	preds = tfnet.return_predict(frame)

	objects_in_frame = []
	for pred in preds:
		if pred['label'] not in objects_in_frame:
			objects_in_frame.append(pred['label'])

	results[i] = objects_in_frame