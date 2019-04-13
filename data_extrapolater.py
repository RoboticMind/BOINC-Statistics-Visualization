import csv
import datetime
stats=[]
dates=[]
with open('Stats.csv', newline='') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	csvreader = list(csvreader)[1:] #[1:] drops headers
	for rawrow in csvreader:
		rowdata=rawrow[0].split(",")
		date=rowdata[0].split("-")
		date=datetime.date(int(date[0]),int(date[1]),int(date[2]))
		dates.append(date)
		stats.append(int(float(rowdata[1])))
	sorted_dates=sorted(dates)
	indexes = [dates.index(x) for x in sorted_dates]

newdata=csvreader

extractnew=False # tells wether or not to try and find new data
writeolddata=False #is ignored if extractnew it True
if extractnew==True:  
	data=csvreader

	for _ in dates:
		try:
			dates.index(_-datetime.timedelta(days=1))
		except:
			if not data[dates.index(_)][0].split(",")[2]=="": #see if there is a Credit per day on that day
				newdate=(_-datetime.timedelta(days=1)).isoformat() #newdate = (index - oneday) in iso format 
				newtotalcredits=int(data[dates.index(_)][0].split(",")[1])-int(data[dates.index(_)][0].split(",")[2]) 
				#newtotalcredits = current credits - day's credits 
				newdata+=[[newdate + ',' + str(newtotalcredits) + ',']] #add format like csv of newdates and credits
	with open("output.csv","w",newline='') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=' ',quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csvwriter.writerow(['Date,Total', 'credit,Credit', 'per', 'day'])
		for extract in newdata:
			csvwriter.writerow(extract)
elif writeolddata==True:
	with open("output.csv","w",newline='') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=' ',quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csvwriter.writerow(['Date,Total', 'credit,Credit', 'per', 'day'])
		for f in indexes:
			csvwriter.writerow(csvreader[f])
