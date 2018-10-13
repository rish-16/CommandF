from __future__ import unicode_literals
import youtube_dl
from flask import Flask, render_template, request
import os
import time
from collections import OrderedDict
import math

app = Flask(__name__)
searchParams = ''

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
	searchParams = request.form['searchParams']
	print(vidurl)
	print(searchParams)
	#vidurl = 'https://www.youtube.com/watch?v=BaW_jenozKc' # put the url of the video here

	# list of options for the downloader
	options = {
		'progress_hooks': [progressHook],
		'writesubtitles': 'subtitles.srt',
	}
	with youtube_dl.YoutubeDL(options) as ydl:
		ydl.download([vidurl])

	#return render_template('final.html', timestamps=timestamps)
	return 'done'

progress = ''
def progressHook(d):
	global progress
	progress = d['status']
	if progress == 'finished':
		subtitle_path = os.path.abspath(d['filename'].split('.')[0]+".en.vtt")
		print(subtitle_path)
		vid_path = os.path.abspath(d['filename'])
		model = findTimestamps(vid_path, subtitle_path)
		print(model)

def 

def findTimestampsText(vidfilename, subtfilename):
	global searchParams
	word = searchParams
	line_dict = {}
	line_list = []
	print(subtfilename)
	print(vidfilename)
	with open(subtfilename, 'rt') as raw_subtitles:
		line = raw_subtitles.readline()
		line_number = 1
		while line:
			line = raw_subtitles.readline()
			#print("Line {}: {}".format(line_number, line.strip()))
			line_number += 1
			if line_number>=4 and line.decode('utf-8')!="\n":
				if(len(line[0:12].decode('ascii', 'ignore').split(':'))>1):
					#print(line[:-1])
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
		os.remove(vidfilename)
		os.remove(subtfilename)
		#print(line_dict)
	#new_dict = {}
	timestr = ""
	for key in line_dict:
		if word in line_dict[key].decode('ascii', 'ignore'):
			timestr += key+" "

	with open('timestamps.txt', 'w') as timeFile:
		timeFile.write(timestr)

	#return new_dict
