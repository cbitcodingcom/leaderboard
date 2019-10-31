from django.shortcuts import render, HttpResponse, render
import urllib.request
import json
from .models import Hacker

# Create your views here.

def index(request):
	hackers = Hacker.objects.order_by('-score', 'time')
	return render(request, 'rankings/index.html', {"hackers":hackers})

def update(request):
	if(request.method == "GET"):
		return render(request, 'rankings/update.html')
	elif(request.method == "POST"):
		url = request.POST["contest_link"]
		url = url.split("***")
		if(len(url) > 1 and url[1] == "2407"):
			url = url[0]
			json_data = urllib.request.urlopen(url)
			json_data = json_data.read().decode('utf-8')
			json_data = json.loads(json_data)
			#return HttpResponse(str(json_data))
			context = {"count":str(json_data["total"]), "contest_link":url}
			return render(request, 'rankings/confirm.html', context)
		else:
			return HttpResponse("You dont have access to this page")


def confirm(request):
	if(request.method == "POST"):
		try:
			url = request.POST["contest_link"]
			json_data = urllib.request.urlopen(url)
			json_data = json_data.read().decode('utf-8')
			json_data = json.loads(json_data)

			for hacker in json_data["models"]:
				name = hacker["hacker"]
				num_results = Hacker.objects.filter(name=name).count()
				if(num_results == 0):
					hacker_obj = Hacker(name=name, score=hacker["score"], time=hacker["time_taken"])
					hacker_obj.save()
				elif(num_results == 1):
					hacker_obj = Hacker.objects.get(name = name)
					hacker_obj.score += hacker["score"]
					hacker_obj.time += hacker["time_taken"]
					hacker_obj.save()
			return HttpResponse("Updated database")
		except Exception as msg:
			return HttpResponse(str(msg))



