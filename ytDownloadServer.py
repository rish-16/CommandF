from __future__ import unicode_literals
import youtube_dl
from flask import Flask, render_template, request
import os
import time
from collections import OrderedDict
import json
import math
import cv2
from darkflow.net.build import TFNet

app = Flask(__name__)
searchParams = []
subtitles = []

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/timestamps")
def timestamps():
	with open("timestamps.txt") as in_timestamps:
		timestamps = in_timestamps.read()
	return timestamps

@app.route("/download", methods=['GET', 'POST'])
def download_file():
	global searchParams
	vidurl = request.form['vidurl']
	search_query = request.form['searchParams'].lower()
	searchParams = search_query.split(",")
	#print(searchParams)
	# for i in searchParams:
	# 	searchParams[i] = searchParams[i].lower()
	print(vidurl)
	#print(searchParams)
	#vidurl = 'https://www.youtube.com/watch?v=BaW_jenozKc' # put the url of the video here

	# list of options for the downloader
	global subtitles
	options = {
		'progress_hooks': [progressHook],
		'writesubtitles': True,
	}
	with youtube_dl.YoutubeDL(options) as ydl:
		ydl.download([vidurl])

	#return render_template('final.html', timestamps=timestamps)
	print(subtitles)
	return 'done'

progress = ''
def progressHook(d):
	progress = d['status']
	global subtitles
	if progress == 'finished':
		print(subtitles)
		subtitle_path = os.path.abspath(d['filename'].split('.mp4')[0]+".en.vtt")
		print(subtitle_path)
		vid_path = os.path.abspath(d['filename'])
		subtitles_string = findTimestampsText(vid_path, subtitle_path, d['filename'])
		yolo_string = YOLOpredictions(vid_path, d['filename'])
		unifiedSearch(subtitles_string, yolo_string)

def findTimestampsText(vidfilepath, subtfilepath, vidfilename):
	try:
		fh = open(vidfilename+"_subtitles.json", "r")
		json_str = fh.read()
		json_data = json.loads(json_str)
		string = subtSearch(json_data)
		fh.close()
		os.remove(vidfilepath)
		os.remove(subtfilepath)
		return string
	except FileNotFoundError:
		line_dict = {}
		line_list = []
		print("File not found")
		# print(subtfilename)
		# print(vidfilepath)
		with open(subtfilepath, 'rt') as raw_subtitles:
			line = raw_subtitles.readline()
			line_number = 1
			while line:
				line = raw_subtitles.readline()
				print("Line {}: {}".format(line_number, line.strip()))
				line_number += 1
				line = line.lower()
				if line_number>=4 and line!="\n":
					if(len(line.split(' --> '))>1):
						print(line[:-1])
						timestamp = line[:-1].split(" --> ")[0]
						continue
					#print(line_dict.keys()
					#print(timestamp)
					#print(line_dict.keys())
					if timestamp.encode('utf-8') in line_dict.keys():
						line_dict[timestamp] = line_dict[timestamp]+" "+line[:-1]
						print(line_dict[timestamp]+" "+timestamp)
						continue
					#print("normal")
					line_dict[timestamp] = line[:-1]
			os.remove(vidfilepath)
			os.remove(subtfilepath)
			#print(line_dict)
			
		# Write to file
		with open('{}_subtitles.json'.format(vidfilename), 'w+') as f:
			f.write(json.dumps(line_dict))
			
		string = subtSearch(line_dict)
		print(string)
		return string

def subtSearch(line_dict):
	global searchParams
	timestr = ""
	for key, value in line_dict.items():
		for word in searchParams:
			if word in value:
				timestr += key+" "
			
	return timestr

	#return new_dict

def YOLOpredictions(videofile, vidfilename):
	# videofile -> MP4 format
	try:
		fh = open(vidfilename+"_yolo.json", "r")
		json_str = fh.read()
		json_data = json.loads(json_str)
		string = getYOLOtimestamps(json_data)
		fh.close()
		return string
	except FileNotFoundError:
		params = {
			'model': 'cfg/yolo.cfg',
			'load': 'bin/yolov2.weights', # Weights file cannot be uploaded to GitHub due to file size
			'threshold': 0.3
		}

		tfnet = TFNet(params)

		cap = cv2.VideoCapture(videofile) # Video is not included in repo
		fps = cap.get(cv2.CAP_PROP_FPS)
		length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

		results = {}

		for i in range(1, int((length/fps))):
			if fps > 0:
				cap.set(cv2.CAP_PROP_POS_MSEC, i*1000)
				ret, frame = cap.read()
				preds = tfnet.return_predict(frame)

				objects_in_frame = []
				for pred in preds:
					if pred['label'] not in objects_in_frame:
						objects_in_frame.append(pred['label'])
						
				print (objects_in_frame)

				results[i] = objects_in_frame
			
		# Write to file
		with open('{}_yolo.json'.format(vidfilename), 'w+') as f:
			f.write(json.dumps(results))
		
		string = getYOLOtimestamps(results)
		return string
	
def getYOLOtimestamps(yolo_dict):
	global searchParams
	timestamp_string = ''
	for key, value in yolo_dict.items():
		for word in searchParams:
			if word in value:
				timestamp_string += key + ' '

	return timestamp_string
	
def unifiedSearch(subt_str, yolo_str):
	
	# First goes through YOLO search
	# Then goes through Subtitle search
	
	# returns all possible timestamps
	
	final_timestr = subt_str + ' ' + yolo_str
	
	with open('timestamps.txt', 'w') as timeFile:
		timeFile.write(final_timestr)